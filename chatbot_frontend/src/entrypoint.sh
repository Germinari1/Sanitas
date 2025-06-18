#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Spinning up chatbot frontend..."

# Run the ETL script
streamlit run main.py --server.runOnSave=true