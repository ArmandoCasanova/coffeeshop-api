# Official base image of Python
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the entire application into the container
COPY . /app

# Expose the port where FastAPI will run
EXPOSE 8000

# Command to run migrations and start the server
# Railway provides $PORT at runtime, defaults to 8000 for local development
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"]
