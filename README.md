# Web Scraping Mission to Mars

![mission_to_mars](Images/mission_to_mars.png)

A web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines how I did.

## Step 1 - Scraping

Complete initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

* A Jupyter Notebook file called `mission_to_mars.ipynb` and used this to complete all of my scraping and analysis tasks. The following outlines what I scraped.

### NASA Mars News

* Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Store them in a list.

```python
# Scrape news titles and teasers
news_titles = news_.find_all('div',class_='content_title')
news_titles[1].get_text()

news_paragraphs = news_.find_all('div', class_='article_teaser_body')
news_paragraphs[1].get_text()
```

### JPL Mars Space Images - Featured Image

* Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
* Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.

```python
# Example:
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
```

### Mars Facts

* Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

```python
df_list = pd.read_html(facts_url, match='Mars - Earth Comparison',index_col=0)
df_list[0]
```

* Use Pandas to convert the data to a HTML table string.

### Mars Hemispheres

* Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
* You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
* Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
* Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

```python
# Example:
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    {"title": "Cerberus Hemisphere", "img_url": "..."},
    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
]
```

---

## Step 2 - MongoDB and Flask Application

Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
* Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.

  * Store the return value in Mongo as a Python dictionary.
* Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
* Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.


## Common Erros

* ChromeDriver supports another Chrome version. [Download the right one](https://chromedriver.chromium.org/downloads)
* Use Pymongo for CRUD applications for your database.
