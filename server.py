from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def caesar_encrypt(text, shift=3):  # hàm mã hóa tin nhắn bằng thuật toán caesar với khóa mặc định là 3
    result = ""  # khởi tạo một chuỗi kết quả để lưu kết quả mã hóa
    for char in text:  # duyệt qua từng ký tự trong text
        if char.isalpha():  # nếu ký tự ấy có phải là ký tự chữ cái hay không
            if char.islower():  # nếu ký tự ấy là chữ cái viết thường
                result += chr((ord(char) + shift - ord('a')) % 26 + ord('a'))
                # chuyển đổi giá trị Unicode của ký tự, thực hiện phép tính dịch chuyển với shift
                # sau đó chuyển đổi trở lại thành ký tự chữ thường.
                # %26 là để đảm bảo chữ cái ấy trong phạm vi 26 chữ cái trong bảng chữ cái tiếng anh
            else:  # nếu ký tự ấy là chữ cái viết hoa
                result += chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
                # chuyển đổi giá trị Unicode của ký tự, thực hiện phép tính dịch chuyển với shift
                # sau đó chuyển đổi trở lại thành ký tự chữ hoa.
                # %26 là để đảm bảo chữ cái ấy trong phạm vi 26 chữ cái trong bảng chữ cái tiếng anh
        else:  # nếu nó không phải là chữ cái
            result += char  # giữ nguyễn ký tự ấy vào kết quả
    return result  # trả về kết quả chuỗi đã mã hóa


def caesar_decrypt(text, shift=3):  # hàm giải mã tin nhắn bằng thuật toán caesar với khóa mặc định là 3
    result = ""  # khởi tạo một chuỗi kết quả để lưu kết quả giải mã
    for char in text:  # duyệt qua từng ký tự trong text
        if char.isalpha():  # nếu ký tự ấy có phải là ký tự chữ cái hay không
            if char.islower():   # nếu ký tự ấy là chữ cái viết thường
                result += chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
                # chuyển đổi giá trị Unicode của ký tự, thực hiện phép tính dịch chuyển với shift
                # sau đó chuyển đổi trở lại thành ký tự chữ thường.
                # %26 là để đảm bảo chữ cái ấy trong phạm vi 26 chữ cái trong bảng chữ cái tiếng anh
            else:  # nếu ký tự ấy là chữ cái viết hoa
                result += chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
                # chuyển đổi giá trị Unicode của ký tự, thực hiện phép tính dịch chuyển với shift
                # sau đó chuyển đổi trở lại thành ký tự chữ hoa.
                # %26 là để đảm bảo chữ cái ấy trong phạm vi 26 chữ cái trong bảng chữ cái tiếng anh
        else:   # nếu nó không phải là chữ cái
            result += char  # giữ nguyễn ký tự ấy vào kết quả
    return result  # trả về kết quả chuỗi đã giải mã


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
    welcome = 'Hello %s! If you want to leave the chat, {quit} to leave.' % name
    client.send(bytes(caesar_encrypt(welcome), "utf8"))

    msg = "%s has joined the chat room!" % name
    broadcast(bytes(caesar_encrypt(msg), "utf8"),prefix="")
    clients[client] = name
    # Sau đó, nó bắt đầu một vòng lặp để liên tục nhận các tin nhắn từ client.
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, caesar_encrypt(name) + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            msg = "%s has left the chat room." % name
            broadcast(bytes(msg, "utf8"), prefix="")
            break

# Nếu một client gửi "{quit}",
# nó đóng kết nối, xóa client khỏi danh sách và thông báo rằng người dùng đã rời đi.


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
