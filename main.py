from bs4 import BeautifulSoup
import requests
import csv

from datetime import datetime

#template = 'https://ca.indeed.com/jobs?q={}&l={}'
def get_url(position,location):
    """Generate a URL from a position and location"""
    template = 'https://ca.indeed.com/jobs?q={}&l={}'
    url = template.format(position,location)
    return url


def get_record(card):
    """EXTRACT JOB DATA FROM A SINGLE RECORD"""
    atag = card.h2.a
    job_title = atag.get('title')
    job_url = 'https://ca.indeed.com/'+ atag.get('href')
    company = card.find('span','company').text.strip()
    job_location = card.find('div','recJobLoc').get('data-rc-loc')
    job_summary = card.find('div','summary').text.strip()
    post_date = card.find('span','date').text
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        job_salary = card.find('span','salaryText').text.strip()
    except AttributeError:
        job_salary = 'Not Provided'
    record = (job_title,company,job_location,post_date,today,job_summary,job_salary,job_url)

    return record


def main(position,location):
    records = []
    url =get_url(position,location)
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')
        for card in cards:
            record = get_record(card)
            records.append(record)
        try:
            url = 'https://ca.indeed.com/' + soup.find('a',{'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
    with open('resultsfromjobsearch','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title','Company','Location','Date Posted','Date Extracted','Summary','Salary','Job URL'])
        writer.writerows(records)

main('engineering co op','canada')










