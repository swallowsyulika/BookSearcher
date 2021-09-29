import requests
from bs4 import BeautifulSoup
from Finder_Base import BASE


class Library(BASE):
    def __init__(self):
        super(BASE).__init__()
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.home_url = "https://lib1.nptu.edu.tw"
        self.search_url = "https://lib1.nptu.edu.tw"
        self.data = {}

    def search(self, name=None, epsiode=None, ISBN=None, author=None, publish=None):
        self.data_clean(name, epsiode, ISBN, author, publish)
        self.make_url_complete("/search*cht/?searchtype=Y&searcharg=")

        r = requests.get(self.search_url, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")

        if str(soup).find("無查獲的館藏")+1:
            return False

        results = []
        targets = soup.find_all(class_="briefCitRow")
        if targets:
            for target in targets:
                title = target.find(class_="briefcitTitle").text.strip()
                title = "Check this book name in website!" if title == None else title
                img_href = target.find("img")["src"]
                img_href = "https://static.findbook.tw/image/book/9789863474760/large" if str(img_href).find("rate_no") >= 0 else img_href
                book_href = self.home_url + target.find(class_="briefcitTitle").find("a")["href"].replace("*", "")
                book_type = None
                price = [ele.find_all("td") for ele in target.find_all(class_="bibItemsEntry")]
                for ele in price:
                    for i in range(len(ele)):
                        ele[i] = ele[i].text.strip()
                results.append([title, img_href, book_href, book_type, price])
        else:
            title = soup.find(id="bibDisplayLayout").find_all(class_="bibInfoData")[1].text.strip()
            title = "Check this book name in website!" if title == None else title
            img_href = soup.find(id="wind").find("img")["src"]
            img_href = "https://static.findbook.tw/image/book/9789863474760/large" if img_href == None else img_href
            book_href = self.search_url
            book_type = None
            price = [x.find_all("td") for x in soup.find_all(class_="bibItemsEntry")]
            for ele in price:
                for i in range(len(ele)):
                    ele[i] = ele[i].text.strip().replace("\xa0", "")
            results.append([title, img_href, book_href, book_type, price])
            
        return results


if __name__ == "__main__":
    test = Library()
    results = test.search("c++")
    if results:
        for result in results:
            for ele in result:
                print(ele)
            print("-"*20)
    else:
        print("無查獲的館藏")
