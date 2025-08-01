"""
Defines the agent for our RAG system
"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, Tool
from langchain.agents import initialize_agent, AgentType

from chains.cypher_chain import hospital_cypher_chain
from chains.review_chain import reviews_vector_chain
from chains.file_retrieval import build_file_retrieval_tool
from tools.wait_times import get_current_wait_times, get_most_available_hospital


HOSPITAL_AGENT_MODEL = os.getenv("HOSPITAL_AGENT_MODEL")

# hospital_agent_prompt = hub.pull("hwchase17/openai-functions-agent")


tools = [
    Tool(
        name="Experiences",
        func=reviews_vector_chain.invoke,
        description="""Useful when you need to answer questions
        about patient experiences, feelings, or any other qualitative
        question that could be answered about a patient using semantic
        search. Not useful for answering objective questions that involve
        counting, percentages, aggregations, or listing facts. Use the
        entire prompt as input to the tool. For instance, if the prompt is
        "Are patients satisfied with their care?", the input should be
        "Are patients satisfied with their care?".
        """,
    ),
    Tool(
        name="Graph",
        func=hospital_cypher_chain.invoke,
        description="""Useful for answering questions about patients,
        physicians, hospitals, insurance payers, patient review
        statistics, and hospital visit details. Use the entire prompt as
        input to the tool. For instance, if the prompt is "How many visits
        have there been?", the input should be "How many visits have
        there been?".
        """,
    ),
    Tool(
        name="Waits",
        func=get_current_wait_times,
        description="""Use when asked about current wait times
        at a specific hospital. This tool can only get the current
        wait time at a hospital and does not have any information about
        aggregate or historical wait times. Do not pass the word "hospital"
        as input, only the hospital name itself. For example, if the prompt
        is "What is the current wait time at Jordan Inc Hospital?", the
        input should be "Jordan Inc".
        """,
    ),
    Tool(
        name="Availability",
        func=get_most_available_hospital,
        description="""
        Use when you need to find out which hospital has the shortest
        wait time. This tool does not have any information about aggregate
        or historical wait times. This tool returns a dictionary with the
        hospital name as the key and the wait time in minutes as the value.
        """,
    ),
]
tools.append(
    build_file_retrieval_tool(
        docs_path = "kb_docs_retrievable", 
        qa_model_env="HOSPITAL_QA_MODEL"
    )
)

llm = ChatGoogleGenerativeAI(
    model=HOSPITAL_AGENT_MODEL,
)

llm_with_tools = llm.bind_tools(tools)

# rag_agent = initialize_agent(
#     tools=tools,
#     llm=llm,                                       
#     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,              
#     verbose=True,
# )

hospital_rag_agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    return_intermediate_steps=True,
)