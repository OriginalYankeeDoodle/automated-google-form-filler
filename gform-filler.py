import requests
from bs4 import BeautifulSoup
import re
from datetime import date

def get_question_ids(url):
    
    ''' Returns a list of entry IDs of various fields in a Google Form'''
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    content = soup.body.find_all(text = re.compile('var FB'))

    match_ids = re.findall('(?<=\[\[)(\d+)', str(content))
    question_ids = ['entry.' + x for x in match_ids[1:]]
    
    return question_ids


def send_answers(url, fname, lname, section, roll_no, subject, date, attendance): #Change the parameters other than url as per your needs
    
    '''Sends the answers for a Google Form'''
    
    ids = get_question_ids(url)
    
    answers = [fname, lname, section, roll_no, subject, date, attendance]
    response = dict(zip(ids, answers))
    
    if 'viewform' in url:
        s = url.index('viewform') 
        response_url = url.replace(url[s::], 'formResponse?')
        
    try:
        #This tries to send the data (answers) using POST method.
        r = requests.post(response_url, response)
        if r.status_code == 200:
            return '[!] Attendence posted !'
        else:
            raise Exception

    except:
        try:
            #This tries to send the data (answers) using URL Reconstruction if the POST method fails.
            ans_list = [x + '=' + y for x, y in zip(ids, answers)]
            
            for i in range(0, len(ans_list)):
                response_url += ans_list[i]
                response_url += '&'
                
            response_url.strip("&")    
            r = requests.get(response_url)
            status = r.status_code
            
            if status == 200:
                return '[!] Attendance sent !'
            else:
                raise Exception
        except:
            #If both POST method and URL Recosntruction fails, it returns an error message
            return '[!] Attendance not sent !'
                

#Change the URL and other parameters to be passed inside send_answers() as per your need.

url = 'https://docs.google.com/forms/d/e/1FAIpQLSf3KA-jsao7DhQEnzf3zV9SLi8sxQBd5zAIdupZVxLm0Wjmqw/viewform?usp=sf_link'

fname = 'First'
lname = 'Last'
section = 'A'
roll_no = '11'
subject = 'Science'
date = str(date.today())
attendance = 'Present'

print(send_answers(url, fname, lname, section, roll_no, subject, date, attendance))
