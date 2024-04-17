# Importing necessary modules
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
import regex as re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from datetime import date

def main_wwr():
    # Setting up the Chrome WebDriver
    driver = webdriver.Chrome()
    # Navigating to the target website
    driver.get("https://weworkremotely.com/")
    # Maximizing the browser window
    driver.maximize_window()
    # Adding a small delay for the page to load
    time.sleep(1)
    
    # Lists to store job data
    job_title_lis = []; posted_date=[]; job_type_lis=[]; comp_name=[]; loc=[]; job_links=[]; apply_links=[]; description=[]; domain_lis=[]
    
    # Finding the navigation elements for job categories
    cat_cls = driver.find_element(By.CLASS_NAME, 'magic__nav')
    cat_lis = cat_cls.find_elements(By.TAG_NAME, 'li')
    # Extracting links for each job category
    cat_link_lis = [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in cat_lis]
    cat_link_lis = cat_link_lis[1:]  # Ignoring the first link which is not a job category
    
    pre_domain = []
    # Extracting domain names from category links
    for do in cat_link_lis:
        try:
            d = re.findall(r'(?<=\/remote-)(.*)(?=-jobs)', do)[0]
        except:
            d = re.findall(r'(?<=categories\/)(.*)(?=-jobs)', do)[0]
        pre_domain.append(d)
        
    i = 0   
    
    # Looping through each job category
    for link in cat_link_lis:
        driver.get(link)
        time.sleep(4)
        pattern = r'https://weworkremotely.com/remote-jobs/[^#]+'
        # Extracting job links within the category
        all_job = driver.find_elements(By.CLASS_NAME, 'feature')
        anchor_tag = driver.find_elements(By.TAG_NAME, 'a')
        all_job_link = [a.get_attribute('href') for a in anchor_tag]
        all_job_link = [item for item in all_job_link if item is not None]
        all_job_link = [re.findall(pattern, link) for link in all_job_link]
        all_job_link = [value for sublist in all_job_link for value in sublist]
        
        print(len(all_job_link))
        d = pre_domain[i]
        # Looping through each job link
        for p_link in all_job_link:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            print(p_link)
            
            driver.get(p_link)
            time.sleep(2)
            
            con = driver.find_element(By.CLASS_NAME, 'content')
            
            try:
                card = driver.find_element(By.CLASS_NAME, 'company-card')
                time.sleep(2)
                # Extracting job details
                c_name = card.find_element(By.TAG_NAME, 'h2').text
                location = card.find_element(By.TAG_NAME, 'h3').text
                if location == 'Top 100':
                    location = card.find_elements(By.TAG_NAME, 'h3')[1].text
                elif location == 'Pro':
                    location = card.find_elements(By.TAG_NAME, 'h3')[1].text
                elif location == 'Website':
                    location = None
                print(location)
                if location == 'Website':
                    location = None
                print(location)
    
                title = con.find_element(By.TAG_NAME, 'h1').text
                date_raw = con.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[1]/h3[1]').text
                date1 = date_raw.replace("POSTED", "")
                date1 = date1.strip()
                job_type = con.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[1]/a[3]/span').text
                apply_link = card.find_element(By.XPATH, '//*[@id="job-cta-alt-2"]').get_attribute('href')
                desc = driver.find_element(By.ID, 'job-listing-show-container').text
                # Appending job details to respective lists
                job_title_lis.append(title); posted_date.append(date1); job_type_lis.append(job_type); comp_name.append(c_name)
                loc.append(location); job_links.append(p_link); apply_links.append(apply_link); description.append(desc)
                domain_lis.append(d)
            except:
                pass
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        i += 1
    driver.close()
    
    # Creating DataFrame with job details
    df = pd.DataFrame({
                "Domain_Name": domain_lis,
                "Job_Title": job_title_lis,
                "Posted_Date": posted_date,
                "Description": description,
                "Company_Name": comp_name,
                "Address": loc,
                "Job_Link": job_links,
                "Apply_Link": apply_links,
                "Job_Type": job_type_lis,
                })
    # Generating filename for CSV with current date
    today = date.today()
    filename = "Extracted_CSV//wwr_data_" + str(today) + ".csv"
    # Saving DataFrame to CSV
    df.to_csv(filename, index=False)
    df.to_csv('We_Work_Remotly.csv', index=False)

# Uncomment the following line to execute the function
# main_wwr()
