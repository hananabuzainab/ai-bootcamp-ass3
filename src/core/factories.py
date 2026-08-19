import os
from functools import lru_cache
from src.config.config_parser import settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from src.logger.logger import logger
class ModelFactory:
    @staticmethod
    @lru_cache(maxsize=1)
    def get_embeddings():
        # إضافة نقطتين : بنهاية السطر
        if settings.embedding_provider.lower() == "huggingface":
            logger.info("initialize embedding model")
            return HuggingFaceEmbeddings(
                model_name=settings.embedding_model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        else:
            raise ValueError("Unsupported embedding provider")
            
    @staticmethod
    @lru_cache(maxsize=1)
    def get_llm():
        if settings.llm_provider.lower()=="gemini":
            logger.info("initialize llm")
            return ChatGoogleGenerativeAI(
            model=settings.llm_model_name,
            temperature=settings.temperature )  

        else:

            raise ValueError(f"unsupported LLM provider :{settings.llm_provider}")             

