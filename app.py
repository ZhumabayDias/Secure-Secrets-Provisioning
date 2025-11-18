import os

def get_secret_from_file():
    try:
        with open("secrets.conf", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_from_vault():
    try:
        import hvac
    except Exception:
        return None

    addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
    token = os.getenv("VAULT_TOKEN")
    if not token:
        return None

    client = hvac.Client(url=addr, token=token)
    try:
        resp = client.secrets.kv.v2.read_secret_version(path="myapp")
        return resp['data']['data'].get('MY_SECRET')
    except Exception:
        try:
            resp = client.secrets.kv.v1.read_secret(path="myapp")
            return resp['data'].get('MY_SECRET')
        except Exception:
            return None

def main():
    secret = os.getenv("MY_SECRET")
    if secret:
        source = "ENV"
    else:
        secret = get_secret_from_file()
        if secret:
            source = "file"
        else:
            secret = get_from_vault()
            if secret:
                source = "vault"
            else:
                source = None

    if secret == "letmein":
        print(f"App: Secret is correct — connected! (from {source})")
    else:
        print("App: No valid secret found.")
        print("    Current secret (raw):", repr(secret))
        print("    How to provide a secret:")
        print("      - Set environment variable: export MY_SECRET=letmein")
        print("      - Or create a file 'secrets.conf' with text: letmein")
        print("      - Or put secret into Vault at secret/data/myapp (KV v2) with key MY_SECRET")

if __name__ == "__main__":
    main()
PY