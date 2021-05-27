#!/usr/bin/env python
# coding: utf-8


# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from time import sleep

#get_ipython().system('which chromedriver')

def scrape_data():
    # Set the exec path and init the chrome browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)


    # Visit the Nasa mars news site
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    # Optional delay for loading the page
    sleep(2)

    html = browser.html
    news_ = soup(html, 'html.parser')

    slide_elem = news_.select_one('ul.item_list li.slide')
    slide_elem

    # Find the parent element of title
    slide_elem.find("div", class_="content_title")

    # Use the parent element to find the first 'a' tag and save it as `news_title`
    news_title = slide_elem.find("div", class_="content_title").get_text()
    news_title

    # Find paragraph related with the article
    news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    news_p

    # Putting all together into For loop to scrape all news and paragraphs
    news_titles = news_.find_all('div', class_='content_title')
    # Remove the first element which is irrelevant
    news_titles.pop(0)
    news_titles[0]

    # Find paragraphs and store into a list
    news_paragraphs = news_.find_all('div', class_='article_teaser_body')
    news_paragraphs[1].get_text()

    # Create a list of news and paragraphs
    news_list = []
    for i in range(len(news_paragraphs)):
        news_list.append((news_titles[i].get_text(),
                        news_paragraphs[i].get_text()))
    news_list


    # Featured Image
    base_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(base_image_url)
    sleep(2)

    browser.click_link_by_partial_href('/images')
    sleep(2)

    browser.find_link_by_partial_href("original_images").click()
    sleep(1)
    featured_image_url = browser.url


    # MARS FACTS
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    sleep(2)

    # Scrape HTML table into list of dataframes
    df_list = pd.read_html(facts_url, match='Mars - Earth Comparison')

    # Export to Html
    facts_html = df_list[0].to_html('facts_html.html', index=False)

    # Visist Mars webpage
    base_mars_url = 'https://astrogeology.usgs.gov/'
    url_s = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_s)
    sleep(1)

    mars_html = browser.html
    mars_ = soup(mars_html, 'html.parser')
    items_ = mars_.find_all('div', class_='item')

    # Create a list of hemispheres' titles and full size images
    mars_hemispheres_list = []
    for i in range(len(items_)):
        # Visit links
        browser.visit(base_mars_url.rstrip(
            base_mars_url[-1]) + items_[i].a["href"])
        # Find the full image link and append it to list
        mars_hemispheres_list.append({"title": items_[i].h3.text,
                                    "img_url": browser.links.find_by_partial_href("full.jpg")[0]['href']})

    browser.quit()

    # Convert df to dictionary
    comparison_index_type = df_list[0].set_index(df_list[0].columns[0]).to_dict('index')

    aq = {'news': news_list, 'fimage': featured_image_url,'comparison': comparison_index_type, 'mars_hemispheres': mars_hemispheres_list}

    print(aq)
    return aq
