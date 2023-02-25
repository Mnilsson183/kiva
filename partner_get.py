import httplib2
import sqlite3
from bs4 import BeautifulSoup
from lxml.html import tostring, html5parser
http = httplib2.Http()
status, response = http.request('http://api.kivaws.org/v1/partners.html')
#use beautiful soup to parse 
# soup = BeautifulSoup(response)
# if you have lxml installed then uncomment and use the next line
soup = BeautifulSoup(response, "lxml")
lines=[]
# establish the connection to the sqlite db
conn = sqlite3.connect('kiva.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS partners (
id int primary key, name varchar(255), status varchar(10), rating varchar(20), start_date datetime,
delinquency_rate float, default_rate float, total_amount_raised unsigned bigint, loans_posted smallint, portfolio_yield real,
profitability float, delinquency_rate_note varchar(100), portfolio_yield_note varchar(100), charges_fees_and_interest varchar(100), average_loan_size_percent_per_capita_income float,
loans_at_risk_rate float, currency_exchange_loss_rate float, url varchar(300), social_performance_strengths varchar(100))''');
count = 0
# The [1:] syntax skips the first header row when we loop through all tr rows
for partner in soup.find_all('tr')[1:]:
	for td in partner:
		# i dont want all the data so purposefully limit the rows
		if(count < 19):
			text=td.renderContents().decode('utf-8')
			# test=td.encode_contents().decode('utf-8')
			if text == '':
				text = 'NULL'
			lines.append(text)
		count += 1
	c.execute('''INSERT OR REPLACE INTO partners (
		id,name,status,rating,start_date,
		delinquency_rate,default_rate,total_amount_raised,loans_posted,portfolio_yield,
		profitability, delinquency_rate_note, portfolio_yield_note, charges_fees_and_interest, average_loan_size_percent_per_capita_income,
		loans_at_risk_rate, currency_exchange_loss_rate, url, social_performance_strengths
		) VALUES (
			?,?,?,?,?,
			?,?,?,?,?,
			?,?,?,?,?,
			?,?,?,?
		)''', lines);
	lines=[]
	count = 0
conn.commit()
conn.close()