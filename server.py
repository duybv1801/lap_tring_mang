#!/usr/bin/env python3
"""
server.py - Simple LAN chat server (TCP, threaded)
Usage: python3 server.py [HOST] [PORT]
Example: python3 server.py 0.0.0.0 5000
"""
import socket
import threading
import sys

HOST = sys.argv[1] if len(sys.argv) >= 2 else "0.0.0.0"
PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 5000

# Global state
clients_lock = threading.Lock()
clients = {}  # sock -> {"name": str, "addr": (ip,port)}

def broadcast(msg, except_sock=None):
    """Gửi msg (bytes) đến tất cả client trừ except_sock."""
    with clients_lock:
        for sock in list(clients.keys()):
            if sock is except_sock:
                continue
            try:
                sock.sendall(msg)
            except Exception:
                remove_client(sock)

def send_to(sock, msg):
    try:
        sock.sendall(msg)
    except Exception:
        remove_client(sock)

def remove_client(sock):
    with clients_lock:
        info = clients.pop(sock, None)
    if info:
        name = info.get("name", "<unknown>")
        print(f"[DISCONNECT] {name} {info['addr']}")
        broadcast(f"*** {name} đã rời phòng.\n".encode('utf-8'))

def handle_client(sock, addr):
    try:
        sock.sendall("Welcome! Hãy gửi tên của bạn:\n".encode('utf-8'))

        name = sock.recv(1024).decode('utf-8').strip()
        if not name:
            sock.sendall("Name không hợp lệ. Đóng kết nối.\n".encode('utf-8'))
            sock.close()
            return
        with clients_lock:
            clients[sock] = {"name": name, "addr": addr}
        print(f"[CONNECT] {name} {addr}")
        broadcast(f"*** {name} đã tham gia phòng.\n".encode('utf-8'), except_sock=sock)
        sock.sendall("--- Bạn có thể chat. Lệnh: /list, /pm <name> <msg>, /quit ---\n".encode('utf-8'))
        # Read loop
        while True:
            data = sock.recv(4096)
            if not data:
                break
            text = data.decode('utf-8').strip()
            if not text:
                continue
            # Handle commands
            if text.startswith("/"):
                parts = text.split(" ", 2)
                cmd = parts[0].lower()
                if cmd == "/quit":
                    sock.sendall(b"Bye\n")
                    break
                elif cmd == "/list":
                    with clients_lock:
                        names = [info["name"] for s, info in clients.items()]
                    sock.sendall(f"Online: {', '.join(names)}\n".encode('utf-8'))
                elif cmd == "/pm" and len(parts) >= 3:
                    target_name = parts[1]
                    msgbody = parts[2]
                    sent = False
                    with clients_lock:
                        for s, info in clients.items():
                            if info["name"] == target_name:
                                send_to(s, f"[PM từ {clients[sock]['name']}] {msgbody}\n".encode('utf-8'))
                                sent = True
                                break
                    if sent:
                        sock.sendall("[PM gửi]\n".encode('utf-8'))
                    else:
                        sock.sendall("[Lỗi] Không tìm thấy người nhận.\n".encode('utf-8'))
                else:
                    sock.sendall("[Lỗi] Lệnh không hợp lệ.\n".encode('utf-8'))
            else:
                # Broadcast normal message
                name = clients[sock]["name"]
                broadcast_msg = f"{name}: {text}\n".encode('utf-8')
                broadcast(broadcast_msg, except_sock=None)
    except Exception as e:
        print(f"[ERROR] Client handler error: {e}")
    finally:
        try:
            remove_client(sock)
        except:
            pass
        try:
            sock.close()
        except:
            pass

def accept_loop(server_sock):
    print(f"Server lắng nghe trên {HOST}:{PORT}")
    while True:
        try:
            sock, addr = server_sock.accept()
            t = threading.Thread(target=handle_client, args=(sock, addr), daemon=True)
            t.start()
        except KeyboardInterrupt:
            print("Server dừng bằng Ctrl-C")
            break
        except Exception as e:
            print("Accept error:", e)

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(100)
    try:
        accept_loop(server_sock)
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()
