import smtplib
from email.mime.text import MIMEText


def sendEmail(content,email):
    fp = open(content, 'rb')
    # Create a text/plain message
    msg = MIMEText(fp.read(),'html')
    fp.close()
    
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Need Any Assistance with Your Junebridals Order?'
    msg['From'] = 'support@junebridals.com'
    msg['To'] = email
    
    s = smtplib.SMTP("smtp.mailgun.org", 587)
    s.starttls()
    s.login('support@mg.junebridals.com', 'mingDA@1234')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print 'Send Ok ' , email

if __name__ == "__main__":
    emailList = []
    with open('adoring.csv') as f:
        for line in f:
            emailList.append(line.split('#')[-1].strip())
    #print emailList
    for email in emailList:
        content = 'email-june.html'
        sendEmail(content,email)