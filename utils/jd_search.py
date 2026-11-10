import requests
from utils.config import JD_SEARCH_API_KEY, JD_SEARCH_ENDPOINT

def jd_web_search(query: str, page_size: int = 3):
    """
    调用京东云智能搜索API，获取联网实时信息
    """
    if not JD_SEARCH_API_KEY:
        return []
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JD_SEARCH_API_KEY}"
    }
    
    payload = {
        "query": query,
        "page_size": page_size,
        "page": 1,
        "safe_mode": True
    }
    
    try:
        response = requests.post(JD_SEARCH_ENDPOINT, json=payload, headers=headers, timeout=10)
        result = response.json()
        
        if result.get("code") == 0 and "data" in result:
            items = result["data"].get("items", [])
            return [
                {
                    "title": item.get("title", ""),
                    "content": item.get("summary", ""),
                    "url": item.get("url", "")
                }
                for item in items
            ]
        return []
    except Exception as e:
        print(f"搜索调用失败: {e}")
        return []
