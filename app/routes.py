
from flask import Flask, render_template, request, jsonify
# from app import app  # Import the app instance from __init__.py
from app.data_extraction import get_all_links, fetch_company_data, clean_data, get_collection_name
from app.data_retrieval import  retrieve_data_from_qdrant, filter_similar_content, summarize_content, remove_internal_duplicates
from app.embedding import store_data_in_qdrant
from dotenv import load_dotenv
import openai
import os
load_dotenv()


app = Flask(__name__)
client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  # Ensure the API key is set in the environment variables
)
@app.route('/')
def index():
    return render_template('bot_interface.html')


@app.route('/extract', methods=['POST'])
def extract_data():
    data = request.get_json()
    base_url = data.get('url')
    if not base_url:
        return jsonify({"error": "No URL provided"}), 400

    all_links = get_all_links(base_url)

    # Fetch data for each link and filter out None values
    data_list = [fetch_company_data(url) for url in all_links]
    data_list = [item for item in data_list if item is not None]  # Filter out None values
    collection_name = get_collection_name(base_url)
    if not data_list:
        return jsonify({"error": "No data extracted from the website"}), 400

    cleaned_data = clean_data(data_list)

    # Store cleaned data in Qdrant
    store_data_in_qdrant(cleaned_data.to_dict(orient='records'), collection_name=collection_name)

    return jsonify({"message": "Data extracted and stored successfully"}), 200


@app.route('/data/query', methods=['POST'])
def query_data():
    # url = "https://modulai.io/"
    url = "https://zenseact.com/"
    collection_name = get_collection_name(url)
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Retrieve relevant content from Qdrant
    retrieved_data = retrieve_data_from_qdrant(query, collection_name=collection_name)
    content_list = [item.get('content', '') for item in retrieved_data]
    unique_content = filter_similar_content(content_list)
    # Extract content safely
    # context = " ".join([item.get('content', '') for item in retrieved_data if 'content' in item])

    context = summarize_content(unique_content)
    print(context)
    print('232323\n')
    # Generate response using LLM
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with "gpt-4" or the desired model
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that provides information based on given context."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ],
            max_tokens=1500,
            temperature=0.7  # Adjust temperature for more or less creative responses
        )
        # print(chat_completion)
        # print(chat_completion['choices'])
        generated_response = chat_completion.choices[0].message.content

    except Exception as e:
        return jsonify({"error": f"OpenAI API Error: {e}"}), 500
    return jsonify({"response": generated_response})


@app.route('/retrieve', methods=['POST'])
def retrieve_data():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    retrieved_data = retrieve_data_from_qdrant(query)
    return jsonify(retrieved_data), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)



