from selenium import webdriver  # Importing necessary modules
import time  # For adding delays in the script
from webdriver_manager.chrome import ChromeDriverManager  # Managing ChromeDriver
from selenium.webdriver.common.by import By  # Locating elements
from selenium.webdriver.support.ui import WebDriverWait, Select  # Waiting for elements, selecting options
# from selenium.webdriver.support import expected_conditions as EC  # Conditions for waiting
from selenium.webdriver.common.keys import Keys  # Simulating keyboard keys
import math  # Math operations
import regex as re  # Regular expressions
import pandas as pd  # Handling data in DataFrame
from datetime import date  # Getting current date

def main_seek(skill, location):
    # skill = 'Data Analyst'
    # location = 'India'
    
    today = date.today()  # Getting the current date
    driver = webdriver.Chrome()  # Initializing Chrome WebDriver
    driver.maximize_window()  # Maximizing the browser window
    driver.get("https://www.seek.com.au/")  # Opening Seek website
    
    # job_id='Python Developer'
    job_id = skill  # Assigning the skill to search for
    driver.find_element(By.ID, 'keywords-input').send_keys(job_id)  # Entering the job skill
    time.sleep(2)  # Adding a delay to allow the page to load
    
    # country='Auburn NSW 2144'
    country = location  # Assigning the location to search for jobs
    driver.find_element(By.ID, 'SearchBar__Where').send_keys(country)  # Entering the location
    time.sleep(2)  # Adding a delay
    
    # Clicking the search button
    button_xpath = f'//*[@id="searchButton"]'
    button_element = driver.find_element(By.XPATH, button_xpath)
    button_element.click()
    time.sleep(2)  # Adding a delay
    
    # Selecting the 'Last 30 days' option from the dropdown
    dropdown_locator = "//span[contains(text(), 'listed')]/ancestor::span"
    dropdown_element = driver.find_element(By.XPATH, dropdown_locator)
    dropdown_element.click()
    option_text = driver.find_element(By.XPATH, "//span[text()='Last 30 days']")
    option_text.click()
    time.sleep(2)  # Adding a delay
    
    try:
        # Extracting the total number of pages
        page_count = driver.find_element(By.ID, "SearchSummary").text
        page_count = page_count.replace(',', '')
        page_count = re.findall(r'\d+', page_count)[0]
        page_count = math.ceil((int(page_count) / 22))
        link = driver.current_url
        
        # Lists to store job details
        job_links_list = []
        Job_Title = []
        Description = []
        Company_Name = []
        Address = []
        Job_Link = []
        Job_Type = []
        Company_Type = []
        
        # Looping through the pages to extract job details
        for i in range(1, 3):
            try:
                page_link = f'https://www.seek.com.au/{job_id}-jobs/in-{country}?daterange=31&page={i}'
                print(page_link)
                driver.get(page_link)
                time.sleep(2)
                
                all_links = []
                job_links = driver.find_elements(By.XPATH, '//article/div/a')
                
                # Extracting job links
                for i in job_links:
                    href = i.get_attribute("href")
                    all_links.append(href)
                    
                # Visiting each job page to extract details
                for j in all_links:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(j)
                    time.sleep(2)
                    
                    try:
                        des = driver.find_element(By.XPATH, '//div[@data-sticky="job-details-page"]/div/div[2]/div/div/div[2]').text
                    except:   
                        des = driver.find_element(By.XPATH, '//div[@data-sticky="job-details-page"]/div/div/div/div/div[2]').text
                        
                    try:
                        title = driver.find_element(By.XPATH, "//h1[@class='_1wkzzau0 a1msqi4y lnocuo0 lnocuol _1d0g9qk4 lnocuop lnocuo21']").text
                    except:
                        title = None
                        
                    try:
                        name = driver.find_element(By.XPATH, "(//span[@class='_1wkzzau0 a1msqi4y lnocuo0 lnocuo1 lnocuo21 _1d0g9qk4 lnocuod'])[1]").text    
                    except:
                        name = None
                        
                    try:
                        location = driver.find_elements(By.XPATH, "//*[local-name() = 'svg']/*[local-name() = 'path' and contains(@d,'M12 1C7.6 1 4 4.6 4 9c0')]/ancestor::span")[1].text    
                    except:
                        location = None
                    
                    try:
                        company_type = driver.find_elements(By.XPATH, "//*[local-name() = 'svg']/*[local-name() = 'path' and contains(@d,'M9 6h2v2H9zm4 0h2v2h-2zm-4')]/ancestor::span")[0].text
                    except:
                        company_type = None
                    
                    try:
                        job_type = driver.find_elements(By.XPATH, "//*[local-name() = 'svg']/*[local-name() = 'path' and contains(@d,'M12 1C5.9 1 1 5.9 1 12s4.9')]/ancestor::span")[0].text
                    except:
                        job_type = None
                        
                    # Appending job details to lists
                    Job_Title.append(title)
                    Description.append(des)
                    Company_Name.append(name)
                    Address.append(location)
                    Job_Link.append(j)
                    Job_Type.append(job_type)
                    Company_Type.append(company_type)
                    
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])  
            
            except:
                print(f'there is no data on the page no.{i}')
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
        driver.quit()  # Closing the WebDriver
        
        # Creating DataFrame from extracted job details
        df = pd.DataFrame({
            "Domain_Name": job_id,
            "Job_Title": Job_Title,
            "Description": Description,
            "Company_Name": Company_Name,
            "Address": Address,
            "Job_Link": Job_Link,
            "Job_Type": Job_Type,
            "Company_Type": Company_Type,
            "Job_Posted": 'Past 30 days'
        })
        
        # Saving DataFrame to a CSV file
        filename = "Extracted_CSV//seek_data_" + str(today) + ".csv"
        df.to_csv(filename, index=False)
        
    except Exception as e:
        # Handling exceptions
        df = pd.DataFrame({
            "Domain_Name": [None],
            "Job_Title": [None],
            "Description": [None],
            "Company_Name": [None],
            "Address": [None],
            "Job_Link": [None],
            "Job_Type": [None],
            "Company_Type": [None],
            "Job_Posted": [None]
        })
        
        # Saving DataFrame to a CSV file
        filename = "Extracted_CSV//seek_data_" + str(today) + ".csv"
        df.to_csv(filename, index=False)
        print('Please enter Australian location: ', e)

# skill='Data analyst'
# location = 'India'
# main_seek(skill, location)
