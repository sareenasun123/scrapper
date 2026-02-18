import csv
import json
import requests
from bs4 import BeautifulSoup


url = "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []

    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    all_books = []

    for book in books:
        title = book.h3.a['title']
        price_text = book.find('p', class_='price_color').text
        currency = price_text[0]
        price = float(price_text[1:])

        book_data = {
            "title": title,
            "currency": currency,
            "price": price
        }

        all_books.append(book_data)  # ✅ append data

    return all_books  # ✅ return after loop


# Call function
books = scrape_books(url)

# Write to JSON file
with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print("Data successfully written to books.json")

with open("books.csv", "w") as f:

    writer = csv.DictWriter(f, fieldnames=["title", "price", "currency"])
    writer.writeheader()
    writer.writerows(books)
    