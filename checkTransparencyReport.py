import os
import re
import json
import smtplib
import datetime

from urllib2 import Request, urlopen, URLError, HTTPError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(domain,request_list):
    Me = 'support@dresspirit.com'
    To = ['632624460@qq.com', 'donglongtu@mingdabeta.com','qinyingjie@mingdabeta.com','231130161@qq.com','zhangpeng@mingdabeta.com']

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Google Transparency Report update urls for %s' % (domain)
    # Me == the sender's email address
    # To = the list of all recipients' email addresses
    msg['From'] = Me
    msg['To'] = ",".join(To)
    text = []
    for request in request_list:
        text.append('Request ID:%s\t;\tDate:%s\t;\tCopyright Owners:%s\t;\tReporting Organizations:%s\t;\tURLs:%s' % (request['Request ID'],request['Date'],request['Copyright Owners'],request['Reporting Organizations'],request['URLs']))
    text = "\n".join(text)
    msg.attach(MIMEText(text, 'plain'))
    
    # Send the email via our own SMTP server.
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login('support@dresspirit.com', 'mingDA1234')
    s.sendmail(Me, To, msg.as_string())
    s.quit()


def checkTransparencyReport(domain):
    url = 'https://www.google.com/transparencyreport/api/v2/reports/copyright/products/search/searchrequests/?end=20&domain=%s&alt=JSONP&c=angular.callbacks._3' % (domain)
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server'
            print 'Reason:', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request'
            print 'Error code:', e.code
    else:
        request_list = []
        start_time = 1481025967813
        data = response.read()
        reg = re.compile(r'{.+}')
        data = reg.findall(data)
        dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir,'%s-request' % (domain))
        try:
            with open(filename) as f:
                sent_request_id_list = [id.strip() for id in f.readlines()]
            f.close()
        except:
            sent_request_id_list = []
        if len(data) > 0:
            requests = json.loads(data[0])['requests']
            for request in requests:
                urls_removed_in_request = request['urls_removed_in_request']
                request_id = str(request['request_id'])
                urls_in_request = request['urls_in_request']
                copyright_owner = request['copyright_owner']['entity_name']
                reporting_org = request['reporting_org']['entity_name']
                request_date_ms = request['request_date_ms']
                date = datetime.datetime.fromtimestamp(int(str(request_date_ms)[:-3])).strftime('%b %d, %Y')
                if request_date_ms > start_time:
                    if request_id not in sent_request_id_list:
                        request_list.append({'Request ID':request_id,'Date':date,'Copyright Owners':copyright_owner,'Reporting Organizations':reporting_org,'URLs':urls_in_request})
                        sent_request_id_list.append(request_id)
            if len(request_list) > 0:
                send_email(domain, request_list)
                with open(filename,'w') as f:
                    for request_id in sent_request_id_list:
                        f.write("%s\n" % request_id)
                f.close()


if __name__ == "__main__":
    domainList = ['doriswedding.com','newadoringdress.com','junebridals.com','ucenterdress.com']
    for domain in domainList:
        checkTransparencyReport(domain)