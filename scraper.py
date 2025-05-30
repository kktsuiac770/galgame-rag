import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_long_comment_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    comment_container = soup.select_one('div#all_comment')
    if comment_container:
        for comment_div in comment_container.find_all('div', class_=lambda c: c and c.endswith('comment_pagging')):
            a_tag = comment_div.find('a', href=True)
            if a_tag and a_tag['href'].startswith('memo.php?'):
                urls.append(a_tag['href'])
    return urls

def scrape_long_comments(urls):
    comments = []
    for url in urls:
        full_url = f"https://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/{url}"
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        comment_divs = soup.select('div#memo')
        for div in comment_divs:
            comments.append(div.get_text(strip=True))
    return comments

def scrape_game_id(game_id): 
    base_url = f"https://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/game_comment_time.php?game={game_id}#all_comment"
    long_comment_urls = scrape_long_comment_urls(base_url)
    long_comments = scrape_long_comments(long_comment_urls)

    os.makedirs("data", exist_ok=True)
    with open(f"data/{game_id}.json", "w", encoding="utf-8") as f:
        json.dump(long_comments, f, ensure_ascii=False, indent=2)
    
    return long_comments


def get_comments(game_id):
    data_path = f"data/{game_id}.json"
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return scrape_game_id(game_id)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <game_id>")
        sys.exit(1)
    game_id = sys.argv[1]
    scrape_game_id(game_id)

