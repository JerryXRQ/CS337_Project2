'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
from collections import defaultdict



def key_info(dish):
    dic=defaultdict(str)
    html = requests.get(dish)
    print(html)
    bs=BeautifulSoup(html.content, features="html.parser")
    i = 1
    ingredients=[]
    det=True
    res=bs.find_all("span",attrs={"class": "ingredients-item-name"})
    for ele in res:
        print(ele.get_text())
    return dic

if __name__ == '__main__':
    main()
