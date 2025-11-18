import os

def get_secret_from_file():
    try:
        with open("secrets.conf", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
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
            source = None

    if secret == "letmein":
        print(f"App: Secret is correct — connected! (from {source})")
    else:
        print("App: No valid secret found.")
        print("    Current secret (raw):", repr(secret))
        print("    How to provide a secret:")
        print("      - Set environment variable: export MY_SECRET=letmein")
        print("      - Or create a file 'secrets.conf' with text: letmein")

if __name__ == "__main__":
    main()