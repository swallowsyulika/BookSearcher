import requests
from bs4 import BeautifulSoup
from Finder_Base import BASE


class Books(BASE):
    def __init__(self):
        super(BASE).__init__()
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.home_url = "https://www.books.com.tw"
        self.search_url = "https://search.books.com.tw"
        self.data = {}

    def search(self, name=None, epsiode=None, ISBN=None, author=None, publish=None):
        self.data_clean(name, epsiode, ISBN, author, publish)
        self.make_url_complete("/search/query/key/")

        r = requests.get(self.search_url, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")

        results = []
        targets = soup.find_all(class_="item")

        if not targets:
            return False
        
        for target in targets:
            title = target.find(attrs={"rel": "mid_name"})["title"]
            img_href = str(target.find("img"))
            img_href = img_href[img_href.find("http"):img_href.find("jpg")+3]
            book_href = "https:" + target.find(attrs={"rel": "mid_name"})["href"]
            book_type = target.find(class_="cat").text
            price = " ".join(tuple([x.text.replace(" ", "") for x in target.find_all("strong")]))
            results.append([title, img_href, book_href, book_type, price])

        return results

    def top_hot(self):
        r = requests.get(self.home_url, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")

        book_name = [ele.text for ele in soup.select("#M201101_19797__P000800010025 p")]
        href = [ele.parent["href"] for ele in soup.select("#M201101_19797__P000800010025 .ban")]
        return [list(x) for x in zip(book_name, href)]


if __name__ == "__main__":
    test = Books()
    '''
    results = test.search("gjgiorjg34894j38jg839jg03428g2")
    if results:
        print(results)
        for result in results:
            for ele in result:
                print(ele)
            print("-"*20)
    else:
        print("Nothing")
    '''
    print(test.top_hot())

    
