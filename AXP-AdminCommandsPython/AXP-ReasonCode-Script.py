import requests
import csv
import json

# Configuration file path (adjust as needed)
CONFIG_FILE = "config.json"  # Or config.txt, etc.
REASONCODE_FILE = "reasoncodes.csv"  # Or config.txt, etc.


def load_config(config_file):
    """Loads configuration from a JSON file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)  # Parses JSON data
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        return None
    except json.JSONDecodeError:  # Handle invalid JSON
        print(f"Error: Invalid JSON format in '{config_file}'.")
        return None

# write a funcion to interact with axp api to add a new user
def add_user(access_token, appkey, user_data):
    #url = "https://na.api.avayacloud.com:443/api/admin/user/v1/accounts/RDDNFT/users"
    url = f"{api_url}{api_service_adduser}"
    headers = {
        'Content-Type': 'application/json',
        'authorization': f'Bearer {access_token}',
        'appkey': appkey
    }
    response = requests.post(url, json=user_data, headers=headers)
    response.raise_for_status()
    return response.json()


def get_access_token(api_url, api_service_token, grand_type, client_id, client_secret, username, password, appkey):
    auth_url = f"{api_url}{api_service_token}"
    payload = {
        'grant_type': grand_type,
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
        print(f"Status Code: {response.status_code}")
        raise Exception("Failed to authenticate")


# Function to list users
def list_users(access_token, appkey):
    headers = {
        'authorization': f'Bearer {access_token}',
        'appkey': appkey
    }

    users_url = "https://na.api.avayacloud.com:443/api/admin/user/v1/accounts/RDDNFT/users?pageNumber=1&pageSize=10&orderBy=loginId"  # Adjust the endpoint as needed
    response = requests.get(users_url, headers=headers)
    response.raise_for_status()
    return response.json()

def GetUser(access_token, appkey):
    url = "https://na.api.avayacloud.com:443/api/admin/user/v1/accounts/RDDNFT/users/11fc9b9d-0ab1-4818-a781-978b28f99b36"

    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}',
        'appkey': appkey
    }

    response = requests.get(url, headers=headers)

    print(response.text)

def AddReasonCode(access_token, appkey, reason_codes):
    
    #url = "https://na.cc.avayacloud.com/api/admin/reason-code/v1beta/accounts/RDDNFT/reason-codes"
    
    url = f"{api_url}{api_service_reasoncode}"

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


def read_reason_codes_from_csv(csv_file_path):
    """Reads reason codes from a CSV file.

    Args:
        csv_file_path: The path to the CSV file.

    Returns:
        A list of dictionaries, or None if an error occurs.
    """

    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:  # Handle potential Unicode issues
            reader = csv.DictReader(csvfile) # Assumes the first row contains headers
            reason_codes = list(reader)
            return reason_codes

    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_file_path}'")
        return None
    except Exception as e:  # Catch other potential errors during file reading
        print(f"Error reading CSV: {e}")
        return None

# Main script
try:
    print(f"======== =========================================== ====================")
    print(f"======== Welcome to AXP Admin Commands Python Script ====================")
    print(f"======== =========================================== ====================")

    print(f"======== Step 1 - Reading Configuration file ====================")
    
    config = load_config(CONFIG_FILE)
    if config:  # Only proceed if config was loaded successfully
        api_url = config.get("api_url")
        api_service_token = config.get("api_service_token")
        api_service_adduser = config.get("api_service_adduser")
        api_service_reasoncode = config.get("api_service_reasoncode")
        client_id = config.get("client_id")
        client_secret = config.get("client_secret")
        grand_type = config.get("grant_type")
        username = config.get("username")
        password = config.get("password")
        appkey = config.get("appkey")
        
        print(f"======== =========================================== ====================")
        print(f"======== Step 2 - Reading File with Reason Codes  ====================")
        csv_file_path = config.get("csv_file_path", REASONCODE_FILE ) # Provide a default if not in config

    print(f"======== =========================================== ====================")
    print(f"======== Now Let's Start  ====================")
    print(f"======== =========================================== ====================")
    print(f"======== Step 3 - Generating Token  ====================")
    access_token = get_access_token(api_url,api_service_token, grand_type, client_id, client_secret, username, password, appkey )

    print(f"Access Token : {access_token}")

    print(f"======== =========================================== ====================")
    print(f"======== Step 4 - Adding Dispositions Code from the file  ====================")
    reason_codes_data = read_reason_codes_from_csv(csv_file_path)

    if reason_codes_data:
        successful_codes, failed_codes = AddReasonCode(access_token, appkey, reason_codes_data)
        print(f"======== Summary:")
        print(f"======== Successfully added {len(successful_codes)} reason codes.")
        if failed_codes:
            print(f"======== Failed to add {len(failed_codes)} reason codes. See error messages above.")
            # Optionally, log the failed codes to a file for later investigation


    print(f"======== Script executado com sucesso ! ")
    print(f"======== =========================================== ====================")
    print(f"======== End of the AXP Admin Commands Python Script ====================")
    print(f"======== =========================================== ====================")

except Exception as e:
    print(f"An error occurred: {e}")

