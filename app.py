import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
from io import BytesIO

# 页面配置 + 极简便签CSS
st.set_page_config(
    page_title="Pet Vaccine Record Log",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 全局底色：奶油米便签纸底色 */
    .stApp {
        background-color: #F8F6ED;
        background-attachment: fixed;
        font-family: "Segoe UI", "PingFang SC", sans-serif;
        color: #648890;
    }

    .block-container {
        padding-top: 24px;
        padding-bottom: 40px;
    }

    h1 {
        color: #527880;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    h2, h3, h4 {
        color: #648890;
        font-weight: 500;
    }

    /* ===== 核心：宠物独立便签卡片 ===== */
    .memo-card {
        background-color: #FCFBF7;
        border: 1.2px solid #C8D9DC;
        border-radius: 14px;
        padding: 18px 20px;
        margin: 14px 0;
    }

    /* 输入框、选择框、日期框 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div {
        background-color: #FCFBF7;
        border: 1.2px solid #C8D9DC;
        border-radius: 12px;
        color: #648890;
    }

    /* 按钮配色：浅豆绿 */
    .stButton > button {
        background-color: #D2E0CC;
        border: 1px solid #B9CBB0;
        border-radius: 12px;
        color: #48686E;
        font-weight: 500;
        padding: 9px 20px;
        box-shadow: none;
        transition: 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #C4D4BC;
    }

    .stRadio > div {
        background-color: #FCFBF7;
        border-radius: 12px;
        padding: 8px;
        border: 1.2px solid #C8D9DC;
    }
    .stRadio label {
        color: #648890;
    }

    .stAlert {
        border-radius: 12px;
    }
    .stAlert[data-testid="stAlertContainer"] {
        background-color: #F1F4EE;
    }

    hr {
        border: none;
        border-top: 1.2px solid #C8D9DC;
        margin-top: 22px;
        margin-bottom: 22px;
    }

    .stCode {
        background-color: #FCFBF7;
        border: 1.2px solid #C8D9DC;
        color: #648890;
    }

    /* 下载按钮：浅灰蓝 */
    .stDownloadButton > button {
        background-color: #D6E1E8;
        border: 1px solid #B8C8D0;
        color: #48686E;
        border-radius: 12px;
        box-shadow: none;
    }
    .stDownloadButton > button:hover {
        background-color: #C9D7DF;
    }

    /* 疫苗状态标签 */
    .tag-valid {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 8px;
        background: #D2E0CC;
        color: #48686E;
        font-size: 0.85em;
    }
    .tag-soon {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 8px;
        background: #F2E9D8;
        color: #7A684E;
        font-size: 0.85em;
    }
    .tag-expired {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 8px;
        background: #E4D9DC;
        color: #705860;
        font-size: 0.85em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

pixel_avatars = {
    "Cat": r"""
      /\_/\
 =( °w° )=
   )   (
  /     \
 |  __  |
  \____/
""",
    "Dog": r"""
        / \__
       (    @\___
       /         O
      /   (_____/
     /_____/
""",
    "Rabbit": r"""
        /\   /\
       /  \ /  \
      /   * *   \
     /     ^     \
    /             \
   /_______________\
""",
    "Hamster": r"""
      .--.
     |o_o |
     |:_/ |
    //   \ \
   (|     | )
  /'\_   _/'\
  \___)=(___/
""",
    "Fox": r"""
       /\_/\
      / ^ ^ \
     >   ^   <
     \  w w  /
      \__U__/
""",
    "Owl": r"""
       ,_,
      (o o)
     =( V )=
      /   \
     /|   |\
    ||     ||
"""
}

if "pet_data" not in st.session_state:
    st.session_state.pet_data = {}
if "vaccine_row_count" not in st.session_state:
    st.session_state.vaccine_row_count = 1

st.title("🐾 Pet Vaccine Record Log")
st.subheader("Add vaccines for existing pets or register a new pet")
st.divider()

pet_list = list(st.session_state.pet_data.keys())
mode = st.radio("Select mode", ["Register new pet", "Add vaccine to existing pet"], horizontal=True)

selected_pet_name = ""
pet_avatar = "Cat"

if mode == "Register new pet":
    pet_name = st.text_input("Pet name")
    pet_avatar = st.radio("Pick a pet avatar", list(pixel_avatars.keys()), horizontal=True)
else:
    if pet_list:
        selected_pet_name = st.selectbox("Choose existing pet", pet_list)
        pet_avatar = st.session_state.pet_data[selected_pet_name]["avatar"]
        st.markdown(f"Avatar: {pet_avatar}")
        st.code(pixel_avatars[pet_avatar])
    else:
        st.info("No pets yet, please register a new pet first.")

st.markdown("### 💉 New vaccination entries")
vaccine_inputs = []
for i in range(st.session_state.vaccine_row_count):
    cols = st.columns([2, 2])
    with cols[0]:
        vac_name = st.text_input(f"Vaccine {i+1} name", key=f"vac_name_{i}")
    with cols[1]:
        vac_date = st.date_input(f"Vaccine {i+1} date", key=f"vac_date_{i}")
    vaccine_inputs.append({"vac_name": vac_name.strip(), "vac_date": vac_date})

if st.button("➕ Add another vaccine row"):
    st.session_state.vaccine_row_count += 1
    st.rerun()

submit_btn = st.button("✅ Save these vaccine records")
if submit_btn:
    if mode == "Register new pet":
        pet_name_clean = pet_name.strip()
        if not pet_name_clean:
            st.warning("⚠️ Please fill in pet name!")
        else:
            if pet_name_clean in st.session_state.pet_data:
                st.warning("⚠️ This pet already exists, switch to 'Add vaccine to existing pet'")
            else:
                new_vaccines = []
                for item in vaccine_inputs:
                    if item["vac_name"]:
                        new_vaccines.append({"vac": item["vac_name"], "date": item["vac_date"]})
                if new_vaccines:
                    st.session_state.pet_data[pet_name_clean] = {
                        "avatar": pet_avatar,
                        "vaccines": new_vaccines
                    }
                    st.success(f"🎉 Registered {pet_name_clean} with {len(new_vaccines)} vaccine(s)")
                    st.session_state.vaccine_row_count = 1
                    st.rerun()
                else:
                    st.warning("⚠️ No valid vaccine info")
    else:
        if not pet_list:
            st.warning("⚠️ No existing pet available")
        else:
            add_vacs = []
            for item in vaccine_inputs:
                if item["vac_name"]:
                    add_vacs.append({"vac": item["vac_name"], "date": item["vac_date"]})
            if add_vacs:
                st.session_state.pet_data[selected_pet_name]["vaccines"].extend(add_vacs)
                st.success(f"🎉 Added {len(add_vacs)} vaccine(s) to {selected_pet_name}")
                st.session_state.vaccine_row_count = 1
                st.rerun()
            else:
                st.warning("⚠️ No valid vaccine info")

st.divider()
st.markdown("### 📋 All Pet Records — Each as a memo note")
pet_data = st.session_state.pet_data

if not pet_data:
    st.info("No pets and vaccine records yet.")
else:
    # 循环：每一只宠物 = 一张独立便签卡片
    for p_name, info in pet_data.items():
        st.markdown('<div class="memo-card">', unsafe_allow_html=True)
        st.markdown(f"#### {p_name}")
        st.code(pixel_avatars[info["avatar"]])
        vac_list = info["vaccines"]
        for vac in vac_list:
            days = (date.today() - vac["date"]).days
            if days > 365:
                tag = '<span class="tag-expired">Expired</span>'
            elif days > 330:
                tag = '<span class="tag-soon">Coming due soon</span>'
            else:
                tag = '<span class="tag-valid">Valid</span>'
            st.markdown(f"- {vac['vac']} | {vac['date']} &nbsp; {tag}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("📷 Export all records as PNG image"):
        fig, ax = plt.subplots(figsize=(10, len(pet_data)*2.4))
        ax.axis("off")
        y = len(pet_data) - 0.3
        for p_name, info in pet_data.items():
            text_lines = [f"【{p_name}】"]
            for vac in info["vaccines"]:
                days = (date.today() - vac["date"]).days
                if days > 365:
                    status = "Expired"
                elif days > 330:
                    status = "Coming due soon"
                else:
                    status = "Valid"
                text_lines.append(f" - {vac['vac']} | {vac['date']} | {status}")
            full_text = "\n".join(text_lines)
            ax.text(0.18, y, full_text, fontsize=11, va="top", color="#527880")
            y -= 2
        buf = BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", facecolor="#F8F6ED")
        buf.seek(0)
        st.download_button(
            label="✅ Download PNG",
            data=buf,
            file_name="pet_vaccine_memo.png",
            mime="image/png"
        )
        plt.close(fig)

if st.button("🗑️ Clear all pets & records"):
    st.session_state.pet_data = {}
    st.session_state.vaccine_row_count = 1
    st.rerun()

# 底部极简装饰
st.markdown(
    """
    <div style="text-align:center; margin-top:30px; color:#B9CBB0; font-size:20px;">
        ˚ ✧ ˚
    </div>
    """,
    unsafe_allow_html=True
)
