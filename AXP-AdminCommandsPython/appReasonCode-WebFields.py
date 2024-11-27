import re
from flask import Flask, render_template, request, jsonify
import requests
import csv  # For CSV handling
import json # For Config File Handling

# ... (your existing functions: get_access_token, AddReasonCode, read_reason_codes_from_csv)

app = Flask(__name__)

@app.route('/', methods=['GET'])  # Route for serving the HTML
def index():
    return render_template('index.html')  # Render the template

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        print("I'm here running inside of the run_script function")  # Print all registered routes
        print("---- Collected Form Data ----") # Section to print form fields received
        api_url = request.form.get('api_url')
        print(f"API URL: {api_url}")
        client_id = request.form.get('client_id')
        print(f"Client ID: {client_id}")
        client_secret = request.form.get('client_secret')
        print(f"Client Secret: {client_secret}")  # Log this for now, but do NOT do this in production. Log the fact it was received only.
        username = request.form.get('username')
        print(f"Username: {username}")
        password = request.form.get('password')  # Be VERY careful with password security
        print(f"Password received (but don't log this in production - use a secure method instead)") # Never do in prod
        appkey = request.form.get('appkey')
        print(f"Appkey: {appkey}")
        print("----------------------------")  # Separator

        if not re.match(r"^https?://", api_url):  # Basic URL validation
            return jsonify({"status": "error", "message": "Invalid API URL format"}), 400

        if not re.match(r"^[a-zA-Z0-9-]+$", client_id):  # Example: Alphanumeric only for client_id
            return jsonify({"status": "error", "message": "Invalid Client ID format (alphanumeric only)"}), 400


        # Basic validation: Check for empty fields
        required_fields = ['api_url', 'client_id', 'client_secret', 'username', 'password', 'appkey']
        for field in required_fields:
            if not request.form.get(field):
                return jsonify({"status": "error", "message": f"{field} is required"}), 400  # 400 Bad Request
        
        print("Reading the CSV file...")  # Print all registered routes

        csv_file = request.files.get('csv_file') # File from Form
        reason_codes_data = read_reason_codes_from_csv(csv_file)
        if not reason_codes_data:
            return jsonify({"status": "error", "message": "Error on CSV Processing"}), 500

        access_token = get_access_token(api_url, client_id, client_secret, username, password, appkey)
        successful_codes, failed_codes = AddReasonCode(access_token, appkey, reason_codes_data, api_url) # Added api_url

        #access_token = get_access_token()
        #successful_codes, failed_codes = AddReasonCode(access_token, appkey, reason_codes_data)

        return jsonify({
            "status": "success", 
            "successful_codes": successful_codes, 
            "failed_codes": failed_codes
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#def get_access_token():
def get_access_token(api_url, client_id, client_secret, username, password, appkey): # Parameters added

    #auth_url = f"{api_url}/auth/token"
    auth_url = api_url
    payload = {
        #'grant_type': 'client_credentials',
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password
    }
    hheaders = {
        "accept": "application/json",
        "appkey": appkey
    }
    
    response = requests.post(auth_url, data=payload, headers=hheaders)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Failed to authenticate")



def read_reason_codes_from_csv(csv_file):
    """Reads reason codes from a CSV file.

    Args:
        csv_file_path: The path to the CSV file.

    Returns:
        A list of dictionaries, or None if an error occurs.
    """

    try:
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            reason_codes = list(reader)
            return reason_codes

    except Exception as e:  # Catch other potential errors during file reading
        print(f"Error reading CSV: {e}")
        return None

#def AddReasonCode(access_token, appkey, reason_codes):
def AddReasonCode(access_token, appkey, reason_codes, api_url): # Modified to include api_url
    #url = "https://na.cc.avayacloud.com/api/admin/reason-code/v1beta/accounts/RDDNFT/reason-codes"
    url = f"{api_url}admin/reason-code/v1beta/accounts/RDDNFT/reason-codes"  # Now uses api_url from parameter

    headers = {
        'Content-Type': 'application/json',
        'authorization': f'Bearer {access_token}',
        'appkey': appkey
    }

    successful_codes = []
    failed_codes = []

    for reason_code in reason_codes:
        response = requests.post(url, json=reason_code, headers=headers)
        
        if response.status_code == 201:  # 201 Created is the expected success code
            print(f"Reason code '{reason_code['codeName']}' added successfully.")
            successful_codes.append(reason_code)
        else:
            print(f"Error adding reason code '{reason_code['codeName']}': {response.text}")
            failed_codes.append(reason_code)

    return successful_codes, failed_codes    


if __name__ == '__main__':
    print(app.url_map)  # Print all registered routes
    app.run(debug=True, host='0.0.0.0', port=8080) # 0.0.0.0 makes it listen on all interfaces
