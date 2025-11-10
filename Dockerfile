#use official python 
FROM python:3.11-slim 

WORKDIR /app 

COPY requirements.txt .. 

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]  


#Note --reload is useful for dev. In production, we’ll remove it and use gunicorn or uvicorn --workers.