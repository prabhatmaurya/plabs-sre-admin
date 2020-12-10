from app import app
import json
from flask import jsonify, render_template, request

@app.route('/',strict_slashes=False)
def home():
    response = dict(version='v2')
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

