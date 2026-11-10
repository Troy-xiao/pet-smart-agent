from utils.joycode_llm import get_joycode_llm
from utils.jd_search import jd_web_search

print("=== 测试JoyCode大模型 ===")
try:
    llm = get_joycode_llm()
    resp = llm.invoke("你好，请简单介绍一下自己")
    print("大模型调用成功：", resp.content[:50])
except Exception as e:
    print("大模型调用失败：", e)

print("\n=== 测试京东云智能搜索 ===")
try:
    result = jd_web_search("2026宠物喂养最新标准")
    if result:
        print("搜索调用成功，返回", len(result), "条结果")
    else:
        print("搜索无结果或未配置")
except Exception as e:
    print("搜索调用失败：", e)


#from utils.config import JOYCODE_API_KEY, JOYCODE_API_BASE
#print("读取到的API地址：", JOYCODE_API_BASE)
#print("读取到的密钥长度：", len(RsCenterCH-rCYhUxB0ueSU09AFcejzdh4DvN9bJOBSQ1zkdY+m6bw=) if RsCenterCH-rCYhUxB0ueSU09AFcejzdh4DvN9bJOBSQ1zkdY+m6bw= else 0)

