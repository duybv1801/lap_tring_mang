#!/usr/bin/env python3
"""
client.py - Simple CLI chat client for the chat server.
Usage:
    python3 client.py <SERVER_IP> [PORT]
Example:
    python3 client.py 192.168.1.10 5000
If chạy file .exe, người dùng sẽ được hỏi IP và port.
"""

import socket
import sys
import threading

def get_server_info():
    """Lấy IP và port từ argv hoặc hỏi người dùng."""
    try:
        server = sys.argv[1]
        port = int(sys.argv[2]) if len(sys.argv) >= 3 else 5000
    except (IndexError, ValueError):
        print("Không tìm thấy tham số dòng lệnh. Hãy nhập thủ công.")
        server = input("Nhập IP của server (mặc định 127.0.0.1): ") or "127.0.0.1"
        try:
            port = int(input("Nhập port (mặc định 5000): ") or "5000")
        except ValueError:
            port = 5000
    return server, port


def recv_loop(sock):
    """Luồng nhận dữ liệu từ server."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("\n[Kết nối đóng bởi server]")
                break
            print(data.decode("utf-8"), end="")
    except Exception as e:
        print("\n[Lỗi nhận dữ liệu:]", e)
    finally:
        try:
            sock.close()
        except:
            pass
        input("\nNhấn Enter để thoát...")
        sys.exit(0)


def main():
    SERVER, PORT = get_server_info()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER, PORT))
    except Exception as e:
        print(f"Không thể kết nối tới server {SERVER}:{PORT} — lỗi: {e}")
        input("\nNhấn Enter để thoát...")
        return

    print(f"Kết nối thành công tới {SERVER}:{PORT}!\n")

    # Bắt đầu luồng nhận tin
    threading.Thread(target=recv_loop, args=(sock,), daemon=True).start()

    try:
        name = input("Tên của bạn: ").strip()
        if not name:
            print("Tên không thể rỗng.")
            sock.close()
            return
        sock.sendall((name + "\n").encode("utf-8"))

        while True:
            line = input()
            if line == "":
                continue
            sock.sendall((line + "\n").encode("utf-8"))
            if line.strip().lower() == "/quit":
                print("Đã thoát.")
                break
    except (KeyboardInterrupt, EOFError):
        try:
            sock.sendall(b"/quit\n")
        except:
            pass
    finally:
        try:
            sock.close()
        except:
            pass
        input("Nhấn Enter để thoát...")  # tránh cửa sổ tắt ngay khi build exe


if __name__ == "__main__":
    main()
