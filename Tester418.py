from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from dotenv import load_dotenv
import os
import time

# load env variables
load_dotenv()  # Automatically loads .env from current directory
pems_user = os.getenv("PEMS_USERNAME")
pems_password = os.getenv("PEMS_PASSWORD")

# Launch Chrome driver
driver = webdriver.Chrome()

# Load a page
driver.get("https://pems.dot.ca.gov/")

# login
# find elements - use name attribute of HTML element
username_field = driver.find_element(by=By.NAME, value="username")
password_field = driver.find_element(by=By.NAME, value="password")
submit_button = driver.find_element(by=By.NAME, value="login")

# # take action on the element - send keys, types keys into editable element like a text field
username_field.send_keys(pems_user)
password_field.send_keys(pems_password)
submit_button.click()

time.sleep(20)  # Wait for login to complete

# # confirm login 
# driver.page_source: returns the HTML source code of the current page
if "Welcome, Lucy" in driver.page_source:
    print("Login successful")

# 3. Navigate to download page
driver.get("https://pems.dot.ca.gov/?dnode=Clearinghouse")

if "Data Clearinghouse" in driver.page_source:
    print("Data Clearinghouse page loaded successfully")

# 4. Fill in download form
select_element = driver.find_element(By.ID, "type")
select = Select(select_element)
select.select_by_visible_text('Station Hour')

select_element_district = driver.find_element(By.ID, "district_id")
select_district = Select(select_element_district)
select_district.select_by_visible_text('District 7')

submit_form = driver.find_element(by=By.NAME, value="submit")
submit_form.click()

time.sleep(20)

if "contains the hourly totals for each active station on the given day" in driver.page_source:
    print("Data page loaded successfully")

# go through each row of the table (each row is a different year of data)
data_table = driver.find_element(By.ID, "kgwdmvrbdo")
rows = data_table.find_elements(By.XPATH, ".//tbody/tr")
print(len(rows))

for i in range(0, len(rows)):
    # get the year from the first column of the row
    year = rows[i].find_element(By.XPATH, ".//td[1]").text
    print(year)
    if year == '24':
        break
    # click on the link in the second column of the row
    # each gray box in the same row has the same list of links for the given year
    link = rows[i].find_element(By.XPATH, ".//td[2]/a")
    link.click()


    time.sleep(5)  # Wait for page to load

# # # 5. Submit the form
# # driver.find_element(By.NAME, "export").click()
# # time.sleep(5)  # Wait for file download to begin

# # # 6. Close browser
# # driver.quit()
