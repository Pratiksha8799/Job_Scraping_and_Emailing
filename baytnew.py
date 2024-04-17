# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 18:42:40 2023

@author: user
"""
# Import necessary libraries
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import regex as re
import math
import humanfriendly
from datetime import date

# Function to scrape job data from Bayt website
def scrape_bayt(skills, location):
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.bayt.com/")

    # Find the search box and enter the search query
    search_box = driver.find_element(By.ID, 'text_search')
    search_box.send_keys(skills)
    
    # Enter location
    location_search = driver.find_element(By.XPATH, "(//input[@id='search_country__r'])[1]")
    location_search.send_keys(location)
    time.sleep(2)

    # Find and click the search button
    button = driver.find_element(By.CSS_SELECTOR, '[data-js-aid="search"]')
    button.click()

    # Click the "Job Type" checkbox (second option)
    checkbox_one = driver.find_element(By.XPATH, '//*[@id="clusterFormId"]/div/div/div[2]/div/div[1]/div/ul/li[4]/a')
    driver.execute_script("arguments[0].click();", checkbox_one)
    time.sleep(3)

    # Get the total number of jobs and calculate the number of pages
    job_count = driver.execute_script("return document.querySelector('#results_inner > div.card > div.card-head > div > div:nth-child(1) > span').textContent;")
    job_count = re.findall(r'^([\d.]+(?:[kK])?) Jobs Found$', job_count)[0]
    job_count = humanfriendly.parse_size(job_count)
    print('job count', job_count)
    job_count = job_count / 20
    page_count = math.ceil(job_count)

    # Get the URL of the current page
    link = driver.current_url

    # Initialize lists to store data
    Description = []
    Job_Title = []
    Company_Name = []
    Job_Link = []
    Company_Industry = []
    Country = []
    Company_Type = []
    Monthly_Salary_Range = []
    Vacancies = []

    # Loop through all pages
    print(page_count)
    for i in range(1, 2):  # Scraping only first page for testing
    
        page = link + '&page={}'.format(i)
        print("Scraping page", i)
        driver.get(page)
        time.sleep(3)
    
        main_div = driver.find_element(By.ID, 'jsMainListingContainer')
        job_cart = main_div.find_elements(By.CLASS_NAME, 'has-pointer-d')

        for job in job_cart:
            job_link = job.find_element(By.TAG_NAME, 'a')
            job_title = job_link.text
            job_post_link = job_link.get_attribute("href")
            
            # Open the job post in a new tab
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(job_post_link)
            time.sleep(5)
            
            # Scraping job details
            company = driver.find_element(By.XPATH, "//ul[contains(@class,'list is-basic t-small')]/li").text
            city = driver.find_element(By.XPATH,"//body/div[4]/section[1]/div[1]/div[1]/div[2]/div[1]/ul[1]/li[2]").text
            desc = driver.find_element(By.XPATH, "//div[@class='t-break']").text
            job_details = driver.find_element(By.ID, "job_card").text
            job_details = re.sub(r'\s+', ' ', job_details)
            Company_Ind = re.findall(r'(?<=Company Industry)(.*)(?=Company Type)', job_details)[0]
            Company_Typ = re.findall(r'(?<=Company Type)(.*)(?=Job Role)', job_details)[0]

            MonthlySalary = re.findall(r'(?<=Monthly Salary Range)(.*)(?=Number of Vacancies)', job_details)[0]
            Number_of_Vacancies = re.findall(r'(?<=Number of Vacancies)(.*)', job_details)[0]
            
            # Append data to lists
            Description.append(desc)
            Job_Title.append(job_title)
            Company_Name.append(company)
            Job_Link.append(job_post_link)
            Company_Industry.append(Company_Ind)
            Company_Type.append(Company_Typ)
            Country.append(city)
            Monthly_Salary_Range.append(MonthlySalary)
            Vacancies.append(Number_of_Vacancies)
            
            # Close the tab and switch back to the main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    # Close the WebDriver session
    driver.quit()

    # Create a DataFrame and save the data to a CSV file
    df = pd.DataFrame({
        "Domain_Name":skills,
        "Job_Title": Job_Title,
        "Description": Description,
        "Company_Name": Company_Name,
        "Address": Country,
        "Job_Link": Job_Link,
        "Company_Industry": Company_Industry,
        "Company_Type": Company_Type,
        "Job_Posted": 'Past 30 days'
    })
    today = date.today()
    filename = "Extracted_CSV//bayt_data_" + str(today) + ".csv"
    df.to_csv(filename, index=False)

# Example usage
# skills = 'Data analyst'
# location = 'India'
# scrape_bayt(skills, location)
