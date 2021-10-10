import asyncio
import aiohttp
import argparse
import json
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from tqdm import tqdm


def parse_meta(article):
    """
    Collect meta info about the article
    """
    article_meta = article.find("div", {"class": "meta"})
    meta_fields = article_meta.find_all("p", {"class": "table"})

    return{
        "title": article.h1.get_text(),
        "category": [category.get_text() for category in meta_fields[0].find_all("a")],
        "date": meta_fields[1].time["content"],
        # "complexity": re.search(r'\d\.\d', meta_fields[2].a.get_text()).group(0)
    }


def parse_text(article):
    """
    Parse text of the article
    """
    # Some hacks applied: as a rule, the last <p> is the author.
    # Besides, we need to remove \xa0(NO-BREAK SPACE) symbol
    text = [p.get_text() for p in article.find_all("p", attrs={"class": None})]
    if article.find_all("p", attrs={"class": None}) and article.find_all("p", attrs={"class": None})[-1].i:
        text.pop()  # remove the author
    text = "\n".join(text)
    text = text.replace(u"\xa0", u" ")
    return text


async def parse_article(url, session):
    response = await session.get(url)
    html = await response.text()
    response.release()
    soup = BeautifulSoup(html, "lxml")
    article = soup.body.find_next(id="article")
    meta = parse_meta(article)
    text = parse_text(article)

    return {"id": url, "text": text} | meta


def get_articles_hrefs(url):
    """Returns href of news for a day"""
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")

    prefix = "https://nplus1.ru/"
    return [prefix + art.a["href"] for art in soup.find_all("article")]


def get_days(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n)).strftime("%Y/%m/%d")


async def collect_data(start_date, end_date, out_file):
    collection = []
    prefix = "https://nplus1.ru/news/"
    async with aiohttp.ClientSession() as session:
        for day in tqdm(get_days(start_date, end_date)):
            url = prefix + day
            day_articles = get_articles_hrefs(url)
            result = await asyncio.gather(*[parse_article(article_url, session) for article_url in day_articles])
            collection.extend(result)

    with open(out_file, "w") as file:
        json.dump(collection, file, ensure_ascii=False)


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--start",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=(datetime.now() - timedelta(days=1)),
        help="Start date to parse news in format %Y-%m-%d"
    )
    parser.add_argument(
        "--end",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=datetime.now(),
        help="End date to parse news in format %Y-%m-%d"
    )
    parser.add_argument(
        "--output",
        default="nplus1_news.json",
        help="Specify output file"
    )

    return parser.parse_args()


async def main():
    args = parse_args()
    await collect_data(start_date=args.start, end_date=args.end, out_file=args.output)


if __name__ == "__main__":
    asyncio.run(main())
