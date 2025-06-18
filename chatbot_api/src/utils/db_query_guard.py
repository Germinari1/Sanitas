def is_safe_cypher(query: str) -> bool:
    """
    Check if a Cypher query is safe to execute by ensuring it does not contain
    any unsafe keywords that could modify the database state. This is meant to 
    prevent malicious or unintended modifications from queries generate by the LLM
    through natural language input.
    
    Args:
        query (str): The Cypher query to check.
    Returns:
        bool: True if the query is safe, False if it contains unsafe keywords.
    """
    unsafe_keywords = [
        "CREATE", "DELETE", "MERGE", "SET", "REMOVE", "CALL", "LOAD", "DROP",
        "SHUTDOWN", "RESTART", "PROFILE", "EXPLAIN", "USE"
    ]
    
    return not any(k in query.upper() for k in unsafe_keywords)