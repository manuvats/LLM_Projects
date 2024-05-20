from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama

from dotenv import load_dotenv

dotenv_path = os.getenv("ENV_PATH")
# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
#Langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

app=FastAPI(
    title = "Langchain Server",
    version = "1.0",
    description = "A simple API Server"
)

add_routes(
    app,
    ChatOpenAI(),
    path = "/openai"
)
model = ChatOpenAI()

#ollama llama2
llm = Ollama(model = "llama2")

prompt1 = ChatPromptTemplate.from_template("Write an essay about {topic} in 100 words")
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic} in 100 words")

add_routes(
    app,
    prompt1|model,
    path = "/essay"
)

add_routes(
    app,
    prompt2|model,
    path = "/poem"
)

if __name__=="__main__":
    uvicorn.run(app, host = "localhost", port = 8000)