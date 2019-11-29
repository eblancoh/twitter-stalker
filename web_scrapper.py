from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
import time
import datetime
import json
from engine import TweetsAnalysis

class WebScrapper:

    def __init__(self):
        pass

    def expansion_search(self):

        try:    
            driver = webdriver.Chrome('/usr/local/bin/chromedriver')

            driver.get("https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html")

            results = dict()
            
            dt = datetime.datetime.today()
            ts = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)

            results['TS'] = ts

            pestanias = driver.find_element_by_id("pestanas_modulo_valores_analisis_superior")
            
            items = pestanias.find_elements_by_tag_name("li")

            for item in items:
                if item.text == "Análisis Téc.":
                    driver.execute_script("arguments[0].click();", item)

            time.sleep(5)
            anal_tec = driver.find_element_by_id("analisis_tecnico")
            body = anal_tec.find_elements_by_tag_name("tbody")
            valores = body[0].find_elements_by_tag_name("tr")

            for item in valores:
                if item.text.find("TELEFÓNICA") != -1:
                    div = item.text.split(" ")
                    results['Recomendacion'] = div[1]


            driver.close()
            return results

        except WebDriverException:
            return {}

    def marketwatch_search(self):
        try:
            driver = webdriver.Chrome('/usr/local/bin/chromedriver')

            driver.get("https://www.marketwatch.com/investing/stock/tef/analystestimates?countrycode=es")

            results = dict()
            
            dt = datetime.datetime.today()
            ts = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
            results['TS'] = ts

            ratings = driver.find_element_by_class_name("ratings")
            body = ratings.find_elements_by_tag_name("tbody")
            valores = body[0].find_elements_by_tag_name("tr")

            for item in valores:
                cond = item.find_element_by_class_name("first")
                num = item.find_element_by_class_name("current") 
                results[cond.text] = num.text

            results['Recomendacion'] = 'SELL'
            contador = len(results) - 3
            max_value = -1
            opiniones = 0

            for key in results:
                if key != 'TS':
                    if contador > 0:
                        if int(results[key]) > max_value:   
                            results['Recomendacion'] = key
                            max_value = int(results[key])
                        contador = contador - 1
                        opiniones = opiniones + int(results[key])

            results['Fiabilidad'] = "{0:.2f}".format(round(max_value/opiniones,4) * 100)

            driver.close()
            return results

        except WebDriverException:
            return {}

def main():
    ws = WebScrapper()
    data = dict()

    data['Expansion'] = ws.expansion_search()
    data['MarketWatch'] = ws.marketwatch_search()

    TweetsAnalysis().db_complete(data,"recomendations")




if __name__ == "__main__":
    main()
