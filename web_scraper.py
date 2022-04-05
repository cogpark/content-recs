import requests
from bs4 import BeautifulSoup

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
        
        return title


if __name__ == "__main__":
    ws = WebScraper()
    x = ws.get_title('www.mass.gov/technology-careers-at-the-commonwealth-of-massachusetts')
    print(x)

