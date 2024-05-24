import tkinter as tk
from tkinter import filedialog, messagebox
from pyzbar.pyzbar import decode
import cv2
import csv
import qrcode
from PIL import Image, ImageTk
import barcode
from barcode.writer import ImageWriter

class QRCodeGenerator:
    def __init__(self, master, admin):
        self.master = master
        self.master.title("二维码和条形码生成系统")
        self.master.geometry("800x730")

        # 快递单号
        self.label_tracking = tk.Label(master, text="快递单号")
        self.label_tracking.pack()
        self.entry_tracking = tk.Entry(master)
        self.entry_tracking.pack()

        # 寄件人姓名
        self.label_sender_name = tk.Label(master, text="寄件人姓名")
        self.label_sender_name.pack()
        self.entry_sender_name = tk.Entry(master)
        self.entry_sender_name.pack()

        # 寄件人地址
        self.label_sender_address = tk.Label(master, text="寄件人地址")
        self.label_sender_address.pack()
        self.entry_sender_address = tk.Entry(master)
        self.entry_sender_address.pack()

        # 寄件人电话
        self.label_sender_phone = tk.Label(master, text="寄件人电话")
        self.label_sender_phone.pack()
        self.entry_sender_phone = tk.Entry(master)
        self.entry_sender_phone.pack()

        # 收件人姓名
        self.label_receiver_name = tk.Label(master, text="收件人姓名")
        self.label_receiver_name.pack()
        self.entry_receiver_name = tk.Entry(master)
        self.entry_receiver_name.pack()

        # 收件人地址
        self.label_receiver_address = tk.Label(master, text="收件人地址")
        self.label_receiver_address.pack()
        self.entry_receiver_address = tk.Entry(master)
        self.entry_receiver_address.pack()

        # 收件人电话
        self.label_receiver_phone = tk.Label(master, text="收件人电话")
        self.label_receiver_phone.pack()
        self.entry_receiver_phone = tk.Entry(master)
        self.entry_receiver_phone.pack()

        # 生成二维码按钮
        self.qr_button = tk.Button(master, text="生成二维码", command=self.generate_qr)
        self.qr_button.pack()

        # 生成条形码按钮
        self.barcode_button = tk.Button(master, text="生成条形码", command=self.generate_barcode)
        self.barcode_button.pack()

        # 保存按钮
        self.save_button = tk.Button(master, text="保存", command=self.save)
        self.save_button.pack()

        # 图片显示区
        self.canvas = tk.Canvas(master, width=300, height=300)
        self.canvas.pack()

        # 二维码和条形码图片初始化
        self.qr_image = None
        self.barcode_image = None

        self.admin = admin
        # 添加返回按钮
        self.back_button = tk.Button(master, text="返回", command=self.back)
        self.back_button.pack()

    def back(self):
        # 关闭当前窗口并打开选择功能界面
        self.master.destroy()
        root = tk.Tk()
        if self.admin:
            app = AdminApplication(root)
        else:
            app = UserApp(root)
        root.mainloop()

    def generate_qr(self):
        # 获取输入的信息
        tracking_number = self.entry_tracking.get()
        sender_name = self.entry_sender_name.get()
        sender_address = self.entry_sender_address.get()
        sender_phone = self.entry_sender_phone.get()
        receiver_name = self.entry_receiver_name.get()
        receiver_address = self.entry_receiver_address.get()
        receiver_phone = self.entry_receiver_phone.get()

        # 将所有信息组合到一起
        info = f'{tracking_number}\n{sender_name}\n{sender_address}\n{sender_phone}\n{receiver_name}\n{receiver_address}\n{receiver_phone}'

        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(info)
        qr.make(fit=True)

        self.qr_image = qr.make_image(fill='black', back_color='white')

        # 显示二维码
        qr_img_tk = ImageTk.PhotoImage(self.qr_image)
        self.canvas.create_image(150, 150, image=qr_img_tk)
        self.canvas.image = qr_img_tk

    def generate_barcode(self):
        # 获取快递单号
        tracking_number = self.entry_tracking.get()

        # 生成条形码
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(tracking_number, writer=ImageWriter())
        self.barcode_image = ean.render()

    def save(self):
        # 保存二维码和条形码
        if self.qr_image is not None:
            self.qr_image.save('qrcode.png')
        if self.barcode_image is not None:
            self.barcode_image.save('barcode.png')
        messagebox.showinfo("成功", "二维码和条形码已保存")

def register(username, password, admin=False):
    # 读取现有的用户数据
    users = read_users_from_csv()
    if username in users:
        return False
    else:
        # 添加新用户
        users[username] = {'password': password, 'admin': admin}
        # 保存用户数据到csv文件中
        save_users_to_csv(users)
        return True

def login(username, password):
    # 读取现有的用户数据
    users = read_users_from_csv()
    if username not in users or users[username]['password'] != password:
        return False, False
    else:
        return True, users[username]['admin']


def read_users_from_csv():
    users = {}
    try:
        with open('users.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                users[row[0]] = {'password': row[1], 'admin': row[2] == 'True'}
    except FileNotFoundError:
        pass
    return users


def save_users_to_csv(users):
    with open('users.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for username, data in users.items():
            writer.writerow([username, data['password'], data['admin']])


def decode_barcode(image_path):
    img = cv2.imread(image_path)
    barcodes = decode(img)
    barcode_data = [barcode.data.decode('utf-8').split('\n') for barcode in barcodes]
    return barcode_data


class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("条形码识别系统登录注册界面")
        self.master.geometry("400x200")

        self.label_username = tk.Label(master, text="用户名")
        self.label_username.pack()
        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="密码")
        self.label_password.pack()
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        self.admin_check = tk.IntVar()  # 管理员注册标记
        self.check_button = tk.Checkbutton(master, text="管理员注册", variable=self.admin_check)
        self.check_button.pack()

        self.login_button = tk.Button(master, text="登录", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(master, text="注册", command=self.register)
        self.register_button.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        login_status, admin = login(username, password)
        if login_status:
            messagebox.showinfo("成功", "登录成功")
            self.master.destroy()
            root = tk.Tk()
            if admin:
                app = AdminApplication(root)  # 管理员登录后打开管理员界面
            else:
                app = UserApp(root)  # 普通用户登录后打开二维码识别界面
            root.mainloop()
        else:
            messagebox.showerror("失败", "错误的用户名或密码")

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        admin = self.admin_check.get() == 1  # 获取是否管理员注册

        if register(username, password, admin):
            messagebox.showinfo("成功", "注册成功")
        else:
            messagebox.showerror("失败", "用户名已存在")

class QRCodeRecognition:
    def __init__(self, master, admin):
        self.master = master
        self.master.title("二维码识别系统")

        self.label = tk.Label(master, text="请点击上传一张二维码图像")
        self.label.pack()

        self.button = tk.Button(master, text="上传图像", command=self.upload_image)
        self.button.pack()

        self.text = tk.Text(master)
        self.text.pack()

        self.canvas = tk.Canvas(master, width=300, height=300)  # 用于显示二维码的画布
        self.canvas.pack()

        self.open_csv()

        self.admin = admin
        # 添加返回按钮
        self.back_button = tk.Button(master, text="返回", command=self.back)
        self.back_button.pack()

    def back(self):
        # 关闭当前窗口并打开选择功能界面
        self.master.destroy()
        root = tk.Tk()
        if self.admin:
            app = AdminApplication(root)
        else:
            app = UserApp(root)
        root.mainloop()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        barcode_data = decode_barcode(file_path)

        for data in barcode_data:
            for item in data:
                self.text.insert(tk.END, item + "\n")

        self.save_to_csv(barcode_data)

        img = Image.open(file_path)
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(150, 150, image=img_tk)
        self.canvas.image = img_tk

    def save_to_csv(self, data):
        with open('output.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)

    # 在打开文件时，添加标题行
    def open_csv(self):
        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['快递单号', '寄件人姓名', '寄件地址','寄件人电话', '收件人姓名', '收件地址','收件人电话'])


class PackageLookup:
    def __init__(self, master, admin):
        self.master = master
        self.master.title("快递查询")

        self.label_tracking = tk.Label(master, text="快递单号")
        self.label_tracking.pack()

        self.entry_tracking = tk.Entry(master)
        self.entry_tracking.pack()

        self.lookup_button = tk.Button(master, text="查询", command=self.lookup)
        self.lookup_button.pack()

        self.text = tk.Text(master)
        self.text.pack()
        self.admin = admin
        # 添加返回按钮
        self.back_button = tk.Button(master, text="返回", command=self.back)
        self.back_button.pack()

    def back(self):
        # 关闭当前窗口并打开选择功能界面
        self.master.destroy()
        root = tk.Tk()
        if self.admin:
            app = AdminApplication(root)
        else:
            app = UserApp(root)
        root.mainloop()

    def lookup(self):
        tracking_number = self.entry_tracking.get()

        with open('output.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == tracking_number:
                    self.text.delete('1.0', tk.END)
                    self.text.insert(tk.END, '\n'.join(row))
                    return
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, "无法找到该快递单号的信息")


class UserApp:
    def __init__(self, master):
        self.master = master
        self.master.title("普通用户界面")

        self.recog_button = tk.Button(master, text="识别二维码", command=self.open_qr_recognition)
        self.recog_button.pack()

        self.lookup_button = tk.Button(master, text="查询快递", command=self.open_package_lookup)
        self.lookup_button.pack()

    def open_qr_recognition(self):
        self.master.destroy()
        root = tk.Tk()
        app = QRCodeRecognition(root, admin=False)
        root.mainloop()

    def open_package_lookup(self):
        self.master.destroy()
        root = tk.Tk()
        app = PackageLookup(root, admin=False)
        root.mainloop()


class AdminApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("管理员界面")

        self.qr_button = tk.Button(master, text="生成二维码", command=self.open_qr_generator)
        self.qr_button.pack()

        self.recog_button = tk.Button(master, text="识别二维码", command=self.open_qr_recognition)
        self.recog_button.pack()

        self.lookup_button = tk.Button(master, text="查询快递", command=self.open_package_lookup)
        self.lookup_button.pack()

    def open_qr_generator(self):
        self.master.destroy()
        root = tk.Tk()
        app = QRCodeGenerator(root, admin=True)
        root.mainloop()

    def open_qr_recognition(self):
        self.master.destroy()
        root = tk.Tk()
        app = QRCodeRecognition(root, admin=True)
        root.mainloop()

    def open_package_lookup(self):
        self.master.destroy()
        root = tk.Tk()
        app = PackageLookup(root, admin=True)
        root.mainloop()

root = tk.Tk()
app = LoginWindow(root)
root.mainloop()
