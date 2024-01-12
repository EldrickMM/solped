import requests

# Define the endpoint
url = 'https://api.amazon.com/auth/o2/token'

# Your credentials (from the security profile)
client_id = 'amzn1.application-oa2-client.5ca5a9b3b5e643d6bf89f8c0b1d2222f'
client_secret = 'amzn1.oa2-cs.v1.a2f73568e9436c94fe4a1a9acd8e8ff8c8badd92ab25b5625e8f1e1d5d8570a7'

# Define the header
headers = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

# Define the body of the POST request
body = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'alexa::proactive_events'  # Scope for Proactive Events API
}

# Send the POST request
response = requests.post(url, headers=headers, data=body)

# Print the access token
print(response.json())
print(response.json()['access_token'])
