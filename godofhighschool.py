#! /usr/bin/python

import feedparser
import praw
import time
import os

naver_page = "http://comic.naver.com/webtoon/list.nhn?titleId=318995&weekday=fri"

def get_latest_scan():
    mngcow_feed_link = "http://mngacow.com/manga-rss/the-god-of-high-school/"
    print("Getting new scan")
    scan_feed = feedparser.parse(mngcow_feed_link)
    for article in scan_feed.entries[:1]:
        return article.link + "?all"

def get_last_submission(r, name):
    bot = praw.objects.Redditor(r,user_name=name)
    submissions = bot.get_submitted()
    return next(submissions)

def start():
    # make variables
    scan = get_latest_scan()
    raw = "http://comic.naver.com/webtoon/detail.nhn?titleId=318995&no=142&weekday=fri"
    subreddit_name = "gohs"
    chapter = scan.replace('http://mngacow.com/the-god-of-high-school/', '').replace('/?all', '')
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

    time.sleep(60)
    print("Making new announcement")
    discussion = get_last_submission(r, "godofhighschool_bot").short_link

    submission_description = "#### [Latest Chapter](%s) | [Korean Raws](%s) | [Discussion](%s)\n\nA subreddit dedicated to the discussion of God Of High School.\n\n###Subreddit Rules\n\n * Always Follow the [Reddiquette](http://www.reddit.com/wiki/reddiquette)\n * Anything Racist, Sexist or Homophobic will be removed regardless of its relevance or popularity.\n * No image macros or memes.\n * No NSFW content (Rule 34, etc.)\n * It is recommended that you post a link to the source of where you found artwork but it is not required.\n\n###Scanlators\n\n 1. [Mangacow](http://mngacow.com/)\n\n###Related Subreddits\n\n 1. /r/manga\n 1. /r/manhwa\n 1. /r/TowerofGod" % (scan, raw, discussion)
    r.update_settings(r.get_subreddit(subreddit_name), description=submission_description)

start()
