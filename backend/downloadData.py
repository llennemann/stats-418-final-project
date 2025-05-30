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

time.sleep(10)  # Wait for login to complete

# # confirm login 
# driver.page_source: returns the HTML source code of the current page
if "Welcome, Lucy" in driver.page_source:
    print("Login successful")

# 3. Navigate to download page
driver.get("https://pems.dot.ca.gov/?dnode=Clearinghouse")

if "Data Clearinghouse" in driver.page_source:
    print("Data Clearinghouse page loaded successfully")

# 4. Fill in download form
# field: type
select_element = driver.find_element(By.ID, "type")
select = Select(select_element)
select.select_by_visible_text('Station Hour')
 
# field: district
select_element_district = driver.find_element(By.ID, "district_id")
select_district = Select(select_element_district)
select_district.select_by_visible_text('District 7')

# field: submit button
submit_form = driver.find_element(by=By.NAME, value="submit")
submit_form.click()

time.sleep(15)


if "hourly totals for each active station" in driver.page_source:
    print("Data page loaded successfully")
else:
    print(driver.page_source)

# go through each row of the table (each row is a different year of data)
table_xpath = "/html/body/div[1]/div[2]/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/table"
data_table = driver.find_element(By.XPATH, table_xpath)
rows = data_table.find_elements(By.XPATH, ".//tbody/tr")
# print(len(rows))  # 25 years and the header row

for i in range(1, len(rows)):
    # get the year from the first column of the row
    year = rows[i].find_element(By.XPATH, ".//td[1]").text
    print("Year: " + year)
    # get data from 2020-2025
    if year == '23':
        break
    # click on the link in the second column of the row
    # each gray box in the same row has the same list of links for the given year
    link = rows[i].find_element(By.XPATH, ".//td[2]/a")
    # print(link.get_attribute("href"))
    link.click()

    time.sleep(10)

    # print list of files to download
    data_files_xpath = "/html/body/div[1]/div[2]/div[1]/div/div/div/div/div/div[4]/div[2]/div/div/table"
    data_files_table = driver.find_element(By.XPATH, data_files_xpath)
    data_files_rows = data_files_table.find_elements(By.XPATH, ".//tbody/tr")
    print('Number of files to download: ' + str(len(data_files_rows)))

    # iterate through the data files
    for j in range(1, len(data_files_rows)):
        file_name = data_files_rows[j].find_element(By.XPATH, ".//td[1]/a")
        if file_name.text in os.listdir(path="/Users/lucy/Downloads"):
            print('File already exists: ' + file_name.text)
            continue
        print('Downloading....' + file_name.text)
        file_name.click() # click on file link to download
        seconds = 0
        dl_wait = True
        while any([filename.endswith(".crdownload") for filename in os.listdir("/Users/lucy/Downloads")]):
            time.sleep(1)
        #time.sleep(15)
        

# # # 6. Close browser
driver.quit()
