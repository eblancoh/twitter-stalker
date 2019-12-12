import requests
import time
import datetime
import json
import random
from engine import TweetsAnalysis
from bs4 import BeautifulSoup

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

class Recomendations:

    def get_user_agent(self):
        user_agent = random.choice(user_agent_list)
        return user_agent


    def expansion_search(self):
        url = 'https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html'

        results = dict()

        params = {
            'User-Agent' : self.get_user_agent()
        }

        r = requests.get(url, params = params)

        if r.status_code == 200:
            content = r.content
            soup = BeautifulSoup(content, 'lxml')
            table = soup.find('table',{'id':'analisis_tecnico'})
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            

    def marketwatch_search(self):
        url = 'https://www.marketwatch.com/investing/stock/tef/analystestimates?countrycode=es'

        results = dict()

        params = {
            'User-Agent' : self.get_user_agent()
        }

        r = requests.get(url, params = params)

        if r.status_code == 200:
            content = r.content
            soup = BeautifulSoup(content, 'lxml')
            table = soup.find('table',{'class':'ratings'})
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            data = []

            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])

            for d in data:
                results[d[0]] = d[1]

            results['Recomendacion'] = 'SELL'
            max_value = -1
            opiniones = 0
            contador = 5

            for key in results:
                  if contador > 0:
                        if int(results[key]) > max_value:   
                            results['Recomendacion'] = key
                            max_value = int(results[key])
                        contador = contador - 1
                        opiniones = opiniones + int(results[key])

            results['Fiabilidad'] = "{0:.2f}".format(round(max_value/opiniones,4) * 100)

            return results


def main():
    r = Recomendations()
    results = dict()

    dt = datetime.datetime.today()
    ts = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)

    results['TS'] = ts

    #results['Expansion'] = {}
    results['MarketWatch'] = r.marketwatch_search()
    #print(results)
    TweetsAnalysis().db_complete(results,'recomendations')

if __name__ == "__main__":
    main()
