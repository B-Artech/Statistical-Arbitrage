from flask import Flask, jsonify, send_from_directory # type: ignore
from flask_cors import CORS # type: ignore
import pandas as pd # type: ignore

app = Flask(__name__)
CORS(app)

CSV_PATH = r'crypto_spread_data.csv'
@app.route('/data')
def get_data():
    df = pd.read_csv(CSV_PATH)
    return jsonify(df.to_dict('records'))

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/app.js')
def serve_js():
    return send_from_directory('.', 'app.js')

if __name__ == '__main__':
    app.run(port=5000)
