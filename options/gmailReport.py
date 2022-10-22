import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import json

import os

def sendGmailReport():
    with open("config.json", "r") as read_file:
        data = json.load(read_file)

    mail_content = ''
    filelist = [ f for f in os.listdir("options/data") if f.endswith(".csv") ]

    #The mail addresses and password
    sender_address = data['sendEmail']
    sender_pass = data['emailPassword']
    receiver_address = data['receiveEmail']
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f'Daily Results: {filelist[0][:-4]}'   #The subject line

    ## Write file as text
    with open(f"options/data/{filelist[0]}", "r", newline="") as f:
        for line in f:
            line = line.replace(',','\t')
            mail_content += f"{line}\n"
    message.attach(MIMEText(mail_content, 'plain'))


    attach_file_name = f"options/data/{filelist[0]}"
    payload = MIMEBase('application', 'octate-stream')
    with open(attach_file_name, 'rb') as attach_file:# Open the file as binary mode
        payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header("Content-Disposition", f"attachment; filename=options/data/{filelist[0]}")
    message.attach(payload)

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

if __name__=="__main__":
    sendGmailReport()