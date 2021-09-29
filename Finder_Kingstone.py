import requests
from bs4 import BeautifulSoup
from Finder_Base import BASE


class Kingstone(BASE):
    def __init__(self):
        super(BASE).__init__()
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.home_url = "https://www.kingstone.com.tw"
        self.search_url = "https://www.kingstone.com.tw"
        self.data = {}

    def search(self, name=None, epsiode=None, ISBN=None, author=None, publish=None):
        self.data_clean(name, epsiode, ISBN, author, publish)
        self.make_url_complete("/new/search/search?q=")

        r = requests.get(self.search_url, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")

        results = []
        targets = soup.find_all(class_="division1 clearfix")

        if not targets:
            return False
        
        for target in targets:
            title = target.find("img")["title"]
            img_href = target.find("img")["src"]
            img_href = self.home_url + img_href if str(img_href).find("restricted") >= 0 else "https://cdn.kingstone.com.tw/images/noimage.gif" if str(img_href).find("english") >= 0 else img_href
            book_href = self.home_url + target.find("a")["href"]
            book_type = target.find(class_="book").text
            price = target.find(class_="buymixbox").find_all("span")
            price = price[0].text + " " + price[1].text if len(price) > 2 else price[0].text
            results.append([title, img_href, book_href, book_type, price])

        return results

    def top_hot(self):
        r = requests.get(self.home_url, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")

        book_name = [ele.text for ele in soup.select("#home_ranking_hour .height2 a")[:5]]
        href = [self.home_url + ele["href"] for ele in soup.select("#home_ranking_hour .height2 a")[:5]]
        return [list(ele) for ele in zip(book_name, href)]

if __name__ == "__main__":
    test = Kingstone()
    '''
    results = test.search("jaiofdajsfoajsfip564")
    if results:
        for result in results:
            for ele in result:
                print(ele)
            print("-"*20)
    else:
        print("Nothing")
    '''
    print(test.top_hot())