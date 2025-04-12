from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

import requests
from bs4 import BeautifulSoup

URL = "https://www.bible.com/bible/111/PSA.42.NIV"
page = requests.get(URL)

skip = "ChapterContent_b__BLNfi"
skip1 = "ChapterContent_label"

soup = BeautifulSoup(page.content, "html.parser")

chapter = soup.find("div", class_ = "ChapterContent_reader__Dt27r")

more = True

while more == True:
    try:
        print(chapter.find_next("div", class_="ChapterContent_content_RrUqA"))
    except:
        more = False

# all_content = chapter.find_all("div", class_="ChapterContent_content__RrUqA")

# print(all_content)



# service = Service(executable_path="chromedriver")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# bible_books = {
#     "Genesis": {"chapters": 50, "abbr": "Gen"},
#     "Exodus": {"chapters": 40, "abbr": "Exo"},
#     "Leviticus": {"chapters": 27, "abbr": "Lev"},
#     "Numbers": {"chapters": 36, "abbr": "Num"},
#     "Deuteronomy": {"chapters": 34, "abbr": "Deu"},
#     "Joshua": {"chapters": 24, "abbr": "Jos"},
#     "Judges": {"chapters": 21, "abbr": "Jud"},
#     "Ruth": {"chapters": 4, "abbr": "Rut"},
#     "1 Samuel": {"chapters": 31, "abbr": "1Sa"},
#     "2 Samuel": {"chapters": 24, "abbr": "2Sa"},
#     "1 Kings": {"chapters": 22, "abbr": "1Ki"},
#     "2 Kings": {"chapters": 25, "abbr": "2Ki"},
#     "1 Chronicles": {"chapters": 29, "abbr": "1Ch"},
#     "2 Chronicles": {"chapters": 36, "abbr": "2Ch"},
#     "Ezra": {"chapters": 10, "abbr": "Ezr"},
#     "Nehemiah": {"chapters": 13, "abbr": "Neh"},
#     "Esther": {"chapters": 10, "abbr": "Est"},
#     "Job": {"chapters": 42, "abbr": "Job"},
#     "Psalms": {"chapters": 150, "abbr": "Psa"},
#     "Proverbs": {"chapters": 31, "abbr": "Pro"},
#     "Ecclesiastes": {"chapters": 12, "abbr": "Ecc"},
#     "Song of Solomon": {"chapters": 8, "abbr": "Son"},
#     "Isaiah": {"chapters": 66, "abbr": "Isa"},
#     "Jeremiah": {"chapters": 52, "abbr": "Jer"},
#     "Lamentations": {"chapters": 5, "abbr": "Lam"},
#     "Ezekiel": {"chapters": 48, "abbr": "Eze"},
#     "Daniel": {"chapters": 12, "abbr": "Dan"},
#     "Hosea": {"chapters": 14, "abbr": "Hos"},
#     "Joel": {"chapters": 3, "abbr": "Joe"},
#     "Amos": {"chapters": 9, "abbr": "Amo"},
#     "Obadiah": {"chapters": 1, "abbr": "Oba"},
#     "Jonah": {"chapters": 4, "abbr": "Jon"},
#     "Micah": {"chapters": 7, "abbr": "Mic"},
#     "Nahum": {"chapters": 3, "abbr": "Nah"},
#     "Habakkuk": {"chapters": 3, "abbr": "Hab"},
#     "Zephaniah": {"chapters": 3, "abbr": "Zep"},
#     "Haggai": {"chapters": 2, "abbr": "Hag"},
#     "Zechariah": {"chapters": 14, "abbr": "Zec"},
#     "Malachi": {"chapters": 4, "abbr": "Mal"},
#     "Matthew": {"chapters": 28, "abbr": "Mat"},
#     "Mark": {"chapters": 16, "abbr": "Mar"},
#     "Luke": {"chapters": 24, "abbr": "Luk"},
#     "John": {"chapters": 21, "abbr": "Joh"},
#     "Acts": {"chapters": 28, "abbr": "Act"},
#     "Romans": {"chapters": 16, "abbr": "Rom"},
#     "1 Corinthians": {"chapters": 16, "abbr": "1Co"},
#     "2 Corinthians": {"chapters": 13, "abbr": "2Co"},
#     "Galatians": {"chapters": 6, "abbr": "Gal"},
#     "Ephesians": {"chapters": 6, "abbr": "Eph"},
#     "Philippians": {"chapters": 4, "abbr": "Phi"},
#     "Colossians": {"chapters": 4, "abbr": "Col"},
#     "1 Thessalonians": {"chapters": 5, "abbr": "1Th"},
#     "2 Thessalonians": {"chapters": 3, "abbr": "2Th"},
#     "1 Timothy": {"chapters": 6, "abbr": "1Ti"},
#     "2 Timothy": {"chapters": 4, "abbr": "2Ti"},
#     "Titus": {"chapters": 3, "abbr": "Tit"},
#     "Philemon": {"chapters": 1, "abbr": "Phm"},
#     "Hebrews": {"chapters": 13, "abbr": "Heb"},
#     "James": {"chapters": 5, "abbr": "Jam"},
#     "1 Peter": {"chapters": 5, "abbr": "1Pe"},
#     "2 Peter": {"chapters": 3, "abbr": "2Pe"},
#     "1 John": {"chapters": 5, "abbr": "1Jo"},
#     "2 John": {"chapters": 1, "abbr": "2Jo"},
#     "3 John": {"chapters": 1, "abbr": "3Jo"},
#     "Jude": {"chapters": 1, "abbr": "Jud"},
#     "Revelation": {"chapters": 22, "abbr": "Rev"}
# }

# english_bible_raw = {

# }

# ChapterContent_chapter__uvbXo

# for value in bible_books.values():
#     book = value["abbr"]
#     for i in range(value["chapters"]):
#         chapter = value["chapters"]
#         # time.sleep(5)

#         bible_url = f"https://www.bible.com/bible/111/{book}.{i+1}.NIV"
#         driver.get(bible_url)

# # print(bible_books["Genesis"]["chapters"])

# # driver.get("https://www.bible.com/bible/111/JHN.1.NIV")

# time.sleep(10)

# # driver.quit()