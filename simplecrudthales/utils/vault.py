from django.conf import settings
import requests

VAULT_TOKEN = None

def auth_approle():
    global VAULT_TOKEN
    try:
        url = settings.VAULT_ADDR + "/v1/auth/approle/login"
        headers = {
            "X-Vault-Namespace": settings.VAULT_NAMESPACE,
            "Content-Type": "application/json"
        }
        data = {
            "role_id": settings.VAULT_ROLE_ID,
            "secret_id": settings.VAULT_SECRET_ID
        }
        post = requests.post(url=url, headers=headers, json=data)
        vault_resp = post.json()
        VAULT_TOKEN = vault_resp['auth']['client_token']
        return vault_resp  # ✅ return raw response data
    except Exception as e:
        raise Exception(f"Vault approle auth failed: {str(e)}")

def get_secret(mount_point, secret_path):
    try:
        url = f"{settings.VAULT_ADDR}/v1/{mount_point}/data/{secret_path}"
        headers = {
            "X-Vault-Namespace": settings.VAULT_NAMESPACE,
            "X-Vault-Token": VAULT_TOKEN,
            "Content-Type": "application/json"
        }
        get = requests.get(url=url, headers=headers)
        vault_resp = get.json()
        return vault_resp["data"]["data"]  # ✅ return only secret values
    except Exception as e:
        raise Exception(f"Vault get_secret failed: {str(e)}")
