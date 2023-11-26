from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from sqlalchemy import Column, Integer, String
import hashlib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/antoan?charset=utf8mb4" % quote(
    'Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)


class User(db.Model):  # tạo bảng User để lưu thông tin đăng nhập
    __tablename__ = 'User'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    name = Column(String(100),nullable=False)
    password = Column(String(150), nullable=False)


def hash_password(password):
    with app.app_context():
        return hashlib.md5(password.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # u1 = User(username='a', name='van', password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()))
        # u2 = User(username='yanghara', name='myvan', password=str(hashlib.md5('abc'.encode('utf-8')).hexdigest()))
        # u3 = User(username='nhatthao', name='nhatthao',
        # password=str(hashlib.md5('thao123'.encode('utf-8')).hexdigest()))
        # u4 = User(username='TThuy', name='thanhthuy', password=str(hashlib.md5('thuyho'.encode('utf-8')).hexdigest()))
        # u5 = User(username='hnhi', name='hoangnhi',
        # password=str(hashlib.md5('hoangnhiprovip'.encode('utf-8')).hexdigest()))
        #
        # db.session.add_all([u2, u3, u4, u5])
        # db.session.commit()
