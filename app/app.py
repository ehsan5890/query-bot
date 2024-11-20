from flask import Flask, jsonify

app = Flask(__name__)

from flask import Flask, request, jsonify
from data_extraction import fetch_company_data, clean_data, store_data_in_qdrant

@app.route('/')
def home():
    return jsonify({"message": "Welcome to QueryBot!"})


@app.route('/extract', methods=['POST'])
def extract_and_store_data():
    url = request.json['url']
    data = fetch_company_data(url)
    if data:
        cleaned_data = clean_data([data])
        store_data_in_qdrant(cleaned_data.to_dict(orient='records'))
        return {"message": "Data extracted and stored successfully."}, 200
    return {"error": "Failed to extract data."}, 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

