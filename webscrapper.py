#!/usr/bin/python3

import os
import random
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from models import Claimed, Scraped, Session

load_dotenv()

with open("user_agets_browsers.txt", "r") as f:
    useragents = [useragent.replace("\n", "") for useragent in f.readlines()]
url = os.environ.get("WEBSITE_URL")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")


def greetings():
    print(
        r"""
  ____                          _   _             _             
 / ___|___  _   _ _ __ ___  ___| | | |_   _ _ __ | |_ ___ _ __  
| |   / _ \| | | | '__/ __|/ _ \ |_| | | | | '_ \| __/ _ \ '__| 
| |__| (_) | |_| | |  \__ \  __/  _  | |_| | | | | ||  __/ |    
 \____\___/ \__,_|_|  |___/\___|_| |_|\__,_|_| |_|\__\___|_|    
                                                                
"""
    )


def get_headers():
    domain_name = url.split("://")[1].split("/")[0]
    useragent = random.choice(useragents)
    headers = {
        "Host": f"{domain_name}",
        "User-Agent": f"{useragent}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
    }
    return headers


def get_request():
    header = get_headers()
    response = requests.get(url=url, headers=header)
    return response.text


def process_with_soup(responded):
    soup = BeautifulSoup(responded, "lxml")
    course_list_class_name = "wp-block-kadence-rowlayout alignnone"
    course_name_link_class_name = "external_link_title"
    course_category_class_name = "mb-10 mt-10"
    course_category_blocklist = [
        "Office Productivity",
        "Business",
        "Personal Development",
        "Health & Fitness",
        "Marketing",
        "Finance & Accounting",
    ]
    listings = [
        (
            courses.find("a", class_=course_name_link_class_name),
            courses.find("p", class_=course_category_class_name)
            .text.strip()
            .split("Category:")[1]
            .strip(),
        )
        for courses in soup.find_all("div", class_=course_list_class_name)
        if courses.find("p", class_="mb-10 mt-10")
        .text.strip()
        .split("Category:")[1]
        .strip()
        not in course_category_blocklist
    ]
    CourseList = []
    for i in range(len(listings)):
        CourseList.append(
            {
                "Title": f"{listings[i][0].text.strip()}",
                "Link": f"{listings[i][0]['href'].split("/?couponCode=")[0]}",
                "Coupon": f"{listings[i][0]['href'].split("/?couponCode=")[1]}",
                "Category": f"{listings[i][1]}",
            }
        )
    return CourseList


def save_data(course_tuple):
    session = Session()
    for course_entry in course_tuple:
        existing_item = (
            session.query(Scraped).filter_by(link=course_entry["Link"]).first()
        )
        existing_item_in_claimed = (
            session.query(Claimed).filter_by(link=course_entry["Link"]).first()
        )
        if existing_item is None and existing_item_in_claimed is None:
            course_record = Scraped(
                title=course_entry["Title"],
                link=course_entry["Link"],
                coupon=course_entry["Coupon"],
                category=course_entry["Category"],
            )
            session.add(course_record)
            display_entry(course_entry)
            craft_message(course_entry)
    session.commit()
    session.close()


def display_entry(ce):
    print(f"Title: {ce["Title"]}")
    print(f"Link: {ce["Link"]}")
    print(f"Coupon: {ce["Coupon"]}")
    print(f"Category: {ce["Category"]}")
    print("-" * 102)


def craft_message(centry):
    chat = f"""
Title: {centry["Title"]}
Link: <code>{centry["Link"]}</code>
Coupon: <code>{centry["Coupon"]}</code>
Category: {centry["Category"]}
"""
    try:
        send_telegram_message(bot_token, chat_id, chat)
    except Exception as e:
        print(f"SOMETHING WENT WRONG: {e}")


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=params)
    except Exception as e:
        print(f"SOMETHING WENT WRONG: {e}")
    finally:
        return response


if __name__ == "__main__":
    greetings()
    while True:
        course_list_output = process_with_soup(get_request())
        save_data(course_list_output)
        base_time_minutes = 15
        jitter = random.choice(range(1, 121))
        base_time_seconds = base_time_minutes * 60
        total_time_seconds = base_time_seconds + jitter
        total_minutes = total_time_seconds // 60
        total_remaining_seconds = total_time_seconds % 60
        print(
            f"Sleeping for {total_minutes} minutes {total_remaining_seconds} seconds..."
        )
        time.sleep(total_time_seconds)
