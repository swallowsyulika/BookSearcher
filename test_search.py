from Finder_Books import Books
from Finder_Eslite import Eslite
from Finder_Kingstone import Kingstone
from Finder_Library import Library


want = input("What book are you look for : ")
B = Books()
E = Eslite()
K = Kingstone()
L = Library()


results = B.search(want)
for result in results:
    for ele in result:
        print(ele)
    print("-" * 20)
print("*"*40)

results = E.search(want)
for result in results:
    for ele in result:
        print(ele)
    print("-" * 20)
print("*"*40)

results = K.search(want)
for result in results:
    for ele in result:
        print(ele)
    print("-" * 20)
print("*"*40)

results = L.search(want)
for result in results:
    for ele in result:
        print(ele)
    print("-" * 20)
print("*"*40)