# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import os

def B12(filepath):
    if filepath.startswith('./data'):
        # raise PermissionError("Access outside /data is not allowed.")
        # print("Access outside /data is not allowed.")
        return True
    else:
        return False

# B3: Fetch Data from an API
def B3(url, save_path):
    if not B12(save_path):
        return None
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

# B4: Clone a Git Repo and Make a Commit
def clone_git_repo(repo_url, commit_message):
    import subprocess
    subprocess.run(["git", "clone", repo_url, "/data/repo"])
    subprocess.run(["git", "-C", "/data/repo", "commit", "-m", commit_message])

# B5: Run SQL Query
def B5(db_path, query, output_filename):
    if not B12(db_path):
        return None
    import sqlite3, duckdb
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

# B6: Web Scraping
def B6(url, output_filename):
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))

# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return None
    if not os.path.exists(os.path.dirname(output_path)):
        print(f"Error: Output directory {os.path.dirname(output_path)} does not exist.")
        return None
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)
    print("Image processed successfully.")

# B8: Audio Transcription
def B8(audio_path):
    import openai
    if not B12(audio_path):
        return None
    with open(audio_path, 'rb') as audio_file:
        return openai.Audio.transcribe("whisper-1", audio_file)

# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    import markdown
    if not B12(md_path):
        return None
    if not B12(output_path):
        return None
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)

# B10: API Endpoint for CSV Filtering
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/filter_csv', methods=['POST'])
def filter_csv():
    import pandas as pd
    data = request.json
    csv_path, filter_column, filter_value = data['csv_path'], data['filter_column'], data['filter_value']
    B12(csv_path)
    df = pd.read_csv(csv_path)
    filtered = df[df[filter_column] == filter_value]
    return jsonify(filtered.to_dict(orient='records'))

if __name__ == "__main__":
    # Test B12 function
    print(B12("./data/sample.txt"))  # Should print True
    print(B12("/etc/passwd"))  # Should print False

    # Test B3 function
    B3("https://jsonplaceholder.typicode.com/todos/1", "./data/sample.json")
    print("Data fetched and saved.")

    # Test B5 function (Make sure the database exists before running)
    result = B5("./data/test.db", "SELECT name FROM sqlite_master WHERE type='table';", "./data/sql_output.txt")
    print(result)

    # Test B6 function
    B6("https://example.com", "./data/scraped.html")
    print("Web scraping completed.")

    # Test B7 function (Ensure image exists)
    B7("./data/sample.jpg", "./data/resized.jpg", (100, 100))
    print("Image processed and saved.")

    # Test B9 function (Ensure markdown file exists)
    B9("./data/format.md", "./data/output.html")
    print("Markdown converted to HTML.")
