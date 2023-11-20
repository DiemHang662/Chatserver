from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    # Hàm này chịu trách nhiệm nhận kết nối từ các client.
    # Hàm chạy trong một vòng lặp vô hạn.
    # Khi một client kết nối, nó chấp nhận kết nối (SERVER.accept()) in ra địa chỉ của client
    # gửi một thông báo chào mừng đến client và
    # bắt đầu một luồng mới (Thread(target=handle_client, args=(client,)).start()) để xử lý giao tiếp với client đó.
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Nhập tên của bạn rồi bắt đầu chat!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    # Hàm này chịu trách nhiệm xử lý giao tiếp với một client cụ thể.
    # Nó nhận tên mà client chọn, gửi một thông báo chào mừng,
    # thông báo rằng một người dùng mới đã tham gia và thêm client vào dictionary clients
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Xin chào %s! Nếu bạn muốn thoát gõ, {quit} để thoát.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s đã tham gia phòng chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    # Sau đó, nó bắt đầu một vòng lặp để liên tục nhận các tin nhắn từ client.
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s đã thoát phòng chat." % name, "utf8"))
            break


# Nếu một client gửi "{quit}", nó đóng kết nối, xóa client khỏi danh sách và thông báo rằng người dùng đã rời đi.


def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


# Hàm này gửi một tin nhắn đến tất cả các client đã kết nối. prefix là một tham số tùy chọn để xác định tên.


clients = {}
addresses = {}
# clients và addresses là các từ điển để theo dõi các client đã kết nối và địa chỉ của chúng.
HOST = '127.0.0.1'
PORT = 33000
# HOST và PORT xác định địa chỉ IP và cổng mà máy chủ lắng nghe.
BUFSIZ = 1024
# BUFSIZ là kích thước bộ đệm.
ADDR = (HOST, PORT)
# SERVER là đối tượng socket của máy chủ, được liên kết với địa chỉ và cổng đã xác định.

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Chờ kết nối từ các client...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
