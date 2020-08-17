'''

Monitor a set of hosts using Python.

Send SMS & EMAIL alert to a set of email addresses and phone numbers whenever a host/ hosts is unreachable.

'''

import os
import time
import smtplib
from twilio.rest import Client

# Define SMS variables here
APIKeyTwilio = 'SKec9befa182856414a1fd489da935a922'
account_sid = 'ACa8a42dd3f98d75fd9f9b88c7156811b1'
auth_token = '94680ed9727c6d9673e3e24ca74d6e21'
client = Client(account_sid, auth_token)

# Define email variables here
gmail_user = 'tim.munyao@gmail.com'
gmail_password = '1988MyTime.!'
sent_from = gmail_user
to = ['it@mpkenya.com', 't.appytude@gmail.com', 'boniface.mungata@minigrp.com', 'george.wanyonyi@minigrp.com']
subject = 'INTERNET DOWNTIME'

# Define hosts file here
hostsfile = open("hosts.txt", "r")

# Begin monitoring
lines = hostsfile.readlines()
print("\n")
print("---MONITORING HAS STARTED---\n")
print("---------------------------------------------------------------------------")
for line in lines:
    response = os.system("ping -c 1 " + line)
    if response == 0:
        status = line.rstrip() + " is Reachable \n"
    else:
        status = line + " is Offline/ Unreachable \n"
        # send sms function
        message = client.messages.create(
            body="\nDear Administrator,\nYour host: " + str(line) + " is Offline/ Unreachable\n",
            from_='+15866666176',
            to='+254779069307'
            # to='+254728599188'
        )

        # send email
        body = "\nDear Administrator,\n\nYour host: " + str(
            line) + " is Offline/ Unreachable\n\n\nSent From Network Monitor"
        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()
            print("Email sent!")
        except:
            print("Something went wrong while sending email!")

    print(status)
    print("---------------------------------------------------------------------------")
    time.sleep(5)
