import requests
from bs4 import BeautifulSoup


class Books:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.url = "https://search.books.com.tw/search/query/key/"

    def search(self, name):
        r = requests.get(self.url+name.strip(),  headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")
        target = soup.find(class_="item")   
        anchor = target.find(attrs={"rel": "mid_name"})
        price = target.find(class_="price")
        price = price.find_all("strong")
        string = ""
        for ele in price:
            string += ele.text + " "
        return [anchor["title"], string.strip(), "https:" + anchor["href"]]


class Eslite:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.url = "http://www.eslite.com/Search_BW.aspx?query="

    def search(self, name):
        if " " in name:
            name = name.strip().replace(" ", "+")
        r = requests.get(self.url+name, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")
        target = soup.find(class_="box_list")
        target = target.find("table")
        anchor = target.find(class_="name")
        anchor = anchor.find_all("a")[1]
        price = target.find_all(class_="price_sale")
        string = ""
        if len(price) > 2:
            string += price[0].text.replace(",", "").strip() + " " + price[2].text
        else:
            string += price[1].text
        return [anchor["title"], string, anchor["href"]]


class Kingstone:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.url = "https://www.kingstone.com.tw/new/search/search?q="

    def search(self, name):
        if " " in name:
            name = name.strip().replace(" ", "+")
        r = requests.get(self.url+name, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")
        target = soup.find(class_="division1 clearfix")
        anchor = target.find(class_="pdnamebox").a
        price = target.find(class_="buymixbox")
        price = price.find_all("span")
        string = ""
        if len(price) > 2:
            string += price[0].text + price[1].text
        else:
            string += price[0].text
        return [anchor.text, string, "https://www.kingstone.com.tw" + anchor["href"]]


if __name__ == "__main__":
    want = "狼與辛香料 20"

    B = Books()
    result = B.search(want)
    print("博客來\n" + result[0] + "\n" + result[1] + "\n" + result[2])

    E = Eslite()
    result = E.search(want)
    print("誠品\n" + result[0] + "\n" + result[1] + "\n" + result[2])

    K = Kingstone()
    result = K.search(want)
    print("金石堂\n" + result[0] + "\n" + result[1] + "\n" + result[2])


