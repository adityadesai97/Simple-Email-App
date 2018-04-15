import smtplib
import os.path

LOG_PATH='./logs.txt'
if not os.path.isfile(LOG_PATH):
    with open('logs.txt', 'w') as file:
        file.write("0\n")

encryptionkey = 1

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
