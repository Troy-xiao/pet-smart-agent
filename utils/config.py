import os
from dotenv import load_dotenv

load_dotenv()

# JoyCode大模型配置
JOYCODE_API_BASE = os.getenv("JOYCODE_API_BASE")
JOYCODE_API_KEY = os.getenv("JOYCODE_API_KEY")
JOYCODE_MODEL_NAME = os.getenv("JOYCODE_MODEL_NAME", "glm-4-flash")

# 京东云智能搜索配置
JD_SEARCH_API_KEY = os.getenv("JD_SEARCH_API_KEY")
JD_SEARCH_ENDPOINT = os.getenv("JD_SEARCH_ENDPOINT")

# 访问密码
ACCESS_PASSWORD = os.getenv("ACCESS_PASSWORD", "123456")
