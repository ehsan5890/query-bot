from flask import Flask, jsonify

app = Flask(__name__)
from flask import Flask, request, jsonify
from data_extraction import get_all_links, fetch_company_data, clean_data
from data_retrieval import  retrieve_data_from_qdrant
from embedding import store_data_in_qdrant
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to QueryBot!"})


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

    if not data_list:
        return jsonify({"error": "No data extracted from the website"}), 400

    cleaned_data = clean_data(data_list)

    # Store cleaned data in Qdrant
    store_data_in_qdrant(cleaned_data.to_dict(orient='records'))

    return jsonify({"message": "Data extracted and stored successfully"}), 200


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


