import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


THALES_BASE_URL = settings.THALES_BASE_URL

THALES_TOKEN_GROUP = settings.THALES_TOKEN_GROUP
THALES_TOKEN_TEMPLATE = settings.THALES_TOKEN_TEMPLATE

THALES_TOKENIZE_USER = settings.THALES_TOKENIZE_USER
THALES_TOKENIZE_PASS = settings.THALES_TOKENIZE_PASS

THALES_DETOKENIZE_USER = settings.THALES_DETOKENIZE_USER
THALES_DETOKENIZE_PASS = settings.THALES_DETOKENIZE_PASS

THALES_DETOKENIZE_MASKING_USER = settings.THALES_DETOKENIZE_MASKING_USER
THALES_DETOKENIZE_MASKING_PASS = settings.THALES_DETOKENIZE_MASKING_PASS



def thales_encrypt(plaintext):
    url = f"{THALES_BASE_URL}/vts/rest/v2.0/tokenize"
    print("url:", url)
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "tokengroup":THALES_TOKEN_GROUP,
        "data":plaintext,
        "tokentemplate":THALES_TOKEN_TEMPLATE
    }
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(THALES_TOKENIZE_USER, THALES_TOKENIZE_PASS), verify=False)
    response.raise_for_status()
    print(response.status_code)
    print("response encrypt:", response.json())
    if response.json()["status"] != "error":
        return response.json()["token"]
    else:
        return plaintext
    

def thales_decrypt(ciphertext):
    url = f"{THALES_BASE_URL}/vts/rest/v2.0/detokenize"
    print("url:", url)
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "tokengroup":THALES_TOKEN_GROUP,
        "token":ciphertext,
        "tokentemplate":THALES_TOKEN_TEMPLATE
    }
    print("data:", data)
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(THALES_DETOKENIZE_USER, THALES_DETOKENIZE_PASS), verify=False)
    response.raise_for_status()
    print("response decrypt:", response.json())
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
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(THALES_DETOKENIZE_MASKING_USER, THALES_DETOKENIZE_MASKING_PASS), verify=False)
    response.raise_for_status()
    if response.json()["status"] != "error":
        return response.json()["data"]
    else:
        return ciphertext
