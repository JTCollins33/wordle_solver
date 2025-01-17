import smtplib
from email.message import EmailMessage

sender = "wordlesender@yahoo.com"
recipient = "wordlesender@yahoo.com"

pwd = input("What is your password: ")

server = smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465)
# server.starttls()
server.ehlo()
server.login(sender, pwd)

msg = 'test message'
server.sendmail(sender, recipient, msg)
server.quit()