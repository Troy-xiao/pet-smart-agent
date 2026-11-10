import streamlit as st
from utils.config import ACCESS_PASSWORD

# 页面配置
st.set_page_config(
    page_title="宠智通 - 全场景智慧养宠AI助手",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 密码验证
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("# 🐾 宠智通 - 智慧养宠AI智能体")
    st.caption("第二届全国人工智能应用创新大赛参赛作品 | 消费民生领域")
    st.divider()
    
    st.subheader("评审访问验证")
    password = st.text_input("请输入访问密码", type="password")
    if st.button("进入系统", type="primary", key="btn_login"):
        if password == ACCESS_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("密码错误，请重试")
    st.stop()

# 首页内容
st.title("🐾 欢迎使用宠智通")
st.caption("基于京东云大模型与智能搜索的全场景智慧养宠AI助手")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 🩺 健康咨询中心\n症状初筛、疾病科普、用药安全、就医建议分级")
    if st.button("前往使用 →", key="btn_health", use_container_width=True):
        st.switch_page("pages/1_健康咨询中心.py")

with col2:
    st.success("### 🥣 智能喂养方案\n定制化喂养计划、饮食禁忌、换粮指导")
    if st.button("前往使用 →", key="btn_feeding", use_container_width=True):
        st.switch_page("pages/2_智能喂养方案.py")

with col3:
    st.warning("### 🧠 行为问题解读\n拆家、乱叫、应激、乱尿等问题分析与矫正")
    if st.button("前往使用 →", key="btn_behavior", use_container_width=True):
        st.switch_page("pages/3_行为问题解读.py")

col4, col5 = st.columns(2)

with col4:
    st.error("### 🚨 应急处置助手\n误食、中暑、外伤、窒息等紧急场景分步指南")
    if st.button("前往使用 →", key="btn_emergency", use_container_width=True):
        st.switch_page("pages/4_应急处置助手.py")

with col5:
    st.info("### 🌐 联网知识问答\n实时检索最新养宠资讯、用品测评、政策规范")
    st.caption("在健康咨询中心开启「联网搜索增强」即可使用")

st.divider()

st.subheader("📊 技术架构说明")
st.markdown("""
- **大模型底座**：京东云大模型 GLM-5.1，负责自然语言推理与生成
- **知识底座**：本地FAISS向量知识库，覆盖医疗、喂养、行为、急救全场景专业内容
- **搜索增强**：京东云智能搜索API，支持实时联网信息补充
- **交互界面**：Streamlit 多页面可视化架构，操作简洁直观
""")
