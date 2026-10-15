# Use Python 3.13 in a lightweight Linux environment
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Display Python logs immediately
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api/ ./api/

# Create a dedicated non-root user
RUN useradd --create-home appuser

# Run the application as this user
USER appuser

# Document the port used by FastAPI
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
