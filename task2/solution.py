from collections import defaultdict
from typing import DefaultDict, Optional

import requests
from bs4 import BeautifulSoup


def write_csv(data: str, file_name: str = "beasts", format="csv") -> None:
    file_name = file_name + "." + format

    with open(file_name, mode="w", encoding="utf-8") as file:
        file.write(data)


def format_count_to_csv(data: DefaultDict[str, int]) -> str:
    res = ""

    for k, v in data.items():
        res += f"{k},{v}\n"

    return res


def count_animals_by_first_letter(html: str, count: DefaultDict[str, int]) -> None:
    soup = BeautifulSoup(html, "html.parser")

    for li in soup.select(
        "div.mw-category-generated div#mw-pages div.mw-content-ltr ul li"
    ):
        tag = li.find("a")

        if tag:
            first_char_of_name = tag.text.strip()[0]

            count[first_char_of_name] += 1


def get_next_page_path(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")

    mw_pages_div = soup.find("div", id="mw-pages")
    if not mw_pages_div:
        return None

    next_page_link = mw_pages_div.find("a", string="Следующая страница")
    if next_page_link:
        return next_page_link.get("href")

    return None


def scrape_animals_and_save_counts() -> None:
    count_animals = defaultdict(int)

    url = "https://ru.wikipedia.org"
    path = "/wiki/Категория:Животные_по_алфавиту"

    while path:
        response = requests.get(url=url + path)
        print(f"count: {count_animals}\n")

        if response.status_code == 200:
            html = response.text
            count_animals_by_first_letter(html, count_animals)

            path = get_next_page_path(html)

    data = format_count_to_csv(count_animals)
    write_csv(data)


if __name__ == "__main__":
    scrape_animals_and_save_counts()
