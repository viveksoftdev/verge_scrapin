#import By
from selenium.webdriver.common.by  import By

from webdriver_manager.chrome import ChromeDriverManager
#import webdriver
from selenium import webdriver
#importing options
from selenium.webdriver import ChromeOptions

#import service
from selenium.webdriver.chrome.service import Service

#import locators
from locators.xpath_locatorss import LOCATORS as xl

from selenium.common.exceptions import NoSuchElementException

from main_class.logger import verge_logger

#import os
import os
import pandas
import time
import re


class MAINSCRAPER:
    def __init__(self,url):
        self.service = Service(executable_path=ChromeDriverManager().install())
        self.options = ChromeOptions()
        self.options.add_experimental_option('detach',True)
        
        self.url = url
        self.driver = webdriver.Chrome(service=self.service,options=self.options)
        self.driver.get(self.url)
        self.pages = 0
      

    def get_main_headlines(self):
        main_news = []
        name_pattern = re.compile('([A-Z.\s]{3,})|([A-Z.\s]{3,} AND [A-Z.\s]+)')
        date_pattern = re.compile('[A-Z]{3,5} [0-9]{1,2}')
        news_pattern = re.compile('[a-zA-Z0-9\?.!"\'_@#$%&\s]{15,}')
        empty_dataframe = pandas.DataFrame()
     
        try:
            main_headlines = self.driver.find_elements(By.XPATH, xl.MAIN_HEADLINES)
            if self.pages == 0:
                accept_element = self.driver.find_element(By.XPATH,xl.ACCEPT_HANDLER).click()
    
            for main_headline  in main_headlines:
                if main_headline:
                    name = name_pattern.search(main_headline.text)
                    date = date_pattern.findall(main_headline.text) 
                    news =[]
                    for item in main_headline.text.split('\n'):
                        news_pattern.search(item)
                        news.append(item)
                
                    
                    
                    data = main_headline.text
                    # print(print(data))
                    if name and date:
                        data_dict = {'Author':name.group().split('\n')[1],
                             'Date':date[0],
                             'News':', '.join(news)}       
                        main_news.append(data_dict)
                        
                    self.pages = 1    
            try:
                csv_ = pandas.read_csv(os.path.abspath('file_name.csv'))
                if csv_:
                    news_dataframe = pandas.DataFrame(main_news)

                    csv_.concat(news_dataframe)
                    csv_ = csv_.drop_duplicates(inplace=True)
                    csv_.to_csv('file_name.csv')

            except Exception as error:
                verge_logger.error(error)
                news_dataframe = pandas.DataFrame(main_news)
                print(news_dataframe)
                news_dataframe.to_csv('file_name.csv')
                
        except NoSuchElementException as error:
            verge_logger.error(error)
        except Exception as error:
            verge_logger.error(error)
            
    # def get_small_headlines(self):        
    #     try:
    #         if self.pages==0:
    #             accept_element = self.driver.find_element(By.XPATH,xl.ACCEPT_HANDLER).click()
    #             self.pages = 1

    #         small_headlines = self.driver.find_elements(By.XPATH,xl.SMALL_HEADLINES)
    #         for small_headline  in small_headlines:
    #             print(small_headline.text.split('\n'))
    #     except NoSuchElementException as error:
    #         print(error)

    #     except Exception as error:
    #         print(error)

 
if __name__ == "__main__":
    verge_scraper = MAINSCRAPER('https://www.theverge.com/')

    verge_scraper.get_main_headlines()

    # verge_scraper.get_small_headlines()
