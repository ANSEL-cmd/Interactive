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

    .memo-card {
        background-color: #FCFBF7;
        border: 1.2px solid #C8D9DC;
        border-radius: 14px;
        padding: 18px 20px;
        margin: 14px 0;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div {
        background-color: #FCFBF7;
        border: 1.2px solid #C8D9DC;
        border-radius: 12px;
        color: #648890;
    }

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
    .tag-scheduled {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 8px;
        background: #D6E1E8;
        color: #48686E;
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


# [NEW] 统一的疫苗状态判断，页面显示和 PNG 导出共用，避免两处逻辑不一致
def get_status(vac_date):
    today = date.today()
    if vac_date > today:
        return "scheduled"
    days = (today - vac_date).days
    if days > 365:
        return "expired"
    if days > 330:
        return "soon"
    return "valid"


def status_tag(status):
    mapping = {
        "valid": '<span class="tag-valid">Valid</span>',
        "soon": '<span class="tag-soon">Coming due soon</span>',
        "scheduled": '<span class="tag-scheduled">Scheduled</span>',
        "expired": '<span class="tag-expired">Expired</span>',
    }
    return mapping[status]


def status_label(status):
    return {
        "valid": "Valid",
        "soon": "Coming due soon",
        "scheduled": "Scheduled",
        "expired": "Expired",
    }[status]


# session_state 初始化
if "pet_data" not in st.session_state:
    st.session_state.pet_data = {}
if "vaccine_row_count" not in st.session_state:
    st.session_state.vaccine_row_count = 1
# [NEW] 缓存导出的 PNG bytes，避免用户点下载时按钮消失
if "png_bytes" not in st.session_state:
    st.session_state.png_bytes = None

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

# [NEW] 加行 / 减行并排，减行最低保留 1 行
col_add, col_remove = st.columns([1, 1])
with col_add:
    if st.button("➕ Add another vaccine row"):
        st.session_state.vaccine_row_count += 1
        st.rerun()
with col_remove:
    if st.button("➖ Remove last row"):
        if st.session_state.vaccine_row_count > 1:
            last = st.session_state.vaccine_row_count - 1
            # 清掉对应 key，避免下次加行时残留旧输入
            st.session_state.pop(f"vac_name_{last}", None)
            st.session_state.pop(f"vac_date_{last}", None)
            st.session_state.vaccine_row_count -= 1
            st.rerun()
        else:
            st.toast("At least one row is required.", icon="ℹ️")

submit_btn = st.button("✅ Save these vaccine records")
if submit_btn:
    if mode == "Register new pet":
        pet_name_clean = pet_name.strip()
        if not pet_name_clean:
            st.warning("⚠️ Please fill in pet name!")
        elif pet_name_clean in st.session_state.pet_data:
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
                # [FIX] 数据变了，之前缓存的 PNG 作废
                st.session_state.png_bytes = None
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
                st.session_state.png_bytes = None
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
    for p_name, info in pet_data.items():
        st.markdown('<div class="memo-card">', unsafe_allow_html=True)
        st.markdown(f"#### {p_name}")
        # [FIX] 用 <pre> 而不是 st.code，头像更像便签涂鸦而不是代码块
        st.markdown(
            f"<pre style='font-family: monospace; color:#648890; "
            f"background:transparent; border:none; margin:0 0 8px 0;'>"
            f"{pixel_avatars[info['avatar']]}</pre>",
            unsafe_allow_html=True
        )
        for vac in info["vaccines"]:
            status = get_status(vac["date"])
            tag = status_tag(status)
            st.markdown(
                f"- {vac['vac']} | {vac['date']} &nbsp; {tag}",
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # [FIX] 先缓存 PNG bytes，下载按钮独立渲染，点下载不会让按钮消失
    if st.button("📷 Export all records as PNG image"):
        fig, ax = plt.subplots(figsize=(10, len(pet_data) * 2.4))
        ax.axis("off")
        y = len(pet_data) - 0.3
        for p_name, info in pet_data.items():
            text_lines = [f"【{p_name}】"]
            for vac in info["vaccines"]:
                status = status_label(get_status(vac["date"]))
                text_lines.append(f" - {vac['vac']} | {vac['date']} | {status}")
            full_text = "\n".join(text_lines)
            ax.text(0.18, y, full_text, fontsize=11, va="top", color="#527880")
            y -= 2
        buf = BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", facecolor="#F8F6ED")
        plt.close(fig)
        st.session_state.png_bytes = buf.getvalue()

    if st.session_state.png_bytes:
        st.download_button(
            label="✅ Download PNG",
            data=st.session_state.png_bytes,
            file_name="pet_vaccine_memo.png",
            mime="image/png"
        )

# [FIX] 清空操作加二次确认，避免手滑
with st.expander("🗑️ Danger zone"):
    confirm = st.checkbox("I understand this will delete all pets and records.")
    if st.button("Clear all pets & records", disabled=not confirm):
        st.session_state.pet_data = {}
        st.session_state.vaccine_row_count = 1
        st.session_state.png_bytes = None
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