class BASE:
    def __init__(self):
       pass

    def data_clean(self, name, epsiode, ISBN, author, publish):
        if name is not None:
            self.data["Name"] = name
        if epsiode is not None:
            self.data["Epsiode"] = epsiode
        if ISBN is not None:
            self.data["ISBN"] = ISBN
        if author is not None:
            self.data["Author"] = author
        if publish is not None:
            self.data["Publish"] = publish

    def make_url_complete(self, back):
        self.search_url += back
        keys = self.data.keys()
        if "ISBN" in keys:
            self.search_url += self.data["ISBN"]
            return
        if "Name" in keys:
            self.search_url += self.data["Name"] + " "
        if "Epsiode" in keys:
            self.search_url += self.data["Epsiode"] + " "
        if "Author" in keys:
            self.search_url += self.data["Author"] + " "
        if "publish" in keys:
            self.search_url += self.data["publish"] + " "

    def search(self, name=None, epsiode=None, ISBN=None, author=None, publish=None):
        pass

    def top_hot(self):
        pass