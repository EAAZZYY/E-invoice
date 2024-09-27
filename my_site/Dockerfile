# syntax=docker/dockerfile:1

# Set the Python version to use
ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-alpine AS base

# Set environment variables to avoid generating .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Create a non-privileged user that the app will run under
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install Python dependencies using requirements.txt
# Use --mount=type=cache for caching pip dependencies
COPY requirements.txt . 
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy the Django project source code into the container
COPY . .

# Ensure the non-privileged user owns the files
RUN chown -R appuser /app

# Switch to the non-privileged user
USER appuser

# Expose the application port (Django default is 8000)
EXPOSE 8000

# Run migrations and start the Django development server using JSON array format
CMD ["sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]
