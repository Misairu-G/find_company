import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_glassdoor_reviews(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code / 200 != 1:
        with open("error_response.html", "wb") as resp_fd:
            resp_fd.write(response.content)
        raise ValueError(f"The URL {url} returns a invalid response with code {response.status_code}.")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    reviews = soup.find_all('div', class_='gdReview')
    data = []
    for review in reviews:
        try:
            company_name = review.find('a', class_='employerName').get_text(strip=True)
            rating = review.find('span', class_='ratingNumber').get_text(strip=True)
            data.append({'Company Name': company_name, 'Rating': rating})
        except AttributeError:
            continue

    return data

def save_to_csv(data, filename='glassdoor_reviews.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def main():
    # 替换成你的实际目标URL
    url = 'https://www.glassdoor.com.au/Reviews/index.htm?overall_rating_low=3.5&page=1&locId=2265449&locType=C'
    data = fetch_glassdoor_reviews(url)
    save_to_csv(data)
    print('数据已经保存到CSV文件。')

if __name__=="__main__":
    main()
