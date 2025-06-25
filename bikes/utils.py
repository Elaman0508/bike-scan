import requests
from bs4 import BeautifulSoup


# 💸 Логика определения цены по типу
def get_price_by_type(bike_type):
    prices = {
        "fixie": "от 200 до 400 $",
        "bmx": "от 150 до 350 $",
        "mtb": "от 400 до 800 $",
        "road": "от 500 до 1500 $",
        "keirin": "от 700 до 2000 $"
    }
    return prices.get(bike_type.lower(), "неизвестно")


# 🧲 Парсинг OLX по ключу
def search_olx_bikes(query, limit=5):
    url = f"https://www.olx.kz/list/q-{query.replace(' ', '-')}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        listings = soup.select("div.offer-wrapper") or soup.select("li[data-id]")

        for item in listings[:limit]:
            title_tag = item.select_one("strong")
            price_tag = item.select_one(".price")
            link_tag = item.find("a", href=True)

            if title_tag and link_tag:
                results.append({
                    "title": title_tag.text.strip(),
                    "price": price_tag.text.strip() if price_tag else "—",
                    "url": link_tag["href"],
                })

        return results

    except Exception as e:
        print("Ошибка при парсинге OLX:", e)
        return []
