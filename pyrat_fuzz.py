import itertools
import string
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

if len(sys.argv) < 3:
    print('[x] Missing arguments !')
    print('[>] Usage: python3 exploit.py <ip> <port>')
    print('[>] Example: python3 exploit.py 192.168.1.24 8080')
    sys.exit(0)

host = sys.argv[1]
port = sys.argv[2]
thread = int(sys.argv[3]) if len(sys.argv) > 3 else 20

BASE_URL = f"http://{host}:{port}/"
MIN_LENGTH = 1
MAX_LENGTH = 3
CHARSET = string.ascii_lowercase + string.digits
TIMEOUT = 3

def check_url(path):
    url = BASE_URL + path
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response_text = response.text
        if response_text != 'Try a more basic connection' :
            print(f"[✅ FOUND] {url} => {path}")
    except requests.RequestException as e:
        print(f"[💥 ERROR] {url} => {e}")


def generate_paths():
    for length in range(MIN_LENGTH, MAX_LENGTH + 1):
        for combo in itertools.product(CHARSET, repeat=length):
            yield ''.join(combo)

def main():
    with ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(check_url, path) for path in generate_paths()]
        for future in as_completed(futures):
            pass 

if __name__ == "__main__":
    print(f"[i] Starting fuzzing on {BASE_URL} with charset '{CHARSET}' and lengths from {MIN_LENGTH} to {MAX_LENGTH}. Using {thread} threads.")
    main()
    print("[i] Fuzzing completed.")