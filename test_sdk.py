import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("JOYCODE_API_BASE"),
    api_key=os.getenv("JOYCODE_API_KEY")
)

try:
    response = client.chat.completions.create(
        model=os.getenv("JOYCODE_MODEL_NAME"),
        messages=[{"role": "user", "content": "你好，请简单介绍一下自己"}]
    )
    print("✅ SDK调用成功！")
    print("模型回复：", response.choices[0].message.content)
except Exception as e:
    print("❌ SDK调用失败")
    print("错误详情：", e)
