#! /usr/bin/python

import praw
import os
import requests
from bs4 import BeautifulSoup

def get_latest_scan():
    print("Getting new scan")
    raw_link = "http://m.webtoons.com/episodeList?titleNo=66"
    response = requests.get(raw_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        latest_chapter = soup.find_all('p', class_='sub_title')[0].find('span').text[4:]
        article = "http://thcmpny.com/naver.html#66,"+latest_chapter
        print("Latest scan: "+article)
        response.close()
        return article
    else:
        print("Couldn't get latest scan")
        response.close()
        exit()

def get_latest_raw():
    naver_page = "http://comic.naver.com/webtoon/list.nhn?titleId=318995&no=142&weekday=fri"
    print("Getting latest raw")
    response = requests.get(naver_page)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        links=[]
        for link in soup.find_all('td', class_='title'):
            try:
                raw_link = link.find('a')['href']
            except:
                None
            links.append(raw_link)
        actual_link = "http://comic.naver.com" + links[0]
        print("Latest raw: "+actual_link)
        response.close()
        return actual_link
    else:
        print("Couldn't get latest web link")
        print(response.status_code)
        response.close()
        exit()

def get_last_submission(r, name):
    bot = praw.objects.Redditor(r,user_name=name)
    submissions = bot.get_submitted()
    return next(submissions)

def start():
    # make variables
    scan = get_latest_scan()
    raw = get_latest_raw()
    subreddit_name = "godofhighschool"
    chapter = scan.replace('http://thcmpny.com/naver.html#66,', '')
    submission_title = "God of High School - %s" % chapter
    submission_text = "RAW: %s\n\n**Please open the raw in a new tab to promote the author**\n----\nSCAN: %s" % (raw, scan)

    # login
    print("Logging in")
    r = praw.Reddit(user_agent='godofhighschool')
    r.login('godofhighschool_bot', os.environ.get('BOT_PASSWORD'))

    last_submission_title = get_last_submission(r, "godofhighschool_bot").title
    if (last_submission_title == submission_title):
        print("Nothing to do")
        exit()
   
    print("Submitting new post")
    submission = r.submit(subreddit_name, submission_title, submission_text)

start()
