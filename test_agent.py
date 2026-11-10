from utils.agent_core import chat_with_agent

# 测试1：基础健康咨询
result = chat_with_agent("狗狗呕吐了一次，精神还可以，怎么办？")
print("=== 测试1：健康咨询 ===")
print(result["answer"])
print("风险等级：", result["risk_level"])
print("\n" + "="*50 + "\n")

# 测试2：禁忌类问题
result2 = chat_with_agent("猫咪能吃巧克力吗？")
print("=== 测试2：饮食禁忌 ===")
print(result2["answer"])
