# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# Instead of scraping each row or data in table, scrape the entire table with Pandas' .read_html() function.
import pandas as pd


# Set your executable path via Splinter
# Then set up the URL 'https://redplanetscience.com/' for scraping
    #**executable_path is unpacking the dictionary we've stored the path in � think of it as unpacking a suitcase
    # headless=False means that all of the browser's actions will be displayed in a Chrome window so we can see them.
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
    # Search for elements with a specific combination of tag (div) and attribute (list_text).
    # Tell our browser to wait one second before searching for components
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Set up the HTML parser using BeautifulSoup
html = browser.html
news_bs = bs(html, 'html.parser')
# Assign slide_elem as the variable to look for the <div /> tag and its descendent (the other tags within the <div /> element)
    # This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further.
    # The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. 
    # CSS works from right to left, such as returning the last item on the list instead of the first.
    # Because of this, when using select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it.
slide_elem = news_bs.select_one('div.list_text')


# Chain .find onto our previously assigned variable, slide_elem and look for content title
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title` variable
    # When the .get_text() this method is chained onto .find(), only the text of the element is returned.
news_title = slide_elem.find('div', class_='content_title').get_text()
print("-------------1st ARTICLE---------")
print(news_title)

# Use the parent element to find the paragraph text
news_summary = slide_elem.find('div', class_="article_teaser_body").get_text()
print("-------------SUMMARY-------------")
print(news_summary)


# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# Find and click the full image button
    # Assign a  new variable to hold the scraping result
    # Use the browser finds to find an element by its tag
    # Use index chaining at the end of first block of code to stipulate taht we want our browser to click the 2nd button
full_image_elem = browser.find_by_tag("button")[1]
# Splinter will "click" the imagine to view its full size
full_image_elem.click() 


# Parse the resulting html with soup
html = browser.html
img_bs = bs(html, 'html.parser')


# Find the relative image url using BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
    # An img tag is nested within this HTML, so we've included it.
    # .get('src') pulls the link to the image.
img_url_rel = img_bs.find('img', class_='fancybox-image').get('src')
img_url_rel
# Basically we're saying, "This is where the image we want lives�use the link that's inside these tags."


# Use the base URL to create an absolute URL
    # img_url is the variable that holds our f string
    # the f-string is a type of string formatting used for print statements in Python.
    # {} The curly brackets hold a variable that will be inserted into the f-string when it's executed.
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# Create a new DataFrame from the HTML table.
    # The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML.
    # By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list.
# Assign columns to the new DataFrame for additional clarity.
# Use the .set_index() function, we're turning the Description column into the DataFrame's index
    # inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


df.to_html()


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# 2. Create a list to hold the images and titles.

# Set up the HTML parser using BeautifulSoup, which parses the HTML text and then stores it as an object.
html = browser.html
soup = bs(html, 'html.parser')

#Parse Products List in HTML in element item
hemispheres = soup.find_all('div', class_='item')

hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.
for which_hemisphere in hemispheres:
    # get title of hemisphere name and remove unnessary text
    full_title = which_hemisphere.h3.text
    title = full_title.replace(" Enhanced", "")
    
    # the base URL doesnt hold the absolute link to the JPEG, so parse html to link
    # add it to base url
    href_relative_link = which_hemisphere.find('a')['href']
    base_url = "https://marshemispheres.com/"
    image_link = base_url + href_relative_link
    
    #vist new sight adn click on link
    browser.visit(image_link)
    
    # use css elements to access link to jpeg
    element = browser.find_link_by_text('Sample').first
    img_url = element['href']
    
#     browser.visit(image_link)
#     html = browser.html
#     soup = soup(html, 'html.parser')
    
#     div_downloads = soup.find("div", class_="downloads")
#     image_url_breadcrumb = div_downloads.a["href"]
#     image_url = base_url + image_url_breadcrumb

    # create a dictionary and send it to list
    hemisphere_image_urls.append({"title": title, "img_url": img_url})
    
print(hemisphere_image_urls) 


browser.quit()
