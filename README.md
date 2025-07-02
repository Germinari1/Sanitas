# Sanitas: An Agentic RAG Chatbot System

This project demonstrates  a Retrieval-Augmented Generation (RAG) chatbot using LangChain, Neo4j (a graph database), and concepts of agentic AI. Given a dataset, the chatbot is specialized to answer questions about hospitals, payers, physicians, patients, visits, and reviews. I supports both RAG over both a graph database (`AuraDB`) and `.txt`/`.pdf` files, besides tools that can be called by the agent.

Some features include: 
- **Graph database**: Uses `Neo4j` to store and query our data. That way, our chatbot can quickly retrieve relevant information.
- **LLM agents**: Uses `LangChain` to create an `AI agent` that can answer questions about the data and select appropriate tools to use, based on the user's query.
- **UI**: Provides a user-friendly interface to interact with the chatbot, built with `Streamlit`.
- **REST API**: The chatbot is exposed as a `REST API`, built using `FastAPI`.
- **Microservices-based architecture**: Each "microservice" is containerized using `Docker`, and `Docker compose` is used to organize such build process.

> Note: this was used as an educational/demonstration project for an event at [Entropic](https://entropic.pythonanywhere.com/). The data used here is synthetic and used for learning and demonstration purposes only.

## Getting Started
Create a `.env` file in the root directory and add the following environment variables:

```.env
GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>

NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>

HOSPITALS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/hospitals.csv
PAYERS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/payers.csv
PHYSICIANS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/physicians.csv
PATIENTS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/patients.csv
VISITS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/visits.csv
REVIEWS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/reviews.csv

HOSPITAL_AGENT_MODEL=gemini-2.0-flash
HOSPITAL_CYPHER_MODEL=gemini-2.0-flash
HOSPITAL_QA_MODEL=gemini-2.0-flash

CHATBOT_URL=http://host.docker.internal:8000/hospital-rag-agent
```

Here, we are using Google's Gemini 2.0 Flash model for the LLMs, but you can replace these with any other models that you prefer. Just keep in mind that different models may have different capabilities. In any case, check the documentation of the model you plan to use.

In case you stick to Gemini, get your API key [here](https://aistudio.google.com/). They offer a free tier.

Follow the directions [here](https://neo4j.com/cloud/platform/aura-graph-database/?ref=docs-nav-get-started) to create a free instance and get your Neo4j-related environment variables.

### Running the Project

After completing these prerequisites:
1. Setting up a Neo4j AuraDB instance
2. Configuring all environment variables in your `.env` file
3. Installing [Docker Compose](https://docs.docker.com/compose/install/)

You're ready to launch the entire application. Open a terminal in the project directory and execute:

```console
$ docker-compose up --build
```

After the build process finishes, you'll be able to access the chatbot API at `http://localhost:8000/docs` and the Streamlit app at `http://localhost:8501/`.