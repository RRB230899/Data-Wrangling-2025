import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_real_article_date(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=7)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        meta_tags = [
            {'property': 'article:published_time'},
            {'name': 'pubdate'},
            {'property': 'og:updated_time'},
            {'itemprop': 'datePublished'},
        ]

        for tag_attrs in meta_tags:
            meta_tag = soup.find('meta', attrs=tag_attrs)
            if meta_tag and meta_tag.get('content'):
                return meta_tag['content']

    except Exception as e:
        print(f"Failed to fetch article {url}: {e}")

    return None


def scrape_bing_news_final_fixed(query, max_pages=3):
    query = query.replace(' ', '+')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    articles = []
    page = 0

    while page < max_pages:
        first = page * 10
        url = f"https://www.bing.com/news/search?q={query}&first={first}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve page {page + 1} for query {query}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        news_cards = soup.find_all('div', class_='news-card')

        if not news_cards:
            print(f"No more articles found after page {page}. Stopping query: {query}")
            break

        for card in news_cards:
            try:
                title_tag = card.find('a', class_='title')
                title = title_tag.text.strip() if title_tag else ''
                link = title_tag['href'] if title_tag else ''

                snippet_tag = card.find('div', class_='snippet')
                snippet = snippet_tag.text.strip() if snippet_tag else ''

                published_text = ''
                publish_datetime_raw = None

                # Try to scrape publish date immediately
                if link:
                    print(f"Scraping article: {link}")
                    publish_datetime_raw = get_real_article_date(link)
                    time.sleep(1)  # Respectful delay to avoid hammering

                articles.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet,
                    'published_text': published_text,
                    'publish_datetime_raw': publish_datetime_raw,
                    'search_query': query.replace('+', ' ')
                })

            except Exception as e:
                print(f"Skipping a card due to error: {e}")

        page += 1
        time.sleep(1)

    return pd.DataFrame(articles)


def batch_scrape_bing_news_fixed(queries, years, max_pages=3):
    full_news_df = pd.DataFrame()

    for base_query in queries:
        for year in years:
            query = f"{base_query} {year}"
            print(f"\nScraping (up to {max_pages*10} articles) for query: {query}")
            news_df = scrape_bing_news_final_fixed(query, max_pages=max_pages)
            full_news_df = pd.concat([full_news_df, news_df], ignore_index=True)

    full_news_df = full_news_df.drop_duplicates(subset=['title'])
    return full_news_df


if __name__ == "__main__":
    queries = [
        "TSMC earthquake manufacturing disruption",
        "Taiwan earthquake chip factory",
        "TSMC server production earthquake",
        "semiconductor supply chain earthquake Taiwan",
    ]

    years = [2021, 2022, 2023, 2024, 2025]

    df = batch_scrape_bing_news_fixed(queries, years, max_pages=3)
    df.to_csv('tsmc_server_earthquake_scrape_full_fixed_final.csv', index=False)
    print(f"\nScraped {len(df)} total articles cleanly with real publish dates captured.")
