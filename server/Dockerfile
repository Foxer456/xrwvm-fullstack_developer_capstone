# Use a lightweight Python base image
FROM python:3.12.0-slim-bookworm

# Environment variables to ensure proper Python behavior
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# Define the working directory in the container
ENV APP=/app
WORKDIR $APP

# Copy and install dependencies
COPY requirements.txt $APP
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application files
COPY . $APP

# Expose the application port
EXPOSE 8000

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Define the default command to start the Django application using Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
