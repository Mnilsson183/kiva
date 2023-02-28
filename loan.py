import httplib2
import sqlite3
from bs4 import BeautifulSoup
from lxml.html import tostring, html5parser
http = httplib2.Http()
#use beautiful soup to parse 
# soup = BeautifulSoup(response)
# if you have lxml installed then uncomment and use the next line

lines=[]
# establish the connection to the sqlite db
conn = sqlite3.connect('outputs/kiva.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS loans (
id int primary key, name varchar(100), status varchar(100), funded_amount int, basket_amount int, 
paid_amount int, video varchar(100), activity varchar(200), sector varchar(100), themes varchar(100),
use varchar(400), delinquent varchar(50), partner_id int, posted_date varchar(100), planned_expiration_date varchar(100),
loan_amount int, lender_count int, currency_exchange_loss_amount int, bonus_credit_eligibility varchar(10), funded_date varchar(100),
paid_date varchar(100), arrears_amount int
)''');
i = 100
while True:
	if (i > 700):
		break
	status, response = http.request('http://api.kivaws.org/v1/loans/' + str(i))
	count = 0
	soup = BeautifulSoup(response, "lxml")
	# The [1:] syntax skips the first header row when we loop through all tr rows
	for partner in soup.find_all('tr')[1:]:
		for td in partner:
			# i dont want all the data so purposefully limit the rows
			if(count < 22):
				try:
					text = td.renderContents().decode('utf-8')
				except AttributeError:
					text = td.renderContents().decode('utf-8')
				# test=td.encode_contents().decode('utf-8')
				if text == '':
					text = 'NULL'
				lines.append(text)
			count += 1
		c.execute('''INSERT OR REPLACE INTO loans (
			id, name, status, funded_amount, basket_amount, 
paid_amount, video, activity, sector, themes,
use, delinquent, partner_id, posted_date, planned_expiration_date,
loan_amount, lender_count, currency_exchange_loss_amount, bonus_credit_eligibility, funded_date,
paid_date, arrears_amount
			) VALUES (
				?,?,?,?,?,
				?,?,?,?,?,
				?,?,?,?,?,
				?,?,?,?,?,
				?,?
			)''', lines);
		lines=[]
		count = 0
	i += 1
conn.commit()
conn.close()