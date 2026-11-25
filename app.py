import streamlit as st
from utils.config import ACCESS_PASSWORD

# 页面基础配置
st.set_page_config(
    page_title="宠智通 - 全场景智慧养宠AI助手",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 自定义侧边栏导航（解决app改首页 + 新增互动模块） ==========
pg = st.navigation([
    st.Page("app.py", title="首页", icon="🏠", default=True),
    st.Page("pages/1_健康咨询中心.py", title="健康咨询中心", icon="🩺"),
    st.Page("pages/2_智能喂养方案.py", title="智能喂养方案", icon="🥣"),
    st.Page("pages/3_行为问题解读.py", title="行为问题解读", icon="🧠"),
    st.Page("pages/4_应急处置助手.py", title="应急处置助手", icon="🚨"),
    st.Page("pages/5_互动体验中心.py", title="互动体验中心", icon="🎮"),
])

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

# ========== 首页主体内容 ==========
st.title("🐾 欢迎使用宠智通")
st.subheader("全场景智慧养宠AI智能体")
st.caption("基于京东云大模型与检索增强技术，覆盖健康、喂养、行为、应急、互动全场景，为养宠人群提供专业、便捷的一站式AI服务")

st.divider()

# 第一行：3个核心功能卡片（等高对齐）
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True, height=320):
        st.markdown("### 🩺 健康咨询中心")
        st.write("基于专业宠物医疗知识库，提供症状分级初筛、疾病科普、用药安全提醒、就医建议分级，精准评估健康风险。")
        st.markdown("**核心能力**")
        st.markdown("- 三级风险自动评估\n- 专业知识库检索\n- 多轮对话记忆")
        if st.button("前往使用 →", key="btn_health", use_container_width=True):
            st.switch_page("pages/1_健康咨询中心.py")

with col2:
    with st.container(border=True, height=320):
        st.markdown("### 🥣 智能喂养方案")
        st.write("根据宠物品类、品种、年龄、体重四大维度，生成定制化喂养计划，包含喂食量、主粮选择、饮食禁忌与换粮指导。")
        st.markdown("**核心能力**")
        st.markdown("- 个性化方案生成\n- 全品类饮食禁忌\n- 分阶段喂养建议")
        if st.button("前往使用 →", key="btn_feeding", use_container_width=True):
            st.switch_page("pages/2_智能喂养方案.py")

with col3:
    with st.container(border=True, height=320):
        st.markdown("### 🧠 行为问题解读")
        st.write("针对拆家、乱叫、应激、乱尿等常见行为问题，深度分析成因，提供可落地的矫正方案与改善建议。")
        st.markdown("**核心能力**")
        st.markdown("- 多维度成因分析\n- 实操性矫正方案\n- 应激应对指南")
        if st.button("前往使用 →", key="btn_behavior", use_container_width=True):
            st.switch_page("pages/3_行为问题解读.py")

# 第二行：3个功能卡片（等高对齐，新增互动体验中心）
col4, col5, col6 = st.columns(3)

with col4:
    with st.container(border=True, height=280):
        st.markdown("### 🚨 应急处置助手")
        st.write("覆盖误食、中暑、外伤、窒息四大高频紧急场景，提供标准化分步处置流程，争分夺秒保障宠物生命安全。")
        st.markdown("**核心能力**")
        st.markdown("- 分步操作指南\n- 风险事项提醒\n- 就医前置建议")
        if st.button("前往使用 →", key="btn_emergency", use_container_width=True):
            st.switch_page("pages/4_应急处置助手.py")

with col5:
    with st.container(border=True, height=280):
        st.markdown("### 🌐 联网知识增强")
        st.write("对接京东云智能搜索能力，可实时检索最新养宠资讯、用品测评、行业规范，补充本地知识库的时效性内容。")
        st.markdown("**使用方式**")
        st.markdown("在健康咨询中心侧边栏开启「联网搜索增强」即可使用")

with col6:
    with st.container(border=True, height=280):
        st.markdown("### 🎮 互动体验中心")
        st.write("3D可交互动物模型 + 人宠语言互译演示，探索AI跨物种交互创新形态，兼具科技感与趣味性。")
        st.markdown("**核心能力**")
        st.markdown("- 3D模型旋转缩放\n- 双向语言翻译演示\n- 五大动物大类")
        if st.button("前往体验 →", key="btn_interact", use_container_width=True):
            st.switch_page("pages/5_互动体验中心.py")

st.divider()

st.subheader("📊 技术架构说明")
col_tech1, col_tech2, col_tech3, col_tech4 = st.columns(4)
with col_tech1:
    st.info("**大模型底座**\n\n京东云 GLM-5.1 大模型，负责自然语言推理与内容生成")
with col_tech2:
    st.success("**知识检索系统**\n\n本地向量知识库，覆盖四大模块专业养宠内容")
with col_tech3:
    st.warning("**搜索增强能力**\n\n京东云智能搜索API，支持实时联网信息补充")
with col_tech4:
    st.error("**前端交互层**\n\nStreamlit 多页面可视化架构，轻量化易访问")

# 运行导航
pg.run()



# import streamlit as st
# from utils.config import ACCESS_PASSWORD

# # 页面基础配置
# st.set_page_config(
#     page_title="宠智通 - 全场景智慧养宠AI助手",
#     page_icon="🐾",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ========== 自定义侧边栏导航（解决app改首页的问题） ==========
# pg = st.navigation([
#     st.Page("app.py", title="首页", icon="🏠", default=True),
#     st.Page("pages/1_健康咨询中心.py", title="健康咨询中心", icon="🩺"),
#     st.Page("pages/2_智能喂养方案.py", title="智能喂养方案", icon="🥣"),
#     st.Page("pages/3_行为问题解读.py", title="行为问题解读", icon="🧠"),
#     st.Page("pages/4_应急处置助手.py", title="应急处置助手", icon="🚨"),
# ])

# # 密码验证
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if not st.session_state.authenticated:
#     st.markdown("# 🐾 宠智通 - 智慧养宠AI智能体")
#     st.caption("第二届全国人工智能应用创新大赛参赛作品 | 消费民生领域")
#     st.divider()
    
#     st.subheader("评审访问验证")
#     password = st.text_input("请输入访问密码", type="password")
#     if st.button("进入系统", type="primary", key="btn_login"):
#         if password == ACCESS_PASSWORD:
#             st.session_state.authenticated = True
#             st.rerun()
#         else:
#             st.error("密码错误，请重试")
#     st.stop()

# # ========== 首页主体内容 ==========
# st.title("🐾 欢迎使用宠智通")
# st.subheader("全场景智慧养宠AI智能体")
# st.caption("基于京东云大模型与检索增强技术，覆盖健康、喂养、行为、应急全场景，为养宠人群提供专业、便捷的一站式AI服务")

# st.divider()

# # 第一行：3个核心功能卡片（等高对齐）
# col1, col2, col3 = st.columns(3)

# with col1:
#     with st.container(border=True, height=320):
#         st.markdown("### 🩺 健康咨询中心")
#         st.write("基于专业宠物医疗知识库，提供症状分级初筛、疾病科普、用药安全提醒、就医建议分级，精准评估健康风险。")
#         st.markdown("**核心能力**")
#         st.markdown("- 三级风险自动评估\n- 专业知识库检索\n- 多轮对话记忆")
#         if st.button("前往使用 →", key="btn_health", use_container_width=True):
#             st.switch_page("pages/1_健康咨询中心.py")

# with col2:
#     with st.container(border=True, height=320):
#         st.markdown("### 🥣 智能喂养方案")
#         st.write("根据宠物品类、品种、年龄、体重四大维度，生成定制化喂养计划，包含喂食量、主粮选择、饮食禁忌与换粮指导。")
#         st.markdown("**核心能力**")
#         st.markdown("- 个性化方案生成\n- 全品类饮食禁忌\n- 分阶段喂养建议")
#         if st.button("前往使用 →", key="btn_feeding", use_container_width=True):
#             st.switch_page("pages/2_智能喂养方案.py")

# with col3:
#     with st.container(border=True, height=320):
#         st.markdown("### 🧠 行为问题解读")
#         st.write("针对拆家、乱叫、应激、乱尿等常见行为问题，深度分析成因，提供可落地的矫正方案与改善建议。")
#         st.markdown("**核心能力**")
#         st.markdown("- 多维度成因分析\n- 实操性矫正方案\n- 应激应对指南")
#         if st.button("前往使用 →", key="btn_behavior", use_container_width=True):
#             st.switch_page("pages/3_行为问题解读.py")

# # 第二行：2个功能卡片（等高对齐）
# col4, col5 = st.columns(2)

# with col4:
#     with st.container(border=True, height=280):
#         st.markdown("### 🚨 应急处置助手")
#         st.write("覆盖误食、中暑、外伤、窒息四大高频紧急场景，提供标准化分步处置流程，争分夺秒保障宠物生命安全。")
#         st.markdown("**核心能力**")
#         st.markdown("- 分步操作指南\n- 风险事项提醒\n- 就医前置建议")
#         if st.button("前往使用 →", key="btn_emergency", use_container_width=True):
#             st.switch_page("pages/4_应急处置助手.py")

# with col5:
#     with st.container(border=True, height=280):
#         st.markdown("### 🌐 联网知识增强")
#         st.write("对接京东云智能搜索能力，可实时检索最新养宠资讯、用品测评、行业规范，补充本地知识库的时效性内容。")
#         st.markdown("**使用方式**")
#         st.markdown("在健康咨询中心侧边栏开启「联网搜索增强」即可使用")

# st.divider()

# st.subheader("📊 技术架构说明")
# col_tech1, col_tech2, col_tech3, col_tech4 = st.columns(4)
# with col_tech1:
#     st.info("**大模型底座**\n\n京东云 GLM-5.1 大模型，负责自然语言推理与内容生成")
# with col_tech2:
#     st.success("**知识检索系统**\n\n本地TF-IDF向量知识库，覆盖四大模块专业养宠内容")
# with col_tech3:
#     st.warning("**搜索增强能力**\n\n京东云智能搜索API，支持实时联网信息补充")
# with col_tech4:
#     st.error("**前端交互层**\n\nStreamlit 多页面可视化架构，轻量化易访问")

# # 运行导航
# pg.run()
