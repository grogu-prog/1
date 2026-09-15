import streamlit as st
import urllib.parse

st.title("🍳 인터넷 실시간 연동 냉장고 레시피")
st.write("냉장고 속 재료들을 선택하면 인터넷(네이버 블로그, 유튜브)에서 최적의 황금 레시피 조합을 실시간으로 검색해 드립니다.")
st.divider()

# 1. 식재료 정보 및 대체재 사전 데이터
if "ingredients_db" not in st.session_state:
    st.session_state.ingredients_db = {
        "양배추": {"expiry": "냉장 보관 시 약 2~3주", "storage": "심지를 파내고 물에 적신 키친타월을 채운 뒤 랩으로 싸서 냉장 보관하세요.", "alternatives": ["배추", "양상추", "청경채", "양파"]},
        "두부": {"expiry": "개봉 후 냉장 2~3일", "storage": "밀폐용기에 두부가 잠길 정도로 찬물을 붓고 소금을 약간 넣어 냉장 보관하세요.", "alternatives": ["연두부", "유부", "버섯", "계란"]},
        "계란": {"expiry": "냉장 보관 시 약 3~4주", "storage": "씻지 말고 뾰족한 부분이 아래로 향하게 하여 냉장고 안쪽에 보관하세요.", "alternatives": ["메추리알", "두부", "닭가슴살"]},
        "파스타 면": {"expiry": "개봉 후 건조한 곳에서 약 1년", "storage": "밀폐용기에 담아 직사광선이 없는 서늘하고 건조한 곳에 보관하세요.", "alternatives": ["소면", "우동 면", "라면 사리", "당면"]},
        "소시지": {"expiry": "개봉 후 냉장 3~5일 (미개봉 시 제품 표기일 참고)", "storage": "밀폐용기나 지퍼백에 밀봉하여 냉장 보관하고, 오래 두고 먹으려면 냉동 보관하세요.", "alternatives": ["햄", "베이컨", "스팸", "닭가슴살", "돼지고기"]},
        "냉동 새우": {"expiry": "냉동 보관 시 약 3~6개월", "storage": "밀봉하여 냉동실 깊은 곳에 보관하고, 요리 전에는 찬물에 담가 해동하세요.", "alternatives": ["소시지", "닭가슴살", "오징어", "어묵"]}
    }

if "custom_ingredients" not in st.session_state:
    st.session_state.custom_ingredients = []

# 자동 유통기한 예측 시스템 함수
def get_automatic_info(name):
    if any(k in name for k in ["고기", "삼겹살", "소", "돼지", "닭"]):
        return {"expiry": "냉장 1~3일 / 냉동 보관 시 3~6개월 내외", "storage": "핏물을 닦고 식용유를 발라 밀폐용기에 담아 보관하세요.", "alternatives": ["소시지", "햄", "두부"]}
    else:
        return {"expiry": "냉장 보관 시 일반적으로 3~7일 내외 권장", "storage": "지퍼백에 담아 외부 공기를 차단한 후 냉장 보관하세요.", "alternatives": ["두부", "계란", "양배추"]}

# 기능 1: 없는 재료 직접 입력창
st.subheader("➕ 없는 재료 직접 입력하기")
with st.form(key="add_ingredient_form", clear_on_submit=True):
    user_input = st.text_input("새로운 재료 이름을 입력하세요", placeholder="여기에 입력...")
    submit_btn = st.form_submit_button("냉장고에 추가")
    if submit_btn and user_input.strip():
        clean_input = user_input.strip()
        if clean_input not in st.session_state.custom_ingredients and clean_input not in st.session_state.ingredients_db:
            st.session_state.ingredients_db[clean_input] = get_automatic_info(clean_input)
            st.session_state.custom_ingredients.append(clean_input)
            st.toast(f"✅ '{clean_input}' 등록 완료!")

# 기능 2: 냉장고 재료 선택 체크박스
st.subheader("🧺 우리 집 냉장고 재료 선택")
selected_ingredients = []
all_checkbox_ingredients = list(st.session_state.ingredients_db.keys())
cols = st.columns(4)
for idx, ing in enumerate(all_checkbox_ingredients):
    with cols[idx % 4]:
        if st.checkbox(ing, key=f"check_{ing}"):
            selected_ingredients.append(ing)

st.divider()

# 기능 3: 유통기한 정보 즉시 표출
if selected_ingredients:
    st.subheader("💡 선택한 재료 맞춤 가이드")
    for ing in selected_ingredients:
        info = st.session_state.ingredients_db.get(ing, get_automatic_info(ing))
        st.markdown(f"### 🔍 {ing} 안내 정보")
        st.info(f"📅 **추천 유통기한:** {info['expiry']}\n\n📦 **권장 보관 방법:** {info['storage']}\n\n🔄 **대체재:** {', '.join(info['alternatives'])}")
    st.divider()

# 기능 4: 블로그 탭 필터링이 주입된 실시간 레시피 링크 연동 엔진
st.subheader("🍽️ 실시간 인터넷 검색 레시피 결과")
if selected_ingredients:
    keyword_text = " ".join(selected_ingredients) + " 레시피"
    
    # 🌟 [핵심 수정] 네이버 통합검색이 아닌 '블로그 탭' 전용 파라미터(where=blog)를 안전하게 인코딩 결합했습니다.
    params = {"where": "blog", "query": keyword_text}
    yt_params = {"search_query": keyword_text}
    
    naver_url = f"https://naver.com?{urllib.parse.urlencode(params)}"
    youtube_url = f"https://youtube.com?{urllib.parse.urlencode(yt_params)}"
    
    st.write(f"✨ **[{', '.join(selected_ingredients)}]** 조합 레시피를 검색할 준비가 되었습니다.")
    st.write("아래 버튼을 누르면 네이버 블로그 레시피 검색 탭과 유튜브 동영상 목록으로 각각 안전하게 이동합니다.")
    st.write("")
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.link_button("💚 네이버 블로그 레시피 보기", naver_url, use_container_width=True)
    with btn_col2:
        st.link_button("❤️ 유튜브 요리 영상 보기", youtube_url, use_container_width=True)
else:
    st.info("상단의 냉장고 재료를 체크하시면 실시간 블로그 및 유튜브 황금 레시피 검색기가 활성화됩니다!")
