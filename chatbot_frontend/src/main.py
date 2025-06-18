"""
A simple Streamlit app that serves as a frontend for our chatbot.
"""
import os

import requests
import streamlit as st

CHATBOT_URL = os.getenv(
    "CHATBOT_URL", "http://localhost:8000/hospital-rag-agent"
)

with st.sidebar:
    st.header("What is this app?")
    st.markdown(
        """
        This chatbot provides an AI agent designed to answer questions about the hospitals, 
        patients, visits, physicians, and insurance payers in a hypothetical hospital system.
        The agent uses retrieval-augmented generation (RAG) to provide accurate and relevant 
        answers based on the data it has access to.
        """
    )

    st.header("Sample Questions")
    st.markdown("- Which hospitals are in the hospital system?")
    st.markdown(
        """- What is the current wait time at wallace-hamilton hospital?"""
    )
    st.markdown(
        """- At which hospitals are patients complaining about billing and
        insurance issues?"""
    )
    st.markdown(
        "- What is the average duration in days for closed emergency visits?"
    )
    st.markdown("- What is the average billing amount for medicaid visits?")
    st.markdown(
        """- How many reviews have been written from
                patients in Florida?"""
    )
    st.markdown(
        """- Which physician has received the most reviews for this visits
        they've attended?"""
    )
    st.markdown("- What is the ID for physician James Cooper?")
    st.markdown(
        """- List every review for visits treated by physician 270.
        Don't leave any out."""
    )


st.title("Sanitas")
st.info(
    """I'm Sanitas, your hospital system chatbot! I'm happy to answer questions about patients, visits, insurance payers, hospitals,
    physicians, and wait times!"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated?", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("Enter your question here..."):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
