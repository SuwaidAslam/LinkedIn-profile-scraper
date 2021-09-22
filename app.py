import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def chrome(headless=False):
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome(executable_path=r'driver/chromedriver.exe', options=opt,desired_capabilities=d)
    browser.implicitly_wait(10)
    return browser
## Pass True if you want to hide chrome browser
browser = chrome(True)
browser.get('https://www.linkedin.com/uas/login')
browser.implicitly_wait(3)
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]


elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

info = []

links = ['https://www.linkedin.com/in/suwaidaslam/',
        # 'https://www.linkedin.com/in/amna-sadiq-743ab0164/',
        # 'https://www.linkedin.com/in/anjana-dheeraj-814660178/',
        # 'https://www.linkedin.com/in/munawar-hussain-70734b38/',
        ]

for link in links:
    browser.get(link)
    browser.implicitly_wait(1)
    def scroll_down_page(speed=8):
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = browser.execute_script("return document.body.scrollHeight")

    scroll_down_page(speed=8)

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')

    # Get Name of the person
    try:
        name_div = soup.find('div', {'class': 'pv-text-details__left-panel mr5'})
        first_last_name = name_div.find('h1').get_text().strip()
    except:
        first_last_name = None
    
    # Get Talks about section info
    try:
        talksAbout_tag = name_div.find('div', {'class': 'text-body-small t-black--light break-words pt1'})
        talksAbout = talksAbout_tag.find('span').get_text().strip()
    except:
        talksAbout = None
    
    # Get Location of the Person
    try:
        location_tag = name_div.find('div', {'class': 'pb2'})
        location = location_tag.find('span').get_text().strip()
    except:
        location = None
    
    # Get Title of the Person
    try:
        title = name_div.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
    except:
        title = None
    
    # Get Company Link of the Person
    try:
        exp_section = soup.find('section', {'id':'experience-section'})
        exp_section = exp_section.find('ul')
        li_tags = exp_section.find('div')
        a_tags = li_tags.find('a')

        company_link = a_tags['href']
        company_link = 'https://www.linkedin.com/' + company_link
    except:
        company_link = None

    # Get Job Title of the Person
    try:
        job_title = li_tags.find('h3', {'class': 't-16 t-black t-bold'}).get_text().strip()
    except:
        job_title = None
    
    # Get Company Name of the Person
    try:
        company_name = li_tags.find('p', {'class': 'pv-entity__secondary-title t-14 t-black t-normal'}).get_text().strip()
    except:
        company_name = None

    contact_page = link + 'detail/contact-info/'
    browser.get(contact_page)
    browser.implicitly_wait(1)

    contact_card = browser.page_source
    contact_page = BeautifulSoup(contact_card, 'lxml')
    # Get Linkdin Profile Link and Contact details of the Person
    try:
        contact_details = contact_page.find('section', {'class': 'pv-profile-section pv-contact-info artdeco-container-card ember-view'})
        contacts = []
        for a in contact_details.find_all('a', href=True):
            contacts.append(a['href'])
    except:
        contacts.append('')
    info.append([first_last_name, title, company_link, job_title, company_name, talksAbout, location, contacts])
    time.sleep(5)


column_names = ["Full Name", "Title", "Company URl", 'Job Title', 
                'Company Name', 'Talks About', 'Location', 'Profile Link and Contact']
df = pd.DataFrame(info, columns=column_names)
df.to_csv('data.csv', index=False)

print(".................Done Scraping!.................")
browser.quit()