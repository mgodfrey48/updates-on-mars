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

    try:
        # Create a dictionary to store the mars info to be returned
        mars = {}

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
        mars['news_title'] = news_title
        mars['news_paragraph'] = news_p



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
        mars['featured_image_url'] = featured_image_url


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

        # Add the html table to the mars_data dictionary
        mars['facts_table'] = html_table


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
        mars['hemisphere_img_urls'] = hemisphere_img_urls

        # Quit the browser
        browser.quit()

    except:
        browser.quit()
        mars = {'news_title': "Oops, Matt Damon is out on a mission right now. Try again!",
                'news_paragraph': '(all image links were pulled from Google Images)',
                'featured_image_url': "https://cdn2.lamag.com/wp-content/uploads/sites/6/2016/02/themartian2.jpg",
                'facts_table': 'Lost in space',
                'hemisphere_img_urls':[{'title': 'Rosey', 'img_url':'data:image/jpeg;base64,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'},
                                        {'title':'Rusty', 'img_url':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmDWNLPmXgmPh0agKbfSNsEzl5ca09-opixw&usqp=CAU'},
                                        {'title':'George', 'img_url':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoGpT0CO9vANvpEQ-mDZegc608xz7pkgn_Sg&usqp=CAU'},
                                        {'title':'Red', 'img_url':'data:image/jpeg;base64,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'}]
                }

    # Return data
    return mars