from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Read the CSV and return its content as a JSON
        data = pd.read_csv(filepath)
        return jsonify(data.to_dict(orient='records')), 200
    
    return jsonify({'error': 'File type not supported'}), 400

if __name__ == '__main__':
    app.run(debug=True)
