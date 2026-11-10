from langchain_openai import ChatOpenAI
from utils.config import JOYCODE_API_BASE, JOYCODE_API_KEY, JOYCODE_MODEL_NAME

def get_joycode_llm(temperature: float = 0.3):
    """
    初始化京东云JoyCode大模型实例（完全兼容OpenAI协议）
    """
    return ChatOpenAI(
        base_url=JOYCODE_API_BASE,
        api_key=JOYCODE_API_KEY,
        model=JOYCODE_MODEL_NAME,
        temperature=temperature,
        max_tokens=2048,
        streaming=True
    )
