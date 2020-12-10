from app import app
from flask import jsonify, render_template, request

@app.route('/',strict_slashes=False)
def home():
    response = dict(version:'v1')
    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)

