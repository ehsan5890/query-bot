from app.data_extraction import fetch_company_data, clean_data

url = "https://modulai.io/"
data = fetch_company_data(url)
if data:
    print(data)
    processed_data = clean_data(data)
    print("Extracted Data:")
    print(processed_data)
else:
    print("Data extraction failed.")
