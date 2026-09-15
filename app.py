import streamlit as st

# 1. 웹 페이지 기본 설정 및 깔끔한 화이트 톤 스타일링
st.set_page_config(page_title="스마트 냉장고 레시피 마스터", page_icon="🍳", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1 { color: #111111; font-family: 'Malgun Gothic', sans-serif; font-weight: 700; }
    h2, h3 { color: #222222; font-family: 'Malgun Gothic', sans-serif; }
    .stAlert { border-radius: 10px; border: 1px solid #e0e0e0; }
    div.stButton > button:first-child {
        background-color: #222222; color: white; border-radius: 6px; border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #444444; color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 식재료 정보 사전 (유통기한, 보관법, 대체재)
if "ingredients_db" not in st.session_state:
    st.session_state.ingredients_db = {
        "양배추": {"expiry": "냉장 보관 시 약 2~3주", "storage": "심지를 파내고 물에 적신 키친타월을 채운 뒤 랩으로 싸서 냉장 보관하세요.", "alternatives": ["배추", "양상추", "청경채"]},
        "두부": {"expiry": "개봉 후 냉장 2~3일", "storage": "밀폐용기에 두부가 잠길 정도로 찬물을 붓고 소금을 약간 넣어 냉장 보관하세요.", "alternatives": ["연두부", "유부", "버섯"]},
        "계란": {"expiry": "냉장 보관 시 약 3~4주", "storage": "씻지 말고 뾰족한 부분이 아래로 향하게 하여 냉장고 안쪽에 보관하세요.", "alternatives": ["메추리알", "두부"]},
        "파스타 면": {"expiry": "개봉 후 건조한 곳에서 약 1년", "storage": "밀폐용기에 담아 직사광선이 없는 서늘하고 건조한 곳에 보관하세요.", "alternatives": ["소면", "우동 면", "라면 사리"]},
        "냉동 새우": {"expiry": "냉동 보관 시 약 3~6개월", "storage": "밀봉하여 냉동실 깊은 곳에 보관하고, 요리 전에는 찬물에 담가 해동하세요.", "alternatives": ["소시지", "닭가슴살", "오징어"]}
    }

# 직접 추가한 재료들을 임시 기억하기 위한 저장소 설정
if "custom_ingredients" not in st.session_state:
    st.session_state.custom_ingredients = []

# 3. 상세 레시피 데이터베이스 (영상 링크 매칭)
RECIPES = [
    {
        "name": "일본식 양배추 볶음 (덮밥 스타일)",
        "required": ["양배추"],
        "sauces": ["돈까스 소스", "버터", "다진 마늘"],
        "video": "https://www.youtube.com/watch?v=SXEMuVCxFKU",
        "steps": [
            "1. 양배추(약 150g)를 흐르는 물에 깨끗이 씻은 뒤, 먹기 좋은 한 입 크기나 얇은 채 모양으로 썰어 물기를 제거합니다.",
            "2. 달궈진 팬에 버터 1큰술을 두르고 다진 마늘 0.5큰술을 넣어 중불에서 마늘 향이 은은하게 올라올 때까지 볶아줍니다.",
            "3. 썰어둔 양배추를 팬에 전부 넣고, 숨이 살짝 죽어 투명해질 때까지 강불에서 2~3분간 빠르게 볶습니다.",
            "4. 돈까스 소스 1.5~2큰술을 넣고 양배추에 소스 색이 골고루 배도록 가볍게 더 볶아준 뒤 불을 끕니다.",
            "5. 그릇에 따뜻한 밥을 담고 볶아진 양배추를 소스와 함께 얹어 덮밥 형태로 완성합니다. (취향에 따라 통깨나 후추 추가)"
        ]
    },
    {
        "name": "초간단 원팬 새우 알리오 올리오",
        "required": ["파스타 면", "냉동 새우"],
        "sauces": ["후추", "올리브유", "마늘", "치킨스톡"],
        "video": "https://www.youtube.com/watch?v=eaDCOY0xAzY",
        "steps": [
            "1. 냉동 새우 한 줌을 찬물에 5분간 담가 해동한 뒤 키친타월로 물기를 완전히 닦아내고, 통마늘은 편으로 얇게 썰어 준비합니다.",
            "2. 팬에 올리브유를 넉넉히(약 3~4큰술) 두르고 편마늘과 다진 마늘 1스푼을 넣어 약불에서 노릇해질 때까지 볶아 기름에 마늘 향을 냅니다.",
            "3. 마늘이 노릇해지면 해동된 새우를 넣고 새우 표면이 붉은색으로 변할 때까지 중불에서 함께 볶아줍니다.",
            "4. 팬에 물 120ml(약 2/3컵), 삶지 않은 파스타 면(또는 냉동면), 치킨스톡 1/3스푼, 굴소스 0.5스푼을 그대로 넣어줍니다.",
            "5. 국물이 자작하게 줄어들고 면이 알맞게 익을 때까지 약 5분간 휘저으며 끓여준 후, 마지막에 후추와 파슬리를 뿌려 완성합니다."
        ]
    },
    {
        "name": "단백질 폭탄 두부 계란 볶음밥",
        "required": ["두부", "계란"],
        "sauces": ["굴소스", "들기름 또는 참기름"],
        "video": "https://www.youtube.com/watch?v=_hTNQ5pV4nA",
        "steps": [
            "1. 두부 한 모(300g)를 칼 옆면으로 으깬 뒤 가볍게 짜서 수분을 제거하고, 대파는 송송 썰어 준비합니다.",
            "2. 기름을 두르지 않은 마른 팬에 으깬 두부를 먼저 넣고, 중강불에서 고슬고슬해질 때까지 달달 볶아 수분을 완전히 날려줍니다.",
            "3. 수분이 날아간 두부에 다진 파와 올리브유 1큰술을 넣고 파 향이 밸 때까지 함께 볶아줍니다.",
            "4. 팬 가운데에 동그랗게 공간을 만든 뒤 계란 1~2개를 깨트려 넣고 재빨리 저어 스크램블 에그를 만듭니다.",
            "5. 두부와 계란을 섞은 후 굴소스 1큰술을 넣어 간을 맞추고, 불을 끈 뒤 들기름 한 바퀴를 휘둘러 고소하게 마무리합니다."
        ]
    },
    {
        "name": "새우 두부 굴소스 볶음",
        "required": ["냉동 새우", "두부"],
        "sauces": ["굴소스", "버터", "다진 마늘"],
        "video": "https://www.youtube.com/watch?v=6LzYuPiD9zQ",
        "steps": [
            "1. 두부는 한 입 크기의 깍두기 모양(또는 삼각형)으로 썰어 키친타월로 물기를 제거하고 소금, 후추로 밑간을 해둡니다.",
            "2. 냉동 새우는 찬물에 해동한 뒤 물기를 닦아내고, 팬에 버터 1큰술을 둘러 두부를 모든 면이 노릇노릇해지도록 구워 따로 건져둡니다.",
            "3. 두부를 구운 팬에 다진 마늘 0.5큰술과 대파를 넣어 향을 낸 뒤, 준비해 둔 새우를 넣고 탱글하게 익을 때까지 볶습니다.",
            "4. 새우가 익으면 구워둔 두부를 다시 넣고 굴소스 1큰술과 물 2큰술을 부어 소스가 재료에 자작하게 배어들도록 중불에서 졸입니다.",
            "5. 국물이 거의 없어지고 전반적으로 윤기가 돌면 참기름을 살짝 둘러 접시에 예쁘게 담아냅니다."
        ]
    }
]

# 4. 웹 화면 레이아웃 및 기능 구현
st.title("🍳 스마트 냉장고 레시피 마스터")
st.write("우리 집 냉장고에 있는 재료를 조합하여 상세한 전문가 요리법과 가이드 비디오를 확인해 보세요.")
st.divider()

# 기능 1: 재료 직접 입력하여 추가하기 섹션
st.subheader("➕ 없는 재료 직접 입력하기")
with st.form(key="add_ingredient_form", clear_on_submit=True):
    user_input = st.text_input("냉장고에 있는 새로운 재료 이름을 입력하세요 (예: 고기, 닭가슴살, 양파 등)", placeholder="여기에 입력...")
    submit_btn = st.form_submit_button("냉장고에 추가")
    
    if submit_btn and user_input.strip():
        clean_input = user_input.strip()
        if clean_input not in st.session_state.custom_ingredients and clean_input not in st.session_state.ingredients_db:
            st.session_state.custom_ingredients.append(clean_input)
            st.toast(f"✅ '{clean_input}' 재료가 냉장고 리스트에 반영되었습니다!", icon="✨")

# 기능 2: 냉장고 재료 선택 섹션 (기본 제공 재료 + 유저가 입력한 재료 결합)
st.subheader("🧺 우리 집 냉장고 재료 선택")
selected_ingredients = []

# 전체 노출할 재료 리스트 구성
all_checkbox_ingredients = list(st.session_state.ingredients_db.keys()) + st.session_state.custom_ingredients

if all_checkbox_ingredients:
    # 4개의 열로 나누어 깔끔하게 체크박스 배치
    cols = st.columns(4)
    for idx, ing in enumerate(all_checkbox_ingredients):
        with cols[idx % 4]:
            if st.checkbox(ing, key=f"check_{ing}"):
                selected_ingredients.append(ing)
else:
    st.info("선택 가능한 재료가 없습니다.")

st.divider()

# 기능 3: 선택한 재료 가이드 제공 (기본 데이터베이스에 매칭되는 경우만 노출)
if selected_ingredients:
    has_guide = any(ing in st.session_state.ingredients_db for ing in selected_ingredients)
    if has_guide:
        st.subheader("💡 선택한 재료 맞춤 가이드")
        for ing in selected_ingredients:
            if ing in st.session_state.ingredients_db:
                info = st.session_state.ingredients_db[ing]
                with st.expander(f"🔍 {ing} - 유통기한 및 대체재 정보", expanded=False):
                    st.write(f"📅 **추천 유통기한:** {info['expiry']}")
                    st.write(f"📦 **보관 방법:** {info['storage']}")
                    st.write(f"🔄 **없을 때 대체재:** {', '.join(info['alternatives'])}")
        st.divider()

# 기능 4: 업그레이드된 레시피 엔진 및 유튜브 링크 노출
st.subheader("🍽️ 지금 만들 수 있는 추천 요리")

matched_any = False

for recipe in RECIPES:
    can_make = True
    missing_ingredients = []
    used_alternatives = {}
    
    for req in recipe["required"]:
        if req in selected_ingredients:
            continue
        else:
            # 기본 재료 사전(ingredients_db)에 등록된 대체재 목록을 기반으로 매칭 로직 작동
            found_alt = False
            for my_ing in selected_ingredients:
                if my_ing in st.session_state.ingredients_db:
                    if req in st.session_state.ingredients_db[my_ing]["alternatives"]:
                        used_alternatives[req] = my_ing
                        found_alt = True
                        break
            
            if not found_alt:
                can_make = False
                missing_ingredients.append(req)

    # 매칭 성공 시 화면 표시
    if can_make:
        matched_any = True
        title_suffix = ""
        if used_alternatives:
            alt_details = [f"{req} 대신 {my_ing}" for req, my_ing in used_alternatives.items()]
            title_suffix = f" (⚠️ {', '.join(alt_details)} 활용)"
            
        st.success(f"### 🍳 {recipe['name']}{title_suffix}")
        
        # 상세 조리법 단계별 노출
        st.write("**[상세 조리 단계]**")
        for step in recipe["steps"]:
            st.write(step)
            
        if recipe["sauces"]:
            st.caption(f"🧂 **필요한 양념/소스:** {', '.join(recipe['sauces'])}")
            
        # 유튜브 동영상 가이드 링크 제공 구현
        st.markdown(f"📺 **[요리 가이드 영상 보러가기 (YouTube)]({recipe['video']})**")
        st.write("")

if not matched_any:
    st.info("상단의 냉장고 재료를 체크하시면 상세 조리법과 유튜브 가이드 링크가 여기에 나타납니다!")
