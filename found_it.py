# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 12:45:54 2023

@author: user
"""

from selenium import webdriver  # Importing webdriver module
import time  # Importing time module
from webdriver_manager.chrome import ChromeDriverManager  # Importing ChromeDriverManager module
from selenium.webdriver.common.by import By  # Importing By class from selenium.webdriver.common.by
from selenium.webdriver.support.ui import WebDriverWait, Select  # Importing WebDriverWait, Select classes
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Importing Keys class from selenium.webdriver.common.keys
import regex as re  # Importing regex module
import math  # Importing math module
from bs4 import BeautifulSoup  # Importing BeautifulSoup module
import requests  # Importing requests module
from selenium.webdriver.support import expected_conditions as EC  # Importing expected_conditions class from selenium.webdriver.support
from selenium.webdriver.common.action_chains import ActionChains  # Importing ActionChains class from selenium.webdriver.common.action_chains
import pandas as pd  # Importing pandas module
import os  # Importing os module
from datetime import date  # Importing date class from datetime module



# Defining the main_foundit function with keywords and location as parameters
def main_foundit(keywords, location):

    # Setting up Chrome webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.foundit.in/")

    # Entering keywords and location into search boxes
    driver.find_element(By.ID, 'SE_home_autocomplete').send_keys(keywords)
    time.sleep(2)
    driver.find_element(By.ID, 'SE_home_autocomplete_location').send_keys(location)
    time.sleep(2)

    # Clicking search button
    button_class = "btn"
    button_xpath = f"//input[@type='submit' and contains(@class, '{button_class}')]"
    button_element = driver.find_element(By.XPATH, button_xpath)
    button_element.click()
    time.sleep(2)

    # Clicking additional search filters
    button_element = driver.find_element(By.XPATH, '//*[@id="top-scroll"]/li[8]/button')
    button_element.click()
    time.sleep(2)

    # Selecting a specific checkbox
    checkbox_xpath = '//*[@id="top-scroll"]/li[8]/div/div[1]/div[1]/div/div'
    checkbox_element = driver.find_element(By.XPATH, checkbox_xpath)
    specific_checkbox_id = '30'
    specific_checkbox_element = checkbox_element.find_element(By.ID, specific_checkbox_id)
    if not specific_checkbox_element.is_selected():
        specific_checkbox_element.click()

    # Applying selected filters
    apply_button_class = 'apply'
    apply_button_element = driver.find_element(By.CLASS_NAME, apply_button_class)
    apply_button_element.click()
    time.sleep(2)

    # Calculating number of pages
    page_count = driver.find_element(By.CLASS_NAME, 'job-count').text
    page_count = re.findall(r'\d+', page_count)[0]
    page_count = math.ceil((int(page_count) / 15))
    time.sleep(2)

    # Initializing lists to store job data
    job_title = []
    c_name = []
    job_type = []
    experience = []
    skills = []
    description_data = []
    industry_list = []
    function_list = []
    url_list = []
    location_list = []

    
        # Looping through pages
    for page in range(2, 4):  # For demonstration, loop is limited to first 3 pages

        try:
            print(page)
            value = f'//*[@id="srpContent"]/div[1]/div/div[18]/div[{page}]'
            click_page = driver.find_element(By.XPATH, value)
            driver.execute_script("arguments[0].click();", click_page)
            print(driver.current_url)
            time.sleep(4)
            print("****")
            
            # Extracting job list from current page
            job_container = driver.find_element(By.ID, 'srpContent')
            job_list = job_container.find_elements(By.CLASS_NAME, 'srpResultCardContainer')
            
            print(len(job_list))
        
            # Looping through job listings on current page
            for i in range(len(job_list)):
                ActionChains(driver).click(job_list[i]).perform()
                time.sleep(3)
                driver.implicitly_wait(5) 
                print(i)
               
                try:
                    job_title.append(job_list[i].find_element(By.CLASS_NAME, 'jobTitle').text)
                except Exception as e:
                    job_title.append('')
        
                try:
                    c_name.append(job_list[i].find_element(By.CLASS_NAME, 'companyName').text.strip())
                except Exception as e:
                    c_name.append('')
                     
                
                try:
                    details = job_list[i].find_elements(By.CLASS_NAME, 'details')
                    if details != []:
                        try:
                            job_type.append(details[0].text)
                        except Exception as e:
                            job_type.append('')
                        try:
                            location_list.append(details[1].text)
                        except Exception as e:
                            location_list.append('')
                       
                        try:
                          experience.append(details[2].text)
                        except Exception as e:
                            experience.append('')
                           
                        
                except Exception as e:
                    job_type.append('')
                    location_list.append('')
                    experience.append('')
                    pass
               
                time.sleep(2)
                
                # Extracting job description and other details
                try:
                    description = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'jobDescInfo'))
                    )
                    description1 = description.text
                    description_data.append(description1)
                except Exception as e:
                    description_data.append('')
                
                try:
                    other_desc = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="jobSummary"]/div[2]/div[2]')))
                    industry = other_desc.text
                    industry_list.append(industry)
                except Exception as e:
                    industry_list.append('')
                
                try:
                    other_desc1 = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="jobSummary"]/div[3]/div[2]')))
                    Function = other_desc1.text
                    function_list.append(Function)
                except Exception as e:
                    function_list.append('')
                
                try:
                    skill_set_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'skillSet'))
                    )
                    skill_list = skill_set_element.text
                    skills.append(skill_list)
                except Exception as e:
                    skills.append('')
                
                # Extracting job URL
                url_before_click = driver.current_url
                try:
                    if 'Quess' in c_name[i]:
                        url_list.append('https://www.foundit.in/seeker/cjt/job-vacancy-mainframe-acf2-business-analyst-quess-it-staffing-formerly-known-as-magna-infotech-pune-5-8-years-66533957')
                    else:
                        element = driver.find_element(By.CLASS_NAME, 'mqfisrp-open-jd')
                        action1 = ActionChains(driver)
                        action1.move_to_element(element).move_by_offset(0, 10).click().perform()
                        window_count = len(driver.window_handles)
                        if window_count == 2:
                            driver.switch_to.window(driver.window_handles[1])
                            current_url1 = driver.current_url
                            url_list.append(current_url1)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        elif window_count == 1:
                            time.sleep(1)
                            current_url1 = driver.current_url
                            url_list.append(current_url1)
                            driver.back()
                            time.sleep(2)
                            job_container = driver.find_element(By.ID, 'srpContent')
                            job_list = job_container.find_elements(By.CLASS_NAME, 'srpResultCardContainer')
                        elif window_count > 2:
                            current_url1 = driver.current_url
                            url_list.append(current_url1)
                            for handle in driver.window_handles[1:]:
                                driver.switch_to.window(handle)
                                driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                except Exception as e:
                    url_list.append('')
                    pass
               
        except Exception as e:
            pass
           
        try:
            # Creating DataFrame and saving to CSV
            df = pd.DataFrame({'Domain_Name': keywords, 'Job_Title': job_title, 'Description': description_data, 
                               'Company_Name': c_name, 'Location': location_list, 'Job_Link': url_list, 
                               'Industry': industry_list, 'Job_Type': job_type, 'Skills': skills, 'Experience': experience})
            today = date.today()
            filename = "Extracted_CSV//foundit_data_" + str(today) + ".csv"
            df.to_csv(filename, index=False)
        except:
            pass

    # Closing the webdriver
    driver.close()