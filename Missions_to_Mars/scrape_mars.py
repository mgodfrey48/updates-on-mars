#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set up the executable path needed to scrape the webpages
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Create a dictionary to store the mars info to be returned
    mars_data = {}

    ###### Find the first article title and summary paragraph #######
    # Open the website to find news about mars
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the first element with the news title, and the first element with the paragraph text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Add title and paragraph text to the mars_data dictionary
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p



    ###### Find the featured image ######
    # Open the website to scrape and find the featured space image
    images_url = 'https://spaceimages-mars.com/'
    browser.visit(images_url)

    # HTML object
    html2 = browser.html

    # Parse HTML with Beautiful Soup
    soup2 = BeautifulSoup(html2, 'html.parser')

    # Retrieve the image url
    image = soup2.find('img', class_='headerimage fade-in')
    link_to_image = image['src']
    featured_image_url = images_url + link_to_image

    # Add the image url to the mars_data dictionary
    mars_data['featured_image_url'] = featured_image_url


    ###### Find some fun facts about Mars! ######
    # Open the Mars facts website
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)

    # Scrape the website to grab the table with Mars and Earth information
    tables = pd.read_html(facts_url)
    facts = tables[0]
    facts

    # Set the first row in the table to be the column names
    facts.columns = facts.iloc[0]

    # Drop the row of data used to name the table columns
    facts = facts.drop(facts.index[0])

    # Reset the index of the table
    facts = facts.set_index('Mars - Earth Comparison')

    # Write the dataframe into an HTML script
    html_table = facts.to_html()

    # Clean up the html code
    html_table = html_table.replace('\n', '')

    # Add the html table to the mars_data dictionary
    mars_data['facts_table'] = html_table


    ###### Scrape the hemisphere images ######
    # Open the website that has the photos of Mars' hemispheres
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Find find links to each hemisphere page
    thumbnails = soup.find_all('div', class_='description')

    # Create a list to store dictionaries holding the hemisphere image info
    hemisphere_img_urls = []

    # Loop through each thumbnail element 
    for thumb in thumbnails:
        
        # Store the title of the image
        title = thumb.find('h3').text
        
        # Find the html link to the high res image page
        link = thumb.find('a')['href']

        # Open the page that has the high res image
        image_page_url = hemispheres_url + link
        browser.visit(image_page_url)

        # Create a new HTML object
        image_page_html = browser.html

        # Parse HTML with Beautiful Soup
        image_soup = BeautifulSoup(image_page_html, 'html.parser')
        
        # Find the image tag, pull out the src, append the image link to the original url
        image_link = image_soup.find('img', class_='wide-image')['src']
        img_url = hemispheres_url + image_link
        
        # Add the title and image url as a dictionary to the hemisphere image urls list
        hemisphere_img_urls.append({'title': title, 'img_url': img_url})

    # Add the hemisphere image urls to the mars_data dictionary
    mars_data['hemisphere_img_urls'] = hemisphere_img_urls

    # Quit the browser
    browser.quit()

    # Return data
    return mars_data