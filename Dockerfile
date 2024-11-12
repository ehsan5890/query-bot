FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the application code
COPY app /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5001

ENV FLASK_APP=app.app

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]


