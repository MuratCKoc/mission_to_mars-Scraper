#!/usr/bin/env python
# coding: utf-8


# Import Dependencies
from config import username, password
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from time import sleep

#get_ipython().system('which chromedriver')


def scrape_data():

    # Scrape News
    news_list = scrape_news()
    # Featured Image
    featured_image_dict = scrape_featured_img()

    mars_facts = scrape_facts()
    mars_hemispheres = scrape_hemispheres()

    #comparison_list_type = df_list[0].set_index(df_list[0].columns[0]).T.to_dict('list')
    #comparison_list_type
    # comparison_index_type = df_list[0].set_index(
    #     df_list[0].columns[0]).to_dict('index')
    # comparison_index_type

    mars_data = {"news": news_list,
                 "fimage": featured_image_dict,
                 "hemisphere": mars_hemispheres,
                 "facts": mars_facts
    }

    
    return mars_data




def scrape_news():

    # Set the exec path and init the chrome browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    try:
        #Visit the Nasa mars news site
        url = 'https://mars.nasa.gov/news'
        browser.visit(url)
        sleep(2)

        # Parse with bs4
        html = browser.html
        news_ = soup(html, 'html.parser')

        # Article Titles
        news_titles = news_.find_all('div', class_='content_title')
        # Remove the first element which is irrelevant
        news_titles.pop(0)
        news_titles[0]

        # Article paragraphs
        news_paragraphs = news_.find_all('div', class_='article_teaser_body')
        news_paragraphs[1].get_text()

        # Article url
        news_text = news_.find_all('div', class_='list_text')

        # Create a list of news and paragraphs
        news_list = []
        # Loop thru the articles
        for i in range(len(news_paragraphs)):
            news_list.append({
                "title": news_titles[i].get_text(),
                "paragraph": news_paragraphs[i].get_text(),
                "url": url+news_text[i].a['href']})
        news_list

    finally:
        browser.quit()
    return news_list


def scrape_featured_img():
    # Featured image:
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    featured_image_dict = {}

    try:
        #Visit base page
        base_image_url = 'https://www.jpl.nasa.gov/images'
        browser.visit(base_image_url)
        sleep(2)

        # Check Mars from filters
        browser.is_element_present_by_id('filter_Mars')
        browser.find_by_id('filter_Mars').first.click()
        sleep(2)

        # Click the first link
        browser.click_link_by_partial_href('/images')
        sleep(2)

        # Get title
        featured_title = browser.find_by_tag('h1').first.value
        print(featured_title)

        # Get url
        featured_image_url = browser.url
        featured_image_dict = {
            "title": featured_title, "url": featured_image_url}
        print(featured_image_dict)
    finally:
        browser.quit()

    # Return the dictionary
    return featured_image_dict


def scrape_facts():

    # Set the exec path and init the chrome browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    try:
        #Visit the Nasa mars news site
        mars_url = 'https://space-facts.com/mars/'
        sleep(2)
        mars_df = pd.read_html(mars_url)[1]

        mars_df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
        mars_html_table = mars_df.to_html(header=None, index=False)
        mars_html_table.replace('\n', '')
    finally:
        browser.quit()
    return mars_html_table


def scrape_hemispheres():

    # Set the exec path and init the chrome browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    try:
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
        mars_hemispheres_list
    finally:
        browser.quit()
    return mars_hemispheres_list

def update_database():
    ###### Setup MongoDB - Insert the data
    conn = ("mongodb+srv://"+username+":"+password +
            "@cluster0.ow6cz.mongodb.net/mars_db?retryWrites=true&w=majority")

    client = pymongo.MongoClient(conn)

    db_name = 'mars_db'

    # Check if db exists, create one if it does not
    if db_name in dblist:
        print("The Database exists")
        mydb = client[db_name]
    else:
        print(f'The DB does not exists. Creating {db_name} for you.')
        # Create new database
        mydb = client[db_name]

    # If collection exists then drop
    try:
        mydb.drop_collection('news')
        mydb.drop_collection('fimage')
        mydb.drop_collection('comparison')
        mydb.drop_collection('mars_hemispheres')
    except:
        pass

    # Create Collections
    news = mydb['news']
    fimage = mydb['fimage']
    comparison = mydb['comparison']
    mars_hemispheres = mydb['mars_hemispheres']

    # Insert the lists to collections
    news.insert(news_list)
    fimage.insert(featured_image_dict)
    comparison.insert(comparison_index_type)
    mars_hemispheres.insert(mars_hemispheres_list)

