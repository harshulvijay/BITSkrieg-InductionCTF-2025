
from flask import Flask, jsonify
import os

app = Flask(__name__)

FLAG = os.environ.get('FLAG', 'fake{flag}')


@app.route('/flag')
def get_flag():
    return jsonify({'flag': FLAG})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
