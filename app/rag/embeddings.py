from langchain_openai import OpenAIEmbeddings
from app.config.config import settings

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small",api_key=settings.openai_api_key)




