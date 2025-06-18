#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Running ETL: moving hospital data from CSVs to graph database..."

# Run the ETL script
python hospital_bulk_csv_write.py