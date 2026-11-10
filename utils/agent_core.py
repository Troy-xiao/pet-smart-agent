from utils.vector_store import load_vector_db, auto_build_vector_db

# 启动时自动构建向量库（云端部署必备）
auto_build_vector_db()
# 加载基础组件
llm = get_joycode_llm()
vector_db = load_vector_db()



from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from utils.vector_store import load_vector_db
from utils.joycode_llm import get_joycode_llm
from utils.jd_search import jd_web_search

# 加载基础组件
llm = get_joycode_llm()
retriever = load_vector_db()  #更新
# vector_db = load_vector_db()
# retriever = vector_db.as_retriever(search_kwargs={"k": 4})

# 对话记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

# 核心问答prompt
QA_PROMPT_TEMPLATE = """
你是专业的智慧养宠AI助手「宠智通」，请结合知识库内容与对话历史，严谨回答用户问题。
要求：
1. 医疗类内容严格遵循知识库标准，分级给出建议，明确标注风险等级
2. 所有医疗建议结尾必须标注：⚠️ 本建议仅供参考，重症请及时就医
3. 语气专业易懂，避免晦涩术语，分点呈现核心内容
4. 若问题超出知识库范围，如实说明并给出通用建议

知识库内容：
{context}

对话历史：
{chat_history}

用户问题：{question}

回答：
"""

QA_PROMPT = PromptTemplate(
    template=QA_PROMPT_TEMPLATE,
    input_variables=["context", "chat_history", "question"]
)

# 问题浓缩prompt（用于把历史对话+新问题整合成独立问题，供检索使用）
CONDENSE_PROMPT_TEMPLATE = """
结合以下对话历史和用户的新问题，将其重新表述为一个独立的完整问题。
对话历史：
{chat_history}

新问题：{question}

独立完整问题：
"""

CONDENSE_PROMPT = PromptTemplate(
    template=CONDENSE_PROMPT_TEMPLATE,
    input_variables=["chat_history", "question"]
)

# 构建带记忆的对话检索问答链
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    condense_question_prompt=CONDENSE_PROMPT,
    combine_docs_chain_kwargs={"prompt": QA_PROMPT},
    return_source_documents=True,
    verbose=False
)


def chat_with_agent(query: str, use_web_search: bool = False):
    """
    智能体核心对话接口，支持开启联网搜索增强
    """
    # 基础检索回答
    result = qa_chain.invoke({"question": query})
    answer = result["answer"]

    # 联网搜索增强
    web_refs = []
    if use_web_search:
        web_results = jd_web_search(query)
        if web_results:
            web_refs = web_results
            refs_text = "\n\n📡 联网参考信息：\n"
            for i, item in enumerate(web_results[:2], 1):
                refs_text += f"{i}. {item['title']}：{item['content'][:100]}...\n"
            answer += refs_text

    # 风险等级解析
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
    response = llm.invoke(prompt)
    return response.content


def analyze_behavior(behavior_desc: str, pet_type: str):
    """行为问题分析"""
    prompt = f"""
    宠物类型：{pet_type}
    行为描述：{behavior_desc}
    
    请分析该行为的可能成因，并给出3-4条可落地的矫正/改善方案。
    要求：先分析原因，再给解决方案，分点清晰，实操性强。
    """
    response = llm.invoke(prompt)
    return response.content


def clear_memory():
    """清空对话记忆"""
    memory.clear()
