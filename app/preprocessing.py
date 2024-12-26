import tiktoken
import string

def fix_encoding(text):
    try:
        # Attempt to encode and decode using 'latin1' and 'utf-8'
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Handle the error by replacing invalid characters
        return text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')


def replace_unknown_chars(text):
    return text.replace("�", "[UNK]")  # Replace unknown characters (common in text issues)


def clean_text(text):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, text))

def preprocess_text(text):
    # Fix encoding issues
    text = fix_encoding(text)
    # Clean non-printable characters
    text = clean_text(text)
    # Replace specific unknown characters
    text = replace_unknown_chars(text)
    return text


def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def process_large_text(raw_text):
    # Step 1: Preprocess the text
    processed_text = preprocess_text(raw_text)

    # Step 2: Check token count
    token_count = count_tokens(processed_text)


    # Step 3: Send the processed text to the API

    return processed_text, token_count



