import requests
from bs4 import BeautifulSoup
from Finder_Base import BASE


class Eslite(BASE):
    def __init__(self):
        super(BASE).__init__()
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.home_url = "http://www.eslite.com"
        self.search_url = "http://www.eslite.com"
        self.data = {}

    def search(self, name=None, epsiode=None, ISBN=None, author=None, publish=None):
        self.data_clean(name, epsiode, ISBN, author, publish)
        self.make_url_complete("/Search_BW.aspx?query=")

        r = requests.get(self.search_url, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")

        results = []
        targets = soup.find(class_="box_list")

        if not targets:
            return False

        targets = targets.find_all("table")
        for target in targets:
            title = target.find(class_="name").find_all("a")[1]["title"]
            img_href = target.find("img")["src"]
            book_href = target.find(class_="name").find_all("a")[1]["href"]
            book_type = target.find(class_="summary").find_all("span")[3].text
            price = target.find(class_="summary").find_all(class_="price_sale")
            price = (price[0].text + price[2].text).replace(",", "").strip() if len(price) == 3 else price[1].text.strip()
            results.append([title, img_href, book_href, book_type, price])

        return results

    def top_hot(self):
        r = requests.get(self.home_url, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")

        book_name = [ele.text for ele in soup.select(".rankword a")]
        href = [ele["href"] for ele in soup.select(".rankword a")]
        return [list(ele) for ele in zip(book_name, href)]


if __name__ == "__main__":
    test = Eslite()
    '''
    results = test.search("sajdiojasvka41c5")
    if results:
        for result in results:
            for ele in result:
                print(ele)
            print("-"*20)
    else:
        print("Nothing")
    '''
    print(test.top_hot())