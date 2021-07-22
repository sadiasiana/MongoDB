from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    time.sleep(1)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = img_url + relative_image_path

    facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(facts_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    table = pd.read_html(facts_url)
    df = table[1]
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)
    html_table = df.to_html(classes=["table-striped table-dark"], justify="center")
    html_table = html_table.replace('\n', '')

    hemp_url = 'https://marshemispheres.com/'
    browser.visit(hemp_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    links = soup.find('div', class_='collapsible results').find_all('div',class_='item')

    hemisphere_img_urls = []
    for link in links:
        hem_title = link.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
        hem_url = 'https://marshemispheres.com/'
        each_hem_image_url = hem_url + link.find('a',class_='itemLink product-item')['href']
        browser.visit(each_hem_image_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        full_image_url = hem_url + soup.find_all('img', class_='wide-image')[0]['src']
        each_hemisphere_image = {
            "title" : hem_title,
            "image_url" : full_image_url
        }
        hemisphere_img_urls.append(each_hemisphere_image)

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'html_table': html_table,
        'hemisphere_img_urls': hemisphere_img_urls
    }

    browser.quit()

    return mars_data
