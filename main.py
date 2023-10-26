from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from datetime import date
from twilio.rest import Client

def grabURL():
    article_links_list = []
    results = []
    text_to_send = ''
    associate = False
    associate_string = ''

    # get list of URLs to visit and plunder!
    try:
        for page in range(1, 5):
            url = 'https://jobs.erieinsurance.com/go/Information-Technology-%d28IT%29/3020900/'
            r = requests.get(url)
            soup = bs(r.content, 'html.parser')
    except:
        text_to_send = '🚨 Failed on bs4 execution'

    # visit URLs and dig for gold!
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    try:

        count = 0
        for result in soup.find_all("a", class_="jobTitle-link"):
            if count % 2 == 0:
                results.append(result.get_text())
            count += 1

    except:
        text_to_send = '🚨 Failed on chromedriver execution'

    today = date.today()

    if 'Associate Software Engineer' in results: associate = True
    if associate: associate_string = '🤖 Associate SWE 🤖 is NOW POSTED'
    else: associate_string = '😭 Associate SWE 😭 is not posted..\n'

    text_to_send = "Erie Insurance IT Job Postings: \n\n" + associate_string + "\n" "Results: \n" + '\n\n'.join(results) + '\n\n' + "Today's Date: " + str(today)
    driver.quit()
    print(text_to_send)
    print(associate_string)


    # Actual $$$ texting stuff -- Comment out in order to save money
    account_sid = "[YOUR ACCOUNT SID HERE]"
        auth_token = "[YOUR AUTH ID HERE]"

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=text_to_send, to='+18144608705', from_='+18556093135')

    except:
        print('🚨 Error connecting to Twilio client')


if __name__ == '__main__':
    grabURL()
