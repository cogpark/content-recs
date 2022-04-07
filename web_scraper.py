import requests
from bs4 import BeautifulSoup
import re

class WebScraper:
    
    def __init__(self):
        return
    
    def get_title(self, url, parser='html.parser'):
        # people might not enter the protocol
        if url[0:3] == 'www':
            url = 'https://' + url

        webdata = requests.get(url)
        # soupText = BeautifulSoup(webdata.text, parser)
        soupContent = BeautifulSoup(webdata.content, parser)

        # Get title attribute and strip out tags
        title = str(soupContent.find("title").text)

        # All Mass.gov title tags have | Mass.gov on them
        if "|" in title:
            title = title.split('|')[0].strip()

      
        # Get node ID so we can get around the problem of duplicate titles. First, find the dataLayer object
        script_text = str(soupContent.find("script", text=re.compile("entityIdentifier")))
        print(script_text)

        

        node_id = re.search('"entityIdentifier":"[0-9]*"', script_text)[0]
        node_id = ''.join([i for i in node_id if i in ['1','2','3','4','5','6','7','8','9','0']])        
        return title, int(node_id)


if __name__ == "__main__":
    ws = WebScraper()
    x = ws.get_title('www.mass.gov/technology-careers-at-the-commonwealth-of-massachusetts')
    print(x)

