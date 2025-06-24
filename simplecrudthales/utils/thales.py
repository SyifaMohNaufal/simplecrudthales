import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from utils import vault

if vault.VAULT_TOKEN == None:
    vault.auth_approle()

secrets_tokenize = vault.get_secret("Demo-Thales", "demo.users/tokenize")
secrets_detokenize = vault.get_secret("Demo-Thales", "demo.users/detokenize")
secrets_detokenize_masking = vault.get_secret("Demo-Thales", "demo.users/detokenize.masking")
usrnm_t = secrets_tokenize["user"]
psswd_t = secrets_tokenize["pass"]
usrnm_dt = secrets_detokenize["user"]
psswd_dt = secrets_detokenize["pass"]
usrnm_dtm = secrets_detokenize["user"]
psswd_dtm = secrets_detokenize["pass"]

THALES_BASE_URL = settings.THALES_BASE_URL

THALES_TOKEN_GROUP = settings.THALES_TOKEN_GROUP
THALES_TOKEN_TEMPLATE = settings.THALES_TOKEN_TEMPLATE

def thales_encrypt(plaintext):
    url = f"{THALES_BASE_URL}/vts/rest/v2.0/tokenize"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "tokengroup":THALES_TOKEN_GROUP,
        "data":plaintext,
        "tokentemplate":THALES_TOKEN_TEMPLATE
    }
    print("plaintext:", plaintext)
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(usrnm_t, psswd_t), verify=False)
    response.raise_for_status()
    if response.json()["status"] != "error":
        print("response thales:", response.json())
        return response.json()["token"]
    else:
        return plaintext
    

def thales_decrypt(ciphertext):
    url = f"{THALES_BASE_URL}/vts/rest/v2.0/detokenize"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "tokengroup":THALES_TOKEN_GROUP,
        "token":ciphertext,
        "tokentemplate":THALES_TOKEN_TEMPLATE
    }
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(usrnm_dt, psswd_dt), verify=False)
    response.raise_for_status()
    if response.json()["status"] != "error":
        return response.json()["data"]
    else:
        return ciphertext

def thales_decrypt_masking(ciphertext):
    url = f"{THALES_BASE_URL}/vts/rest/v2.0/detokenize"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "tokengroup":THALES_TOKEN_GROUP,
        "token":ciphertext,
        "tokentemplate":THALES_TOKEN_TEMPLATE
    }
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(usrnm_dtm, psswd_dtm), verify=False)
    response.raise_for_status()
    if response.json()["status"] != "error":
        return response.json()["data"]
    else:
        return ciphertext
