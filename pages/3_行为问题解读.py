import streamlit as st
from utils.agent_core import analyze_behavior

st.set_page_config(page_title="行为问题解读", page_icon="🧠", layout="centered")

st.title("🧠 宠物行为问题解读")
st.caption("AI深度分析宠物行为成因，提供科学、可落地的矫正方案与改善建议，帮助您建立更和谐的人宠关系")
st.divider()

with st.form("behavior_form"):
    pet_type = st.selectbox("宠物类型", ["狗狗", "猫咪"])
    behavior_desc = st.text_area(
        "请详细描述具体行为问题",
        placeholder="例如：我家狗狗每天出门都爆冲，拉不住怎么办？\n猫咪最近总乱尿，猫砂盆也清理了还是没用",
        height=120
    )
    submitted = st.form_submit_button("分析并给出矫正方案", type="primary")

if submitted and behavior_desc:
    with st.status("🧠 正在分析行为成因...", expanded=True):
        st.write("🔍 正在匹配行为学知识库...")
        st.write("📝 正在生成针对性矫正方案...")
        result = analyze_behavior(behavior_desc, pet_type)
    
    st.divider()
    st.subheader("🔍 行为分析与矫正方案")
    st.markdown(result)
    st.caption("💡 行为矫正需要耐心坚持，严重行为问题建议咨询专业训宠师")
elif submitted:
    st.warning("请描述具体的行为问题，以便精准分析")
