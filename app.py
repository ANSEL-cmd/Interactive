import streamlit as st
from datetime import date

# 内置ASCII像素宠物头像，没有版权问题
pixel_avatars = {
    "Pixel Cat": r"""
 /\_/\
( o.o )
 > ^ <
""",
    "Pixel Dog": r"""
  /^ ^\
 / o o \
|   ω   |
 \     /
  \___/
""",
    "Pixel Rabbit": r"""
  /\     /\
 {  o   o  }
 {    ^    }
  \       /
   \___/
"""
}

# 初始化存储记录（刷新页面数据就清空，我们在文档里写明这个限制）
if "vaccine_records" not in st.session_state:
    st.session_state.vaccine_records = []

st.title("🐾 Pet Vaccine Record Log")
st.subheader("Log your pet's vaccination information")
st.divider()

# ====== 表单区域：用户输入 ======
st.markdown("### Add a new vaccine record")
pet_name = st.text_input("Pet name")
vaccine_name = st.text_input("Vaccine name e.g. Rabies, Feline Triple")
inject_date = st.date_input("Vaccination date")
selected_avatar = st.selectbox("Pick a pixel avatar for your pet", list(pixel_avatars.keys()))

add_button = st.button("✅ Add Record")

# 提交表单 + 错误校验（处理空输入，作业要求的错误处理）
if add_button:
    pet_name_clean = pet_name.strip()
    vaccine_clean = vaccine_name.strip()
    if not pet_name_clean:
        st.warning("⚠️ Pet name cannot be empty! Please fill in the pet name.")
    elif not vaccine_clean:
        st.warning("⚠️ Vaccine name cannot be empty!")
    else:
        new_item = {
            "pet_name": pet_name_clean,
            "vaccine": vaccine_clean,
            "inject_day": inject_date,
            "avatar": selected_avatar
        }
        st.session_state.vaccine_records.append(new_item)
        st.success("🎉 New vaccine record saved!")

st.divider()

# ====== 展示所有记录 + 到期判断 ======
st.markdown("### 📋 All Vaccine Records")
all_records = st.session_state.vaccine_records

if len(all_records) == 0:
    st.info("No vaccine records yet. Add your first record above!")
else:
    for idx, rec in enumerate(all_records):
        st.code(pixel_avatars[rec["avatar"]])
        st.write(f"**Pet:** {rec['pet_name']}")
        st.write(f"**Vaccine:** {rec['vaccine']}")
        st.write(f"Vaccinated on: {rec['inject_day']}")

        days = (date.today() - rec["inject_day"]).days
        if days > 365:
            st.error(f"Status: Expired! ({days} days since injection)")
        elif days > 330:
            st.warning(f"Status: Coming due soon! ({days} days since injection)")
        else:
            st.success(f"Status: Valid! ({days} days since injection)")

        delete_btn_key = f"del{idx}"
        if st.button(f"🗑️ Delete this record", key=delete_btn_key):
            st.session_state.vaccine_records.pop(idx)
            st.rerun()
        st.divider()

# 一键清空全部记录
if st.button("🗑️ Reset ALL records"):
    st.session_state.vaccine_records = []
    st.rerun()
