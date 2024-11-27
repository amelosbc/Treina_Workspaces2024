from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    try:
        return jsonify({"status": "success", "message": "Test successful!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=8080)  # Or another port
