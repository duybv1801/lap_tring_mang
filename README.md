# 💬 Chương Trình Chat Mạng LAN (CLI)

**Mô tả:**
Chương trình cho phép các máy tính trong cùng mạng LAN giao tiếp với nhau qua giao diện dòng lệnh (CLI). Chương trình được xây dựng theo mô hình **Client-Server** sử dụng giao thức **TCP**.

**Công nghệ & Kiến trúc:**
* **Ngôn ngữ:** Python 3
* **Giao thức:** **TCP Sockets** (thư viện `socket`)
* **Xử lý đồng thời:** **Đa luồng** (`threading`). Server sử dụng đa luồng để xử lý nhiều kết nối client cùng lúc, và Client dùng luồng riêng để nhận tin không bị chặn.

---

### Hướng Dẫn Vận Hành

Chương trình cần được chạy trên ít nhất hai máy hoặc hai cửa sổ terminal khác nhau.

#### 1. Khởi động Server (`server.py`)

Server phải được chạy trên một máy chủ cố định.

1.  Mở Terminal/Command Prompt trên máy chủ.
2.  Chạy lệnh với địa chỉ IP (của máy chủ) và Port.
    * **Lệnh:** `python3 server.py [HOST_IP] [PORT]`
    * **Ví dụ (Lắng nghe mọi kết nối):** `python3 server.py 0.0.0.0 5000`
3.  **Output:** `Server lắng nghe trên <HOST_IP>:<PORT>`

#### 2. Khởi động Client (`client.py`)

Client có thể chạy trên cùng hoặc các máy khác trong mạng, cần biết IP của Server.

1.  Mở Terminal/Command Prompt trên máy Client.
2.  Chạy lệnh với địa chỉ IP của Server và Port:
    * **Lệnh:** `python3 client.py <SERVER_IP> [PORT]`
    * **Ví dụ:** `python3 client.py 192.168.1.100 5000`
3.  Client sẽ hỏi tên người dùng, sau đó bạn có thể bắt đầu chat.
4.  **Lưu ý:** Nếu chạy file `.exe` hoặc không truyền tham số, chương trình sẽ hỏi IP và Port một cách tương tác.

---

### Các Lệnh Chat (Commands)

Sau khi kết nối và nhập tên, client có thể sử dụng các lệnh sau:

| Lệnh | Chức năng | Tham số |
| :--- | :--- | :--- |
| **Tin nhắn thường** | Gửi tin nhắn đến tất cả người dùng đang online (Broadcast). | - |
| **`/list`** | Hiển thị danh sách tên người dùng đang online. | - |
| **`/pm <name> <msg>`** | Gửi tin nhắn riêng (Private Message) đến `<name>`. | `<name>`, `<msg>` |
| **`/quit`** | Ngắt kết nối và thoát khỏi chương trình. | - |