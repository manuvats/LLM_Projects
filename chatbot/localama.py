from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

#Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's queries"),
        ("user", "Question: {question}")
    ]
)

## streamlt framework
st.title('Langchain Demo With Llama2')
input_text=st.text_input("Search the topic u want")

#Ollama LLama2 LLM
llm = Ollama(model = "llama2")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser
