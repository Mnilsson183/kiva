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
id int primary key, name varchar(100), location varchar(100), activity varchar(100), number_of_borrowers int, 
paid int, loan_amount int)''');
i = 100
while True:
	if (i > 300):
		break
	status, response = http.request('http://api.kivaws.org/v1/loans/' + str(i))
	count = 0
	soup = BeautifulSoup(response, "lxml")
	# The [1:] syntax skips the first header row when we loop through all tr rows
	for partner in soup.find_all('tr')[1:]:
		for td in partner:
			# i dont want all the data so purposefully limit the rows
			if(count < 7):
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
			id, name, location, activity, number_of_borrowers, 
			paid, loan_amount
			) VALUES (
				?,?,?,?,?,
				?,?
			)''', lines);
		lines=[]
		count = 0
	i += 1
conn.commit()
conn.close()