import requests
import csv

# Replace these with your actual API credentials
api_url = "https://na.api.avayacloud.com/api/auth/v1/RDDNFT/protocol/openid-connect/token"
client_id = "seguros-atlas"
client_secret = "YMN85CqygVCkfC6T67eNjD1ROGxRH8dA"
username = "tadmin@segurosatlas.com.mx"
password = "ipRG87),W)Lqvw1"
appkey = "d53d2362d0ee4b1da3de1274c5518883"

# write a funcion to interact with axp api to add a new user
def add_user(access_token, appkey, user_data):
    url = "https://na.api.avayacloud.com:443/api/admin/user/v1/accounts/RDDNFT/users"
    headers = {
        'Content-Type': 'application/json',
        'authorization': f'Bearer {access_token}',
        'appkey': appkey
    }
    response = requests.post(url, json=user_data, headers=headers)
    response.raise_for_status()
    return response.json()


def get_access_token():
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
    url = "https://na.cc.avayacloud.com/api/admin/reason-code/v1beta/accounts/RDDNFT/reason-codes"

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
    print(f"======== Obter Token ====================")
    access_token = get_access_token()
    print(f"Access Token : {access_token}")
    print(f"Autenticação realizada com sucesso! {access_token}")

    print(f"======== Adicionar um Disposition Code ====================")
    csv_file_path = "reasoncodes.csv" # or get this from user input
    reason_codes_data = read_reason_codes_from_csv(csv_file_path)

    if reason_codes_data:
        successful_codes, failed_codes = AddReasonCode(access_token, appkey, reason_codes_data)
        print(f"\nSummary:")
        print(f"Successfully added {len(successful_codes)} reason codes.")
        if failed_codes:
            print(f"Failed to add {len(failed_codes)} reason codes. See error messages above.")
            # Optionally, log the failed codes to a file for later investigation

    print(f"======== OBTER UM USUARIO====================")
    print(GetUser(access_token, appkey))

    print(f"========= Listar Usuarios ===================")
    users = list_users(access_token, appkey)
    print("Users in the environment:")
    for user in users:
        print(user)

except Exception as e:
#except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


print(f"Script executado com sucesso ! ")
