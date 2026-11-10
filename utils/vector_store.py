import os
import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from langchain_core.documents import Document

def load_knowledge(knowledge_path: str):
    """加载知识库并按语义块切分"""
    with open(knowledge_path, 'r', encoding='utf-8') as f:
        content = f.read()
    chunks = [p.strip() for p in content.split('\n\n') if p.strip()]
    return chunks

def cut_text(text):
    """中文分词预处理"""
    return ' '.join(jieba.lcut(text))

def build_vector_db(knowledge_path: str, save_path: str = "./vector_db"):
    """构建TF-IDF向量数据库"""
    chunks = load_knowledge(knowledge_path)
    cut_chunks = [cut_text(c) for c in chunks]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cut_chunks)
    
    os.makedirs(save_path, exist_ok=True)
    with open(os.path.join(save_path, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
    with open(os.path.join(save_path, 'matrix.pkl'), 'wb') as f:
        pickle.dump(tfidf_matrix, f)
    with open(os.path.join(save_path, 'chunks.pkl'), 'wb') as f:
        pickle.dump(chunks, f)
    
    print(f"向量数据库已构建完成，保存至: {save_path}")

def load_vector_db(save_path: str = "./vector_db"):
    """加载向量库，返回完全兼容LangChain的检索器"""
    with open(os.path.join(save_path, 'vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)
    with open(os.path.join(save_path, 'matrix.pkl'), 'rb') as f:
        tfidf_matrix = pickle.load(f)
    with open(os.path.join(save_path, 'chunks.pkl'), 'rb') as f:
        chunks = pickle.load(f)
    
    class SimpleRetriever:
        def __init__(self, vectorizer, matrix, chunks, top_k=4):
            self.vectorizer = vectorizer
            self.matrix = matrix
            self.chunks = chunks
            self.top_k = top_k
        
        def get_relevant_documents(self, query):
            query_cut = cut_text(query)
            query_vec = self.vectorizer.transform([query_cut])
            scores = cosine_similarity(query_vec, self.matrix)[0]
            top_idx = np.argsort(scores)[::-1][:self.top_k]
            docs = [Document(page_content=self.chunks[idx]) for idx in top_idx]
            return docs
    
    return SimpleRetriever(vectorizer, tfidf_matrix, chunks)

def auto_build_vector_db():
    """启动时自动检测向量库，不存在则自动构建"""
    save_path = "./vector_db"
    knowledge_path = "./knowledge_base/pet_full_knowledge.txt"
    if not os.path.exists(os.path.join(save_path, 'chunks.pkl')):
        print("检测到向量库不存在，正在自动构建...")
        build_vector_db(knowledge_path, save_path)
    else:
        print("向量库已存在，直接加载")

if __name__ == "__main__":
    build_vector_db("./knowledge_base/pet_full_knowledge.txt")
