from agents.hospital_rag_agent import hospital_rag_agent_executor
from fastapi import FastAPI
from models.hospital_rag_query import HospitalQueryInput, HospitalQueryOutput
from utils.async_utils import async_retry
from fastapi import HTTPException

app = FastAPI(
    title="Sanitas - Hospital Chatbot",
    description="Endpoints for a hospital system RAG chatbot",
)


@async_retry(max_retries=3, delay=1)
async def invoke_agent_with_retry(query: str):
    """
    Retry the agent if a tool fails to run. Asynchronous invocation is used.
    
    Args:
        query (str): The query to send to the RAG agent.
    Returns:
        dict: The response from the RAG agent.
    """
    try:
        return await hospital_rag_agent_executor.ainvoke({"input": query})
    except ValueError as e:
        raise


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/hospital-rag-agent")
async def query_hospital_agent(
    query: HospitalQueryInput,
) -> HospitalQueryOutput:
    try:
        query_response = await invoke_agent_with_retry(query.text)
    except ValueError as e:
        # 400 Bad Request: user asked for something unsafe
        raise HTTPException(status_code=400, detail=str(e))

    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]
    return query_response

