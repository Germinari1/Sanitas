FROM python:3.11-slim

WORKDIR /app

# Copy only dependency declaration first for better caching
COPY ./pyproject.toml ./pyproject.toml
RUN pip install .

# Then copy the actual application code
COPY ./src/ /app

EXPOSE 8000
CMD ["sh", "entrypoint.sh"]
