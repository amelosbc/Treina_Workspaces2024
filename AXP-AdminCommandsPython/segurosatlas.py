import requests

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

def AddResonCode(access_token, appkey):
    url = "https://na.cc.avayacloud.com/api/admin/reason-code/v1beta/accounts/RDDNFT/reason-codes"

    payload = {
        "codeName": "TesteACW3",
        "codeType": "DISPOSITION",
        "description": "Just a Test 3"
    }

    headers = {
        'Content-Type': 'application/json',
        'authorization': f'Bearer {access_token}',
        'appkey': appkey
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    

# Main script
try:
    print(f"======== Obter Token ====================")
    access_token = get_access_token()
    print(f"Access Token : {access_token}")
    print(f"Autenticação realizada com sucesso! {access_token}")

    print(f"======== Adicionar um Disposition Code ====================")
    print(AddResonCode(access_token, appkey))

    print(f"======== OBTER UM USUARIO====================")
    print(GetUser(access_token, appkey))

    print(f"========= Listar Usuarios ===================")
    users = list_users(access_token, appkey)
    print("Users in the environment:")
    for user in users:
        print(user)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


print(f"Script executado com sucesso ! ")
