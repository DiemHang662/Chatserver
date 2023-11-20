from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


# Hàm này chạy trong một vòng lặp vô hạn để liên tục nhận tin nhắn từ máy chủ.
# Nếu có tin nhắn mới, nó sẽ hiển thị tin nhắn đó trên giao diện.


def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


# Hàm này được gọi khi người dùng muốn gửi một tin nhắn.
# Nó lấy nội dung từ ô nhập, gửi nó đến máy chủ thông qua socket và hiển thị nó trên giao diện.
# Nếu tin nhắn là "{quit}", nó sẽ đóng kết nối và thoát ứng dụng.


def on_closing(event=None):
    my_msg.set("{quit}")
    send()


# Hàm này được gọi khi người dùng đóng cửa sổ.
# Nó set nội dung tin nhắn thành "{quit}"
# gọi hàm send để đảm bảo thông báo "thoát" được gửi đến máy chủ trước khi đóng kết nối.


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Dùng để lưu nội dung tin nhắn sẽ gửi đi
my_msg.set("Nhập tên của bạn!.")
scrollbar = tkinter.Scrollbar(messages_frame)  # Dùng để cuộn lên để xem các tin nhắn trước đó

msg_list = tkinter.Listbox(messages_frame, height=15, width=50,
                           yscrollcommand=scrollbar.set)  # ListBoxd để chứa tin nhắn
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Gửi", command=send)  # nút gửi tin nhắn
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
# Tạo cửa sổ giao diện với các thành phần như Listbox để hiển thị tin nhắn,
# Entry để nhập tin nhắn và nút "Gửi" để gửi tin nhắn.


# Ket noi toi server
HOST = '127.0.0.1'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
# Xác định thông số kết nối và tạo một socket client để kết nối đến máy chủ.
# Sau đó, một luồng riêng biệt được khởi tạo để liên tục nhận tin nhắn từ máy chủ trong khi giao diện đồ họa đang chạy.
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
# Cuối cùng, tkinter.mainloop() được gọi để bắt đầu thực thi giao diện đồ họa.
