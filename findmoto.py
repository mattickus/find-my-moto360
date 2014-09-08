import sys
import getopt
import json
import urllib2
import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

## Usage findmoto.py [zipcode] [distance]

zipcode = str(sys.argv[1])
distance = str(sys.argv[2])
body = ''
x = 0
url = 'http://api.remix.bestbuy.com/v1/stores(area(' + zipcode + ',' + distance + '))+products(sku%20in(8307143))?format=json&show=storeId,name,products.sku,products.name&apiKey=YOURAPIKEY'
req = urllib2.Request(url)
reply = urllib2.urlopen(req)
js = json.load(reply)
username = ""
password = ""
fromaddr = ""
toaddr = ""

result = js['stores']
for each in result:
	if x != 0:
		body += '\n'
	body += each['name'] + '\n'
	result2 = js['stores'][x]['products']
	for each2 in result2:
		body += '\t' + each2['name'] + '\n'
	x += 1

if body != '':
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	subject = str(x) + " Moto 360s Found Within " + distance + " Miles"
	msg['Subject'] = subject
	msg.attach(MIMEText(body,'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("username","password")
	text = msg.as_string()
	server.sendmail(fromaddr,toaddr,text)
	server.quit()
