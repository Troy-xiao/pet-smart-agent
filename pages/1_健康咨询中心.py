import streamlit as st
import plotly.graph_objects as go
from utils.agent_core import chat_with_agent, clear_memory

st.set_page_config(page_title="健康咨询中心", page_icon="🩺", layout="wide")
st.title("🩺 宠物健康咨询中心")
st.caption("基于专业知识库的症状初筛与健康建议")

# 侧边栏配置
with st.sidebar:
    st.header("功能设置")
    use_web_search = st.checkbox("开启联网搜索增强", value=False)
    st.caption("开启后将结合京东云智能搜索补充实时信息")
    
    if st.button("清空对话记录"):
        clear_memory()
        st.session_state.health_messages = []
        st.rerun()
    
    st.divider()
    st.subheader("快速提问示例")
    quick_q = [
        "猫咪呕吐了一次，精神正常怎么办？",
        "狗狗拉稀带血，很臭，精神差",
        "猫咪一直打喷嚏流黄鼻涕",
        "狗狗不能吃什么食物？"
    ]
    for q in quick_q:
        if st.button(q, use_container_width=True):
            st.session_state.health_messages.append({"role": "user", "content": q})
            resp = chat_with_agent(q, use_web_search)
            st.session_state.health_messages.append({"role": "assistant", "content": resp})

# 初始化对话
if "health_messages" not in st.session_state:
    st.session_state.health_messages = []

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 对话咨询")
    for msg in st.session_state.health_messages:
        with st.chat_message(msg["role"]):
            if isinstance(msg["content"], dict):
                st.markdown(msg["content"]["answer"])
            else:
                st.write(msg["content"])
    
    user_input = st.chat_input("请描述宠物的症状、品种、年龄...")
    if user_input:
        st.session_state.health_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("正在分析症状..."):
                response = chat_with_agent(user_input, use_web_search)
                st.markdown(response["answer"])
        
        st.session_state.health_messages.append({"role": "assistant", "content": response})

with col2:
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
        
        st.metric("风险等级", risk)
    else:
        st.info("描述宠物症状后，此处将展示风险评估结果")
