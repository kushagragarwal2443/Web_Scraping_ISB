from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver= webdriver.Firefox()
driver.get("https://www.facebook.com")
email=""
password=""
email_element=driver.find_element_by_id("email")
email_element.send_keys(email)
pass_element=driver.find_element_by_id("pass")
pass_element.send_keys(password)
pass_element.send_keys(Keys.RETURN)
pass_element.close()
