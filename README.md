# QueryBot: A Retrieval-Augmented Generation (RAG) System with Flask

QueryBot is an AI-powered chatbot built using a Retrieval-Augmented Generation (RAG) approach. It allows users to ask questions, retrieves relevant data from a database (Qdrant), and provides intelligent responses using OpenAI's GPT models. The system is designed with Flask, Docker, and an interactive user interface.

---

## Features

- **Retrieval-Augmented Generation**: Combines retrieved data from a vector database with GPT for context-aware answers.
- **Database Integration**: Utilizes Qdrant, a high-performance vector database, for storing and retrieving data.
- **Interactive User Interface**: Simple and intuitive web-based chatbot interface.
- **Context-Aware Responses**: Tracks conversation history to handle follow-up questions effectively.
- **Scalable Architecture**: Deployed using Docker for seamless scalability.

---

## Prerequisites

- Python 3.9+
- Docker (for Qdrant and deployment)
- OpenAI API key for GPT integration

---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ehsan5890/querybot.git
    cd querybot
    ```

2. **Set up the virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:
    Create a `.env` file in the root directory:
    ```
    OPENAI_API_KEY=your_openai_api_key
    QDRANT_HOST=localhost
    QDRANT_PORT=6333
    FLASK_APP=app/app.py
    FLASK_ENV=development
    ```

5. **Run Qdrant (via Docker)**:
    ```bash
    docker run -d -p 6333:6333 qdrant/qdrant
    ```


 

---


