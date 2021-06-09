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

    # Set the exec path and init the chrome browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)


    ##Visit the Nasa mars news site
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    # Optional delay for loading the page
    sleep(2)
    html = browser.html
    news_ = soup(html, 'html.parser')
    print(news_)


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
        news_list.append({"title": news_titles[i].get_text(
        ), "paragraph": news_paragraphs[i].get_text()})
    news_list


    # Featured Image
    featured_image_dict = scrape_featured_img()

    # MARS FACTS
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    sleep(2)

    # Scrape HTML table into list of dataframes
    df_list = pd.read_html(facts_url, match='Mars - Earth Comparison')
    print(df_list[0])

    #facts_list = []
    # for index, row in df_list[0].iterrows():
    #     print(row[2])


    # Export to Html
    facts_html = df_list[0].to_html('facts_html.html', index=False)
    print(facts_html)

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

    browser.quit()

    #comparison_list_type = df_list[0].set_index(df_list[0].columns[0]).T.to_dict('list')
    #comparison_list_type


    comparison_index_type = df_list[0].set_index(
        df_list[0].columns[0]).to_dict('index')
    comparison_index_type


    aq = {'news': news_list, 'fimage': featured_image_dict,
          'comparison': comparison_index_type, 'mars_hemispheres': mars_hemispheres_list}
  
    mars_data = {"news": news_list,
                 "fimage": featured_image_dict,
                 "hemisphere": mars_hemispheres_list,
                 "facts": comparison_index_type
                 }

    ###### Setup MongoDB - Insert the data
    conn = ("mongodb+srv://"+username+":"+password +
            "@cluster0.ow6cz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

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

    return mars_data

asd = scrape_data()


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
