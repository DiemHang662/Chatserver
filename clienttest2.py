from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter  # tkinter là thư viện GUI của python,
# cung cấp một cách nhanh chóng và dễ dàng tạo ứng dụng trong python
from tkinter import messagebox  # import messagebox để hiển thị hộp thoại chú thông tin chỉ dẫn
from DB.dao import app  # Import 'app' từ module 'DB'
from DB.dao import User, hash_password  # Import database User và hàm băm mật khẩu từ Module 'DB'

logged_in = False  # mặc định khi bắt đầu chạy client trạng thái đăng nhập là false


def send(event=None):  # hàm gửi tin nhắn từ client
    raw_msg = my_msg.get()  # lấy nội dung tin nhắn từ ô nhập liệu
    my_msg.set("")  # xóa nội dung tin nhắn trong ô nhập liệu khi đã bấm nút gửi

    if logged_in: # nếu người dùng đã đăng nhập
        encrypted_msg = caesar_encrypt(raw_msg)  # mã hóa tin nhắn bằng hàm caesar_encrypt
        client_socket.send(bytes(encrypted_msg, "utf8"))  # gửi tin nhắn đã được mã hóa cho server
    else:  # nếu người dùng chưa đăng nhập

        client_socket.send(bytes(raw_msg, "utf8"))  #tin

    if raw_msg == "{quit}":  # nếu tin nhắn mà người dùng nhập là {quit}
        client_socket.close()  # đóng kết nối
        top.quit()  # đóng giao diện(thoát ứng dụng)


def receive():  # hàm nhận tin nhắn từ các client
    while True:  # lệnh while ám chỉ một vòng lặp để luôn nhận tin nhắn từ client
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")  # biến msg chứa tin nhắn mà client đã gửi
            # đã được gải mã từ dạng byte sang chuỗi nhờ utf8
            if logged_in:  # nếu trạng thái đăng nhập là false
                decrypted_msg = caesar_decrypt(msg)  # tin nhắn được giải mã tại client bằng hàm giải mã
                msg_list.insert(tkinter.END, decrypted_msg)  # tin nhắn được giải mã ở trên được gắn vào
                # cuối listbox trên giao diện tin nhắn
            else: # nếu người dùng chưa đăng nhập
                msg_list.insert(tkinter.END, msg)
        except OSError:  # quăng ngoại lệ để bắt lỗi
            break


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


def on_closing(event=None):  # hàm đóng khi người dùng bấm vào 'X' trên giao diện
    my_msg.set("{quit}")  # tạo thông điệp {quit} để đóng kết nối và thoát ứng dụng
    send()


def login():
    name = entry_field.get()  # lấy tên đăng nhập từ ô nhập liệu
    if name:  # kiểm tra có tên đăng nhập hay không, nếu có thì có nghĩa người dùng đã đăng nhập
        entry_field.config(state=tkinter.DISABLED)  # vô hiệu hóa ô nhập liệu
        login_button.config(state=tkinter.DISABLED)  # vô hiệu hóa nút đăng nhập để không thể đăng nhập lần 2
        send_button.config(state=tkinter.NORMAL)  # bật nút gửi lên để người dùng có thể gửi tin nhắn
        client_socket.send(bytes(name, "utf8"))  # gửi tên đăng nhập lên server


def open_login_window():  # tạo giao diện đăng nhập
    global login_window  # Khai báo biến login_window là biến toàn cục để có thể sử dụng nó sau này trong các hàm khác.
    login_window = tkinter.Toplevel(top)  # tạo một cửa sổ con với vị trí top
    login_window.title("Đăng nhập")  # cửa sổ ấy có tên đăng nhập

    # Thiết lập kích thước của cửa sổ đăng nhập
    login_window.geometry("300x160")

    frame = tkinter.Frame(login_window, padx=20, pady=20)
    # Tạo một Frame để chứa các widget trong cửa sổ đăng nhập với viền padding 20 pixel.
    frame.pack(expand=True, fill="both")

    login_label = tkinter.Label(frame, text="Nhập tên đăng nhập:") # tạo một label có tên "Nhập tên đăng nhập:"
    login_label.grid(row=0, column=0, pady=10) # vị trí label ở cột 0 hàng 0 với padding là 10 pixel

    login_entry = tkinter.Entry(frame)  # tạo một ô nhập liệu để mật tên đăng nhập
    login_entry.grid(row=0, column=1, pady=10, padx=10) # vị trí của ô nhập liệu ở cột 1 hàng 0

    login_label_password = tkinter.Label(frame, text="Nhập mật khẩu:") # tạo một label có tên "Nhập mật khẩu:"
    login_label_password.grid(row=1, column=0, pady=10) # với vị trí cột 1 hàng 0

    login_entry_password = tkinter.Entry(frame, show="*") # tạo một ô nhập liệu để nhập mật khẩu với kí tự che dấu mật khẩu là *
    login_entry_password.grid(row=1, column=1, pady=10, padx=10) # với vị trí cột 1 hàng 1

    login_button = tkinter.Button(frame, text="Đăng nhập",
                                  command=lambda: login_and_close(login_entry.get(), login_entry_password.get()))
    # tạo 1 button có tên là Đăng nhập, khi người dùng đã nhập tên và mật khẩu
    # với hàm callback lamda để gọi hàm login_and_close và truyền tên đăng nhập và mật khẩu đã nhập.
    login_button.grid(row=2, column=0, columnspan=2, pady=20) # với vị trí hàng 0 cột 2


def login_and_close(username, password):
    global logged_in # sử dụng biến toàn cục logged_in
    if not username or not password:
        # Hiển thị thông báo lỗi nếu một trong hai trường bị bỏ trống
        messagebox.showerror("Login Failed", "Vui lòng nhập cả tên đăng nhập và mật khẩu.")
        return

    if validate_login(username, password):
        # nếu đăng nhập thành công
        login_window.destroy() # đóng cửa sổ đăng nhập
        entry_field.config(state=tkinter.NORMAL) # kích hoạt ô nhập liệu để nhập tin nhắn
        login_button.config(state=tkinter.DISABLED) # vô hiệu hóa nút đăng nhập
        send_button.config(state=tkinter.NORMAL) # kích hoạt lại nút gửi
        client_socket.send(bytes(username, "utf8")) # gửi username lên server
        logged_in = True # cập nhật lại trạng thái đăng nhập là true
    else: # nếu đăng nhập sai thì thông báo cho người dùng
        messagebox.showerror("Login Failed", "Tên đăng nhập hoặc mật khẩu không đúng.")


def validate_login(username, password):
    with app.app_context():  # Truy vấn cơ sở dữ liệu để kiểm tra người dùng
        user = User.query.filter_by(username=username, password=hash_password(password)).first()

        # Trả về True nếu người dùng tồn tại và mật khẩu đúng, ngược lại là False
        return user is not None


top = tkinter.Tk()
top.title("Chat Room Client 1")  # tên của ứng dụng

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar() # tạo một biến để theo dõi tin nhắn trong ô nhập liệu
my_msg.set("Nhập tin nhắn của bạn!")
scrollbar = tkinter.Scrollbar(messages_frame) # tạo thanh cuộn để cuộn xem tin nhắn ở phía trên
msg_list = tkinter.Listbox(messages_frame, height=30, width=75, yscrollcommand=scrollbar.set)
# tạo listbox để chứa tin nhắn với chiều dài 30 độ rộng 75
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y) # đặt thanh cuộn ở bên phải listbox
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH) # đặt listbox ở bên trái và mở rộng ra hai bên
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg) # tạo một ô nhập liệu
entry_field.pack()

login_button = tkinter.Button(top, text="Đăng nhập", command=open_login_window) # tạo một nút đăng nhập
login_button.pack()

send_button = tkinter.Button(top, text="Gửi", state=tkinter.DISABLED, command=send) # tạo một nút gửi
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
# Đặt hàm on_closing làm hàm callback khi người dùng đóng cửa sổ gốc

# Kết nối đến máy chủ
HOST = '127.0.0.1' # địa chỉ ip của máy chủ, ở đây là localhost
PORT = 33000 # số cổng sử dụng kết nối
if not PORT: # kiểm tra port có tồn tại ko
    PORT = 33000 # nếu ko gán nó vào 33000
else:
    PORT = int(PORT) # nếu có thì chuyển nó thành số nguyên

BUFSIZ = 1024
# BUFSIZ là kích thước bộ đệm
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR) # Kết nối đến địa chỉ và cổng của server bằng cách sử dụng phương thức connect() của socket.

receive_thread = Thread(target=receive)
# Điều này được thực hiện để có thể đọc tin nhắn từ server
# trong khi vẫn có thể gửi tin nhắn từ giao diện người dùng mà không làm đứng chương trình chính.
receive_thread.start()
tkinter.mainloop()
# giữ cho giao diện người dùng luôn mở và có thể tương tác với người dùng