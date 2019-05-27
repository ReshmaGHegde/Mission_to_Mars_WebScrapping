#from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from pprint import pprint

def scrape_all():
    
    browser = Browser('chrome', executable_path='./Chrome_Safe/chromedriver.exe',headless=True)
    news_title, news_paragraph = mars_news(browser)
    featured_image_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts(browser)
    hemispheres = hemisphere(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image_url,
        "mars_weather" : mars_weather,
        "facts" : facts,
        "hemispheres" : hemispheres
        
    }
    browser.quit()
    return data

def mars_news(browser):

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    try:
        latest_article = news_soup.find('li',{'class','slide'})
        #time.sleep(2)
        news_title = latest_article.find("div", {'class','content_title'}).get_text()
        news_paragraph = latest_article.find("div", {'class','article_teaser_body'}).get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph

def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    
    browser.is_element_present_by_id('full_image', wait_time=0.5)
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    browser.is_element_present_by_text("more info", wait_time=0.5)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()
    #time.sleep(2)
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    image = img_soup.select_one('figure.lede a img')
    try:
        partial_image = image.get("src")
    except AttributeError:
        return None
    featured_image_url = f'https://www.jpl.nasa.gov{partial_image}'
    print(featured_image_url)
    return featured_image_url

def twitter_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')
    mars_weather = tweet_soup.select_one('p.TweetTextSize').get_text()
    print(mars_weather)
    return mars_weather

def mars_facts(browser):
#    try:
#        df = pd.read_html("http://space-facts.com/mars/")[0]
#    except BaseException:
#        return None

#    df.columns = ["description", "value"]
#    df.set_index("description", inplace=True)

    # Add some bootstrap styling to <table>
#    return df.to_html(classes="table table-striped")
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    table_soup = BeautifulSoup(html, 'html.parser')
    table_stat = table_soup.find("table", {'class','tablepress tablepress-id-mars'})

    #pprint(table_stat)

    eq_diameter = table_stat.find("tr", {'class','row-1 odd'}).get_text()
    eq_diameter = eq_diameter.strip()
    eq_diameter.split(":")
    #print(len(eq_diameter))
    #print(eq_diameter[0:19])
    #print(eq_diameter[20:28])


    po_diameter = table_stat.find("tr", {'class','row-2 even'}).get_text()
    po_diameter = po_diameter.strip()
    po_diameter.split(":")
    #print(len(po_diameter))
    #print(po_diameter[0:14])
    #print(po_diameter[15:23])


    mass = table_stat.find("tr", {'class','row-3 odd'}).get_text()
    mass = mass.strip()
    mass.split(":")
    #print(len(mass))
    #print(mass[0:4])
    #print(mass[5:34])


    moons = table_stat.find("tr", {'class','row-4 even'}).get_text()
    moons = moons.strip()
    moons.split(":")
    #print(len(moons))
    #print(moons[0:5])
    #print(moons[6:25])


    orbit_dist = table_stat.find("tr", {'class','row-5 odd'}).get_text()
    orbit_dist = orbit_dist.strip()
    orbit_dist.split(":")
    #print(len(orbit_dist))
    #print(orbit_dist[0:14])
    #print(orbit_dist[15:39])


    orbit_period = table_stat.find("tr", {'class','row-6 even'}).get_text()
    orbit_period = orbit_period.strip()
    orbit_period.split(":")
    #print(len(orbit_period))
    #print(orbit_period[0:12])
    #print(orbit_period[13:33])


    surface_temp = table_stat.find("tr", {'class','row-7 odd'}).get_text()
    surface_temp = surface_temp.strip()
    surface_temp.split(":")
    #print(len(surface_temp))
    #print(surface_temp[0:19])
    #print(surface_temp[20:34]) 

    first_record = table_stat.find("tr", {'class','row-8 even'}).get_text()
    first_record = first_record.strip()
    first_record.split(":")
    #print(len(first_record))
    #print(first_record[0:12])
    #print(first_record[13:31])
    key= first_record[0:12]


    recorded_by = table_stat.find("tr", {'class','row-9 odd'}).get_text()
    recorded_by = recorded_by.strip()
    recorded_by.split(":")
    #print(len(recorded_by))
    #print(recorded_by[0:11])
    #print(recorded_by[12:31])
    key9 = recorded_by[0:11]
    value9 = recorded_by[12:31]

    table_stat_dist = {f'{eq_diameter[0:19]}':eq_diameter[20:28],f'{po_diameter[0:14]}':po_diameter[15:23],f'{mass[0:4]}':mass[5:34],f'{moons[0:5]}':moons[6:25],f'{orbit_dist[0:14]}':orbit_dist[15:39],f'{orbit_period[0:12]}':orbit_period[13:33],f'{surface_temp[0:19]}':surface_temp[20:34],f'{first_record[0:12]}':first_record[13:31],f'{recorded_by[0:11]}':recorded_by[12:31]}
    table_stat_dist_df = pd.DataFrame(table_stat_dist.items(),columns=['Parameters','Values'])
    #table_stat_dist_df
    return table_stat_dist_df.to_html(classes="table table-striped")

def hemisphere(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        hempisphere_items = hemi_soup.find_all("div", {'class','item'})
    except AttributeError:
        None, None

    img_urls_list = []

    for h in hempisphere_items:
        hemispheres_dict = {}
        title_p = h.find('h3').get_text()
        #title_list.append(title_p)
        ar = h.find('img',class_='thumb')
        href_link  = 'https://astrogeology.usgs.gov' + ar['src']
        #img_list.append(href_link)
        hemispheres_dict['title']= title_p
        hemispheres_dict['img_url'] = href_link
        img_urls_list.append(hemispheres_dict)   
        #pprint(img_urls_list)
    return img_urls_list

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())