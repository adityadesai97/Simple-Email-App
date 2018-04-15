import tkinter as tk
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import npl

LARGE_FONT = ("Verdana", 20)


class ControllerClass(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def login(self, e1, e2):
        try:
            npl.server.login(e1, e2)
        except SMTPAuthenticationError:
            print("The details entered were incorrect")
        else:
            print("Successfully logged in")
            with open('logs.txt', 'a') as file:
                file.write("\nfrom:{}\n".format(self.encrypt(e1, npl.encryptionkey).rstrip("\r\n")))
            with open('logs.txt', 'r') as file:
                data = file.readlines()
            data[0] = str(int(data[0]) + 1) + "\n"
            with open('logs.txt', 'w') as file:
                file.writelines(data)
            self.show_frame(PageOne)

    def send(self, e1, e2, e3):
        fromname = self.getsendername()
        msg = MIMEMultipart()
        msg['From'] = fromname
        msg['To'] = e1
        msg['Subject'] = e2
        message = e3
        msg.attach(MIMEText(message))
        try:
            npl.server.sendmail(fromname, e1, msg.as_string())
        except SMTPRecipientsRefused:
            print("Error occurred")
        else:
            npl.server.close()
            print('Successfully sent the mail')
            with open('logs.txt', 'a') as file:
                file.write("to:{}\nsubject:{}\nmessage:{}\n".format(self.encrypt(e1, npl.encryptionkey).rstrip("\r\n"), self.encrypt(e2, npl.encryptionkey).rstrip("\r\n"), self.encrypt(e3, npl.encryptionkey).rstrip("\r\n")))
            self.show_frame(PageTwo)

    def getsendername(self):
        with open('logs.txt', 'r') as file:
            data = file.readlines()
        pointer = int(data[0])
        sendername = self.decrypt(data[2 + ((pointer - 1) * 5)].split(":")[1], npl.encryptionkey).rstrip("\r\n") + "@gmail.com"
        return sendername

    def encrypt(self, plainText, shift):

        cipherText = ""
        for ch in plainText:
            if ch.isalpha():
                stayInAlphabet = ord(ch) + shift
            else:
                finalLetter = ch
                cipherText += finalLetter
                continue
            if stayInAlphabet > ord('z'):
                stayInAlphabet -= 26
            finalLetter = chr(stayInAlphabet)
            cipherText += finalLetter
        return cipherText

    def decrypt(self, encryption, encryption_shift):

        cipherText1 = ""
        for c in encryption:
            if c.isalpha():
                stayInAlphabet1 = ord(c) - encryption_shift
            else:
                finalLetter1 = c
                cipherText1 += finalLetter1
                continue
            if stayInAlphabet1 > ord('z'):
                stayInAlphabet1 += 26
            finalLetter1 = chr(stayInAlphabet1)
            cipherText1 += finalLetter1
        return cipherText1


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        StartPage.make_widgets(self)

    def make_widgets(self):
        usernamelabel = tk.Label(self, text="Username")
        usernamelabel.grid(row=1)
        passwordlabel = tk.Label(self, text="Password")
        passwordlabel.grid(row=2)

        usernameentry = tk.Entry(self)
        usernameentry.grid(row=1, column=1)
        passwordentry = tk.Entry(self, show="*")
        passwordentry.grid(row=2, column=1)

        quitbutton = tk.Button(self, text='Quit', command=self.quit).grid(row=4, column=0, sticky=tk.W, pady=4)
        loginbutton = tk.Button(self, text='Login', command=lambda: self.controller.login(e1=usernameentry.get(), e2=passwordentry.get())).grid(row=4, column=1, sticky=tk.W, pady=4)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        PageOne.make_widgets(self)

    def make_widgets(self):
        recipientlabel = tk.Label(self, text="Recipient")
        recipientlabel.grid(row=1)
        subjectlabel = tk.Label(self, text="Subject")
        subjectlabel.grid(row=2)
        messagelabel = tk.Label(self, text="Message")
        messagelabel.grid(row=3)

        recipiententry = tk.Entry(self)
        recipiententry.grid(row=1, column=1)
        subjectentry = tk.Entry(self)
        subjectentry.grid(row=2, column=1)
        messageentry = tk.Entry(self)
        messageentry.grid(row=3, column=1)

        quitbutton = tk.Button(self, text='Quit', command=self.quit).grid(row=4, column=0, sticky=tk.W, pady=4)
        sendbutton = tk.Button(self, text='Send', command=lambda: self.controller.send(e1=recipiententry.get(), e2=subjectentry.get(), e3=messageentry.get())).grid(row=4, column=1, sticky=tk.W, pady=4)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        PageTwo.make_widgets(self)

    def make_widgets(self):
        label = tk.Label(self, text="Sent!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


app = ControllerClass()
app.mainloop()
