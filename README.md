# Interested in knowing more about Mars??

This repo contains files to scrape various webpages for data, news, and images of Mars. 

Files:
* `mission_to_mars.ipynb` - jupyter notebook with code to scrape Mars data and images from the web
* `scrape_mars.py` - python file with a scrape function that uses the code from `mission_to_mars.ipynb` and returns the scraped data in a dictionary
* `app.py` - python file that creates a local host and mongo database, calls `scrape_mars.py`, adds the returned data to the mongo database, and renders that data onto a webpage

To use the files in this repository:
1. Clone the repository to your computer and open it in terminal.
2. Run `app.py` and visit the server in Google Chrome.
3. Click on the button on the webpage, and learn a little bit about Mars!
