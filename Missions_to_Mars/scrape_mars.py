# This is the Python script that comes from the Jupyter Notebook: mission_to_mars.ipynb

# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)



def scrape():
    ###########################################
    ## NASA Mars News Web Scraping
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")

    # Finding the latest title and paragraph text
    slide_element = soup.select_one("ul.item_list li.slide")
    # Scrape the Latest News Title
    news_title = slide_element.find("div", class_="content_title").text
    # Scrape the Latest Paragraph Text
    news_p = slide_element.find("div", class_="article_teaser_body").text
    # Close the browser after scraping
    browser.quit()

    ###########################################
    ## JPL Mars Space Image - Feured Image
    # Link doesn't work - Instructor said to skip - Used the example url given

    featured_image_url = 'https://mars.nasa.gov/system/downloadable_items/45346_PIA22743-2.jpg'


    ###########################################
    ## Mars Facts Web Scraping
    url = 'https://space-facts.com/mars/'

    # Use pandas to read the html table data
    mars_facts = pd.read_html(url)
    # Read the first dictionary in the list into a pandas dataframe and name columns
    mars_facts_df = mars_facts[0]
    mars_facts_df .columns = ['Parameter', 'Value']
    # Convert the dataframe table into an html table
    mars_facts_table = mars_facts_df.to_html(index=False)
    mars_facts_table = mars_facts_table.replace('\n', '')
    mars_facts_table = mars_facts_table.replace('right', 'left')
    mars_facts_table = mars_facts_table.replace('dataframe', 'table table-striped table-bordered table-responsive-sm')

    ###########################################
    ## Mars Hemispheres Web Scraping
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html,"lxml")

    # Get the html containing the titles and put into a list
    title_list = soup.find_all('div', class_='description')
    
    # Loop through 
    # Initiate the list to store dictionaries
    hemisphere_image_urls = []
    for title in title_list:
        # Navigate browser to page then click on title link to hires image page
        browser.visit(url)
        browser.click_link_by_partial_text(title.a.h3.text)

        # Get page html and make beautifulsoup object
        html = browser.html
        soup = bs(html,"lxml")

        # Parse the image relative url then append to domain name
        img_url_list = soup.find('img', class_='wide-image')
        img_url = f"https://astrogeology.usgs.gov{img_url_list['src']}"

        # Create dictionary for hemisphere_image_urls
        post = {
                'title': title.a.h3.text,
                'img_url': img_url
                }
        hemisphere_image_urls.append(post)

    # Close the browser after scraping
    browser.quit()

    ###########################################
    ## Store data in a dictionary
    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'fact_table': mars_facts_table,
        'hemisphere_image_urls': hemisphere_image_urls
        }

    print(mars_data)
    return mars_data

    


