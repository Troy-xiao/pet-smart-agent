from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

def build_vector_db(knowledge_path: str, save_path: str = "./vector_db"):
    loader = TextLoader(knowledge_path, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
        separators=["\n\n", "\n", "。", "；", " "]
    )
    split_docs = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="shibing624/text2vec-base-chinese",
        model_kwargs={"device": "cpu"}
    )
    vector_db = FAISS.from_documents(split_docs, embeddings)
    vector_db.save_local(save_path)
    print(f"向量库构建完成，保存至 {save_path}")
    return vector_db

def load_vector_db(save_path: str = "./vector_db"):
    embeddings = HuggingFaceEmbeddings(
        model_name="shibing624/text2vec-base-chinese",
        model_kwargs={"device": "cpu"}
    )
    vector_db = FAISS.load_local(
        save_path, embeddings, allow_dangerous_deserialization=True
    )
    return vector_db

if __name__ == "__main__":
    build_vector_db("./knowledge_base/pet_full_knowledge.txt")

import os

def auto_build_vector_db():
    """自动检测向量库，不存在则自动构建"""
    save_path = "./vector_db"
    knowledge_path = "./knowledge_base/pet_full_knowledge.txt"
    
    if not os.path.exists(save_path):
        print("检测到向量库不存在，正在自动构建...")
        build_vector_db(knowledge_path, save_path)
    else:
        print("向量库已存在，直接加载")

