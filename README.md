
# Automated Job Scraping and Emailing

![App Screenshot](https://github.com/Pratiksha8799/Basic_Charts_Plotly/blob/main/images/AI.png)

The project aims to automate the process of job scraping from various websites based on user-provided criteria (skills and location) and then emailing the scraped data to the user.



## Features

- Website Selection: Users can select from various supported job websites like Seek, Bayt, We Work Remotely, Found It, or choose to scrape all supported websites simultaneously.
- Scraping: Upon selection, the system initiates scraping of the chosen website(s) to extract job listings based on the provided criteria.
- Email Notification: Once scraping is completed, the extracted data is compiled into CSV files and sent to the user's provided email address.
- Logging: All activities including scraping errors and email sending status are logged for future reference.

## Dependencies

To run this project, you will need to install following libraries.

* Flask: A micro web framework for Python.
* threading: Used for concurrent execution of tasks.
* smtplib: Library for sending emails using SMTP.
* email.mime: For composing email messages.
* logging: Library for event logging.
* os: For file and directory operations.
* time: For introducing delays.

## Setup:

* Install Python if not already installed. 
* Install Flask and other dependencies using pip.
```bash
  pip install Flask
```
* Configure Gmail account credentials (senders_email and sender_password) in the main_email function for email sending functionality.
* Ensure the Gmail account has less secure app access enabled.
## Deployment

To deploy this project run
* Clone the repository.
* Navigate to the project directory.
* Install required dependencies.
* Run the app. 
```bash
  python app.py
```
* Access the dashboard in your web browser at http://localhost:5001/.





## Usage
* Run the Flask application by executing the script.

```bash
python app.py
```
* Access the application through a web browser at http://localhost:5001/.
* Fill in the required fields on the web form:
   * Skills: Desired job skills.
   * Location: Desired job location.
    * Email: Email address to receive the scraped data.
    * Website: Select from available options (Seek, Bayt, We Work Remotely, Found It, or All Sites).

* Submit the form. The scraping process will commence.
* Upon completion, the extracted data will be emailed to the provided email address.
* Log files (scraping_log.log) will record all activities and errors encountered during scraping and email sending.

#### Note: Ensure proper internet connectivity and valid email credentials for successful scraping and emailing.


## Used By

The project can be utilized by individuals or organizations who are:

* Job Seekers: Individuals looking for job opportunities can use this project to gather listings from multiple job websites based on their desired skills and location. It provides a convenient way to explore various job options without manually visiting each website.

* Recruitment Agencies: Companies or agencies involved in recruitment can use this project to gather job listings for their clients or for internal research purposes. It streamlines the process of collecting job data from different sources, saving time and effort.

* HR Professionals: Human resource professionals within organizations can utilize this project to stay updated on job openings relevant to their industry or specific roles. It offers a centralized platform to monitor job listings from different websites.

* Freelancers: Freelancers seeking remote work opportunities can benefit from this project by easily accessing job listings from websites specializing in remote work opportunities, such as We Work Remotely.

* Researchers: Academics or researchers studying employment trends or job markets can use this project to gather data for analysis. It provides a systematic way to collect job-related information from various sources.

* Entrepreneurs: Entrepreneurs or startup founders looking to hire talent can use this project to scout for potential candidates across multiple job websites. It offers a cost-effective solution for small businesses to conduct initial talent searches.
## 🚀 Conclusion

In conclusion, the automated job scraping and emailing project offers a versatile solution for streamlining the process of job searching, data collection, and dissemination. By leveraging web scraping techniques and email automation


## Support

For support, email pratikshagarkar871999@gmail.com


## About me

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://medium.com/@pratiksha.garkar)

