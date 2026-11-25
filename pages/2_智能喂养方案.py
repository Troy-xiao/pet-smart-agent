import streamlit as st
from utils.agent_core import generate_feeding_plan

st.set_page_config(page_title="智能喂养方案", page_icon="🥣", layout="centered")

st.title("🥣 定制化智能喂养方案")
st.caption("基于宠物品种、年龄、体重等多维度信息，AI生成专属科学喂养计划，涵盖喂食量、营养需求、饮食禁忌全方面指导")
st.divider()

with st.form("feeding_form"):
    col1, col2 = st.columns(2)
    with col1:
        pet_type = st.selectbox("宠物类型", ["狗狗", "猫咪"])
        breed = st.text_input("品种", placeholder="例如：金毛、英短蓝猫")
    with col2:
        age = st.text_input("年龄", placeholder="例如：2岁、3个月")
        weight = st.text_input("体重", placeholder="例如：10kg、4kg")
    
    submitted = st.form_submit_button("生成专属喂养方案", type="primary")

if submitted and breed and age and weight:
    with st.status("🥣 正在生成定制化喂养方案...", expanded=True):
        st.write("📊 正在分析宠物基础信息...")
        st.write("🥩 正在匹配营养需求标准...")
        st.write("📝 正在生成完整喂养建议...")
        result = generate_feeding_plan(pet_type, breed, age, weight)
    
    st.divider()
    st.subheader("📋 专属喂养方案")
    st.markdown(result)
    st.caption("💡 以上方案为通用建议，特殊体质宠物请遵医嘱")
elif submitted:
    st.warning("请完整填写宠物信息，以便生成精准方案")
