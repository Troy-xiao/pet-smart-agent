import os
from openai import OpenAI
from utils.vector_store import load_vector_db, auto_build_vector_db
from utils.config import JOYCODE_API_BASE, JOYCODE_API_KEY, JOYCODE_MODEL_NAME
from utils.jd_search import jd_web_search

# 启动时自动构建向量库
auto_build_vector_db()

# 初始化大模型客户端
client = OpenAI(
    base_url=JOYCODE_API_BASE,
    api_key=JOYCODE_API_KEY
)

# 加载检索器
retriever = load_vector_db()

# 全局对话记忆
chat_history = []

SYSTEM_PROMPT = """
你是专业的智慧养宠AI助手「宠智通」，请结合参考知识库与对话历史，严谨回答用户问题。
要求：
1. 医疗类内容严格遵循知识库标准，分级给出建议，明确标注风险等级
2. 所有医疗建议结尾必须标注：⚠️ 本建议仅供参考，重症请及时就医
3. 语气专业易懂，避免晦涩术语，分点呈现核心内容
4. 若问题超出知识库范围，如实说明并给出通用建议
"""


def chat_with_agent(query: str, use_web_search: bool = False):
    """
    智能体核心对话接口
    """
    # 1. 检索知识库相关内容
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in docs])

    # 2. 拼接对话历史
    history_text = ""
    for msg in chat_history[-6:]:  # 保留最近6轮对话
        history_text += f"{msg['role']}: {msg['content']}\n"

    # 3. 组装最终prompt
    final_prompt = f"""
    {SYSTEM_PROMPT}

    参考知识库内容：
    {context}

    对话历史：
    {history_text}

    用户问题：{query}

    请给出回答：
    """

    # 4. 调用大模型
    response = client.chat.completions.create(
        model=JOYCODE_MODEL_NAME,
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0.3,
        max_tokens=2048
    )
    answer = response.choices[0].message.content

    # 5. 联网搜索增强
    web_refs = []
    if use_web_search:
        web_results = jd_web_search(query)
        if web_results:
            web_refs = web_results
            refs_text = "\n\n📡 联网参考信息：\n"
            for i, item in enumerate(web_results[:2], 1):
                refs_text += f"{i}. {item['title']}：{item['content'][:100]}...\n"
            answer += refs_text

    # 6. 更新对话记忆
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": answer})

    # 7. 风险等级解析
    risk_level = "低风险"
    if "高风险" in answer or "立即就医" in answer:
        risk_level = "高风险"
    elif "中风险" in answer or "密切观察" in answer:
        risk_level = "中风险"

    return {
        "answer": answer,
        "risk_level": risk_level,
        "web_refs": web_refs
    }


def generate_feeding_plan(pet_type: str, breed: str, age: str, weight: str):
    """生成定制化喂养方案"""
    prompt = f"""
    请为以下宠物生成科学喂养方案：
    宠物类型：{pet_type}
    品种：{breed}
    年龄：{age}
    体重：{weight}
    
    要求包含：
    1. 每日喂食次数与喂食量建议
    2. 主粮选择要点（蛋白含量、营养需求）
    3. 可喂食的辅食与禁忌食物
    4. 日常饮水与喂养注意事项
    
    分点清晰，语言实用易懂。
    """
    response = client.chat.completions.create(
        model=JOYCODE_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def analyze_behavior(behavior_desc: str, pet_type: str):
    """行为问题分析"""
    prompt = f"""
    宠物类型：{pet_type}
    行为描述：{behavior_desc}
    
    请分析该行为的可能成因，并给出3-4条可落地的矫正/改善方案。
    要求：先分析原因，再给解决方案，分点清晰，实操性强。
    """
    response = client.chat.completions.create(
        model=JOYCODE_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def clear_memory():
    """清空对话记忆"""
    global chat_history
    chat_history = []
