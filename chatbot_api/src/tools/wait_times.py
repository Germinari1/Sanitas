import os
from typing import Any

import numpy as np
from langchain_neo4j import Neo4jGraph


def _get_current_hospitals() -> list[str]:
    """
    Fetch a list of current hospital names from a Neo4j database.
    
    Args:
        None
    Returns:
        list[str]: A list of hospital names in lowercase.
    """
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
    )

    current_hospitals = graph.query(
        """
        MATCH (h:Hospital)
        RETURN h.name AS hospital_name
        """
    )

    current_hospitals = [d["hospital_name"].lower() for d in current_hospitals]

    return current_hospitals


def _get_current_wait_time_minutes(hospital: str) -> int:
    """
    Get the current wait time at a hospital in minutes.
    
    Args:
        hospital (str): The name of the hospital.
    Returns:
        int: The wait time in minutes, or -1 if the hospital does not exist.
    """

    current_hospitals = _get_current_hospitals()

    if hospital.lower() not in current_hospitals:
        return -1

    return np.random.randint(low=0, high=600)


def get_current_wait_times(hospital: str) -> str:
    """
    Get the current wait time at a hospital formatted as a string.

    Args:
        hospital (str): The name of the hospital.
    Returns:
        str: The wait time formatted as "X hours Y minutes" or "Y minutes".
    """
    try:
        wait_time_in_minutes = _get_current_wait_time_minutes(hospital)
    except Exception:
        return f"Error: Unable to fetch wait time for '{hospital}'."

    if wait_time_in_minutes == -1:
        return f"Hospital '{hospital}' does not exist."

    hours, minutes = divmod(wait_time_in_minutes, 60)

    if hours > 0:
        formatted_wait_time = f"{hours} hours {minutes} minutes"
    else:
        formatted_wait_time = f"{minutes} minutes"

    return formatted_wait_time


def get_most_available_hospital(_: Any) -> dict[str, float]:
    """
    Find the hospital with the shortest wait time.
    
    Args:
        _: Unused parameter, can be any type.
    Returns:
        dict[str, float]: A dictionary with the hospital name as the key and the wait time in minutes as the value.
    """
    # guard against database errors
    try:
        current_hospitals = _get_current_hospitals()
    except Exception:
        return {"error": "Unable to fetch hospital list from database."}

    # no hospitals to choose
    if not current_hospitals:
        return {"error": "No hospitals found in database."}

    current_wait_times = [
        _get_current_wait_time_minutes(h) for h in current_hospitals
    ]

    # choose the shortest wait
    try:
        best_time_idx = int(np.argmin(current_wait_times))
    except ValueError:
        return {"error": "No wait-time data to choose from."}

    best_hospital = current_hospitals[best_time_idx]
    best_wait_time = current_wait_times[best_time_idx]

    return {best_hospital: best_wait_time}
