# Import necessary libraries and modules
from langchain.chat_models import ChatOpenAI
import sqlite3
import pandas as pd
import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
import streamlit as st

# Set the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the Langchain ChatOpenAI model
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4")

# Connect to the SQLite database
connection = sqlite3.connect("Chinook_Sqlite.sqlite")

# Import necessary libraries and modules


# Create an instance of SQLDatabase using the 'customer.db' SQLite database
db = SQLDatabase.from_uri('sqlite:///Chinook_Sqlite.sqlite')

# Create an SQL agent executor with specified parameters
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True,
    return_intermediate_steps=True
)

from langchain import LLMChain
from langchain.agents import (AgentExecutor, Tool, ZeroShotAgent)
from langchain_experimental.tools import PythonREPLTool

# Define a description to suggest how to determine the choice of tool
description = (
    "Useful when you require to answer analytical questions. "
    "Use this more than the Python REPL tool if the question is about analytics,"
    "like 'How many tracks per genre are there?' or 'count the number of customers by genre'. "
    "Try not to use clause in the SQL."
)

# Create a Tool object for customer data with the previously defined agent executor 'create_sql_agent' and description
analytics_tool = Tool(
    name="Analytics",
    func=agent_executor.run,
    description=description,
)

# Create the whole list of tools
tools = [PythonREPLTool()]
tools.append(analytics_tool)

# Define the prefix and suffix for the prompt
prefix = "Below are tools that you can access:"
suffix = (
    "Pass the relevant part of the request directly to the Analytics tool.\n\n"
    "Request: {input}\n"
    "{agent_scratchpad}"
)

# Create the prompt using ZeroShotAgent
# Use agent_scratchpad to store the actions previously used, guiding the subsequent responses.
agent_prompt = ZeroShotAgent.create_prompt(
    tools, prefix=prefix, suffix=suffix, input_variables=["input", "agent_scratchpad"]
)

# Create an instance of ZeroShotAgent with the LLMChain and the allowed tool names
zero_shot_agent = ZeroShotAgent(
    llm_chain=LLMChain(llm=llm, prompt=agent_prompt),
    allowed_tools=[tool.name for tool in tools]
)

# Create an AgentExecutor which enables verbose mode and handling parsing errors
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=zero_shot_agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# Define user input
user_inquiry = st.text_input("Use a bar graph to visualize the result of the following inquiry: " \
          "What are the total sales per country?")

#user_inquiry = "Use a bar graph to visualize the result of the following inquiry: " \
#          "What are the total sales per country?"

# Run the agent to generate a response
if st.button("Run Query"):
    # Run the agent to generate a response
    response = agent_executor.run(user_inquiry)
    st.write(response)

#agent_executor.run(user_inquiry)