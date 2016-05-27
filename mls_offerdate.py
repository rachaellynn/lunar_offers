#my third (and this time successful!) try at pulling offer date data from mLSPIN
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import mechanize
import urllib2
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
import sys
import pdb
import time
import csv
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import os
#import urllib.request 

# spoof our browser so it looks like we're not a robot connecting to the website
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent','Firefox')]
driver = webdriver.Firefox()


url = 'https://h3s.mlspin.com/signin.asp'
driver.get(url)
# login
username = driver.find_element_by_name('user_name')
password = driver.find_element_by_name('pass')
login = driver.find_element_by_name('signin')
time.sleep(2)
username.send_keys(os.environ['MLSPIN_ID')
time.sleep(2)
password.send_keys(os.environ['MLSPIN_PASSWORD'])
time.sleep(2)
login.submit()
time.sleep(2)
# >> click on the search page
driver.find_element_by_xpath('//*[@title=" Search MLS Listings "]').click()
driver.switch_to_frame('TopFrame')
time.sleep(2)
# >> select property types
action = ActionChains(driver)
action.key_down(Keys.CONTROL).perform()
driver.find_element_by_xpath("//select[@name='proptype']/option[@value='SF']").click()
driver.find_element_by_xpath("//select[@name='proptype']/option[@value='CC']").click()
driver.find_element_by_xpath("//select[@name='proptype']/option[@value='MF']").click()
driver.find_element_by_xpath("//select[@name='proptype']/option[@value='LD']").click()
action.key_up(Keys.CONTROL).perform()
# >> select status
action = ActionChains(driver)
action.key_down(Keys.CONTROL).perform()
driver.find_element_by_xpath("//select[@name='status']/option[@value='CTG']").click()
driver.find_element_by_xpath("//select[@name='status']/option[@value='UAG']").click()
driver.find_element_by_xpath("//select[@name='status']/option[@value='SLD']").click()
driver.find_element_by_xpath("//select[@name='status']/option[@value='RNT']").click()
driver.find_element_by_xpath("//select[@name='status']/option[@value='WDN']").click()
driver.find_element_by_xpath("//select[@name='status']/option[@value='EXP']").click()
driver.find_element_by_xpath("//select[@name='status']/option[@value='CAN']").click()
action.key_up(Keys.CONTROL).perform()
# >> clear out the time frame
driver.find_element_by_name('TimeFrame').clear()
# >> select towns
driver.find_element_by_xpath("//select[@name='TheTowns']/option[@value='MA']").click()
driver.execute_script("AddTown()")
# >> select offer_date
driver.find_element_by_xpath("//select[@name='addfield']/option[@value='OFFER_DATE']").click()
# >> add date
enterdate = driver.find_element_by_name('criteria')
date = "12/01/2015"
end_date = "12/31/2015"
enterdate.send_keys(date)
# >> click "count"
driver.execute_script("GetCount()")
time.sleep(40)
# >> record the date and the count
data = driver.find_element_by_id("countDownText")
target = open('offer_data.csv', 'a')
target.write(date + "\t" + data.text)
print data.text
target.write("\n")

# >> create the loop
date = datetime.datetime.strptime(date,"%m/%d/%Y") 
end_date = datetime.datetime.strptime(end_date,"%m/%d/%Y")

while date < end_date:
	date += timedelta(days=1) #advances the date
	date_text = datetime.datetime.strftime(date,"%m/%d/%Y") #turns it back into a string
	driver.find_element_by_name('criteria').clear() #clears previous date	
	enterdate = driver.find_element_by_name('criteria') #find the criteria field
	enterdate.send_keys(date_text) #sends the new date
	# >> click "count"
	driver.execute_script("GetCount()")
	time.sleep(40)
	# >> record the date and the count
	data = driver.find_element_by_id("countDownText")
	target = open('offer_data.csv', 'a')
	target.write(date_text + "\t" + data.text)
	print data.text
	target.write("\n")
target.close

