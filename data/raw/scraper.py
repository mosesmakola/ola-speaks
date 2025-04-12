import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

bible_books = {
    "Genesis": {"chapters": 50, "abbr": "Gen"},
    "Exodus": {"chapters": 40, "abbr": "Exo"},
    "Leviticus": {"chapters": 27, "abbr": "Lev"},
    "Numbers": {"chapters": 36, "abbr": "Num"},
    "Deuteronomy": {"chapters": 34, "abbr": "Deu"},
    "Joshua": {"chapters": 24, "abbr": "Jos"},
    "Judges": {"chapters": 21, "abbr": "Jud"},
    "Ruth": {"chapters": 4, "abbr": "Rut"},
    "1 Samuel": {"chapters": 31, "abbr": "1Sa"},
    "2 Samuel": {"chapters": 24, "abbr": "2Sa"},
    "1 Kings": {"chapters": 22, "abbr": "1Ki"},
    "2 Kings": {"chapters": 25, "abbr": "2Ki"},
    "1 Chronicles": {"chapters": 29, "abbr": "1Ch"},
    "2 Chronicles": {"chapters": 36, "abbr": "2Ch"},
    "Ezra": {"chapters": 10, "abbr": "Ezr"},
    "Nehemiah": {"chapters": 13, "abbr": "Neh"},
    "Esther": {"chapters": 10, "abbr": "Est"},
    "Job": {"chapters": 42, "abbr": "Job"},
    "Psalms": {"chapters": 150, "abbr": "Psa"},
    "Proverbs": {"chapters": 31, "abbr": "Pro"},
    "Ecclesiastes": {"chapters": 12, "abbr": "Ecc"},
    "Song of Solomon": {"chapters": 8, "abbr": "Son"},
    "Isaiah": {"chapters": 66, "abbr": "Isa"},
    "Jeremiah": {"chapters": 52, "abbr": "Jer"},
    "Lamentations": {"chapters": 5, "abbr": "Lam"},
    "Ezekiel": {"chapters": 48, "abbr": "Eze"},
    "Daniel": {"chapters": 12, "abbr": "Dan"},
    "Hosea": {"chapters": 14, "abbr": "Hos"},
    "Joel": {"chapters": 3, "abbr": "Joe"},
    "Amos": {"chapters": 9, "abbr": "Amo"},
    "Obadiah": {"chapters": 1, "abbr": "Oba"},
    "Jonah": {"chapters": 4, "abbr": "Jon"},
    "Micah": {"chapters": 7, "abbr": "Mic"},
    "Nahum": {"chapters": 3, "abbr": "Nah"},
    "Habakkuk": {"chapters": 3, "abbr": "Hab"},
    "Zephaniah": {"chapters": 3, "abbr": "Zep"},
    "Haggai": {"chapters": 2, "abbr": "Hag"},
    "Zechariah": {"chapters": 14, "abbr": "Zec"},
    "Malachi": {"chapters": 4, "abbr": "Mal"},
    "Matthew": {"chapters": 28, "abbr": "Mat"},
    "Mark": {"chapters": 16, "abbr": "Mar"},
    "Luke": {"chapters": 24, "abbr": "Luk"},
    "John": {"chapters": 21, "abbr": "Joh"},
    "Acts": {"chapters": 28, "abbr": "Act"},
    "Romans": {"chapters": 16, "abbr": "Rom"},
    "1 Corinthians": {"chapters": 16, "abbr": "1Co"},
    "2 Corinthians": {"chapters": 13, "abbr": "2Co"},
    "Galatians": {"chapters": 6, "abbr": "Gal"},
    "Ephesians": {"chapters": 6, "abbr": "Eph"},
    "Philippians": {"chapters": 4, "abbr": "Phi"},
    "Colossians": {"chapters": 4, "abbr": "Col"},
    "1 Thessalonians": {"chapters": 5, "abbr": "1Th"},
    "2 Thessalonians": {"chapters": 3, "abbr": "2Th"},
    "1 Timothy": {"chapters": 6, "abbr": "1Ti"},
    "2 Timothy": {"chapters": 4, "abbr": "2Ti"},
    "Titus": {"chapters": 3, "abbr": "Tit"},
    "Philemon": {"chapters": 1, "abbr": "Phm"},
    "Hebrews": {"chapters": 13, "abbr": "Heb"},
    "James": {"chapters": 5, "abbr": "Jam"},
    "1 Peter": {"chapters": 5, "abbr": "1Pe"},
    "2 Peter": {"chapters": 3, "abbr": "2Pe"},
    "1 John": {"chapters": 5, "abbr": "1Jo"},
    "2 John": {"chapters": 1, "abbr": "2Jo"},
    "3 John": {"chapters": 1, "abbr": "3Jo"},
    "Jude": {"chapters": 1, "abbr": "Jud"},
    "Revelation": {"chapters": 22, "abbr": "Rev"}
}

# Scrape verses from Bible.com
def scrape_bible_verses(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        container = soup.find("div", class_="ChapterContent_reader__Dt27r")
        if not container:
            logging.warning(f"No verse container found at: {url}")
            return []
        verses = container.find_all("span", class_="ChapterContent_content__RrUqA")
        return [v.get_text(strip=True) for v in verses if v.get_text(strip=True)]
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return []

# Handle extra metadata line in Lingala/Yoruba Psalms
def clean_title_verse(verses, book, lang):
    if book == "Psalms" and lang in ["lin", "yor"]:
        return verses[1:]
    return verses

# Scrape and align verses for one chapter
def process_chapter(book, abbr, chapter):
    urls = {
        "eng": f"https://www.bible.com/bible/111/{abbr}.{chapter}.NIV",
        "lin": f"https://www.bible.com/bible/1964/{abbr}.{chapter}.MNB",
        "yor": f"https://www.bible.com/bible/207/{abbr}.{chapter}.YCE"
    }

    logging.info(f"Starting: {book} Chapter {chapter}")
    verses_by_lang = {}

    for lang, url in urls.items():
        verses = scrape_bible_verses(url)
        verses_by_lang[lang] = clean_title_verse(verses, book, lang)
        logging.info(f"{lang.upper()} scraped {len(verses)} raw verses")

    # Ensure verse alignment
    min_len = min(len(verses_by_lang["eng"]), len(verses_by_lang["lin"]), len(verses_by_lang["yor"]))
    if min_len == 0:
        logging.warning(f"Skipped {book} {chapter} due to empty verse list")
        return []

    results = []
    for i in range(min_len):
        results.append({
            "book": book,
            "chapter": chapter,
            "verse": i + 1,
            "eng": verses_by_lang["eng"][i],
            "lin": verses_by_lang["lin"][i],
            "yor": verses_by_lang["yor"][i]
        })

    logging.info(f"{book} {chapter} processed with {min_len} verse pairs")
    return results

# Threaded scraper
def scrape_all_books():
    raw_bible = []
    tasks = []

    for book, meta in bible_books.items():
        for chapter in range(1, meta["chapters"] + 1):
            tasks.append((book, meta["abbr"], chapter))

    logging.info(f"Starting scraping with {len(tasks)} chapters...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(lambda args: process_chapter(*args), tasks)
        for chapter_data in results:
            raw_bible.extend(chapter_data)

    logging.info(f"Scraping complete. Total verses collected: {len(raw_bible)}")
    return raw_bible

# Save output
if __name__ == "__main__":
    bible_data = scrape_all_books()
    with open("bible_raw_data.json", "w", encoding="utf-8") as f:
        json.dump(bible_data, f, ensure_ascii=False, indent=2)
    logging.info("JSON written to bible_raw_data.json")