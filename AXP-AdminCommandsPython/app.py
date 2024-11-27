from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/run_script', methods=['POST'])  # Keep the same route
def run_script():
    try:
        return jsonify({"status": "success", "message": "Test successful!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True,port=8080) # host='0.0.0.0' for local network
