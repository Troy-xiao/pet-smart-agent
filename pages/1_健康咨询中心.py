import streamlit as st
import plotly.graph_objects as go
from utils.agent_core import chat_with_agent

st.set_page_config(page_title="健康咨询中心", page_icon="🩺", layout="wide")

# 页面标题与介绍
st.title("🩺 宠物健康咨询中心")
st.caption("基于专业宠物医疗知识库的AI智能咨询，支持症状初筛、风险分级、多轮对话，为您的爱宠健康保驾护航")
st.divider()

# 初始化会话状态
if "health_messages" not in st.session_state:
    st.session_state.health_messages = []
if "use_web_search" not in st.session_state:
    st.session_state.use_web_search = False

# 侧边栏功能区
with st.sidebar:
    st.header("⚙️ 功能设置")
    st.session_state.use_web_search = st.checkbox("开启联网搜索增强", value=st.session_state.use_web_search)
    st.caption("开启后将结合京东云智能搜索补充实时资讯")
    
    st.divider()
    
    if st.button("🆕 新建对话", use_container_width=True, type="primary"):
        st.session_state.health_messages = []
        st.rerun()
    
    st.divider()
    st.subheader("💡 快速提问示例")
    quick_questions = [
        "猫咪呕吐了一次，精神正常怎么办？",
        "狗狗拉稀带血，很臭，精神差",
        "猫咪一直打喷嚏流黄鼻涕",
        "狗狗不能吃什么食物？"
    ]
    for q in quick_questions:
        if st.button(q, use_container_width=True):
            st.session_state.health_messages.append({"role": "user", "content": q})
            resp = chat_with_agent(q, st.session_state.health_messages[:-1], st.session_state.use_web_search)
            st.session_state.health_messages.append({"role": "assistant", "content": resp})
            st.rerun()

# 主体布局：对话区 + 风险评估区
col_chat, col_risk = st.columns([2, 1])

with col_chat:
    st.subheader("💬 对话咨询")
    # 对话记录展示区（在上）
    chat_container = st.container(height=500)
    with chat_container:
        if not st.session_state.health_messages:
            st.info("👋 您好，请描述宠物的症状、品种、年龄等信息，我会为您提供专业的健康建议。")
        else:
            for msg in st.session_state.health_messages:
                with st.chat_message(msg["role"]):
                    if isinstance(msg["content"], dict):
                        st.markdown(msg["content"]["answer"])
                    else:
                        st.write(msg["content"])
    
    # 输入框（天然固定在底部，符合大众聊天习惯）
    user_input = st.chat_input("请描述宠物的症状、品种、年龄...")
    if user_input:
        st.session_state.health_messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)
            
            with st.chat_message("assistant"):
                with st.status("🧠 AI思考中...", expanded=True):
                    st.write("🔍 正在检索专业知识库...")
                    st.write("🤖 正在生成诊疗建议...")
                    response = chat_with_agent(
                        user_input, 
                        st.session_state.health_messages[:-1], 
                        st.session_state.use_web_search
                    )
                    st.write("✅ 回答生成完成")
                st.markdown(response["answer"])
        
        st.session_state.health_messages.append({"role": "assistant", "content": response})
        st.rerun()

with col_risk:
    st.subheader("📈 健康风险评估")
    if st.session_state.health_messages and isinstance(st.session_state.health_messages[-1]["content"], dict):
        last_resp = st.session_state.health_messages[-1]["content"]
        risk = last_resp["risk_level"]
        
        # 风险等级仪表盘
        risk_score = {"低风险": 30, "中风险": 65, "高风险": 90}.get(risk, 0)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={'text': "健康风险指数"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgreen"},
                    {'range': [40, 75], 'color': "gold"},
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': risk_score
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("当前风险等级", risk)
        st.caption("⚠️ 风险评估仅供参考，身体异常请及时就医")
    else:
        st.info("描述宠物症状后，此处将自动展示健康风险评估结果")
