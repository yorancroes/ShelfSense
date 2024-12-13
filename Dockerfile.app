FROM python:3.11-slim

WORKDIR /app

# Copy the entire app folder
COPY ./app /app

# Install system dependencies
RUN apt-get update && apt-get install -y python3-tk libpq-dev && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
