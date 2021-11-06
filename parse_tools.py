'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import data

def process_ingredients(ele):
    temp=ele.replace(",","")
    temp=temp.replace("¼",".25")
    temp=temp.replace("¾",".75")
    temp=temp.replace("½",".5")
    temp = temp.replace("- ", "")
    #ele.replace()
    words=temp.split()
    quantity=0
    unit=""
    name=""
    additional=[]
    #print(words)
    for e in words:
        if e[0]=="(":
            temp=temp.replace(e,"")
            temp=temp.replace("  "," ")
            additional.append(e)
        elif e[-1]==")":
            temp = temp.replace(e, "")
            temp = temp.replace("  ", " ")
            additional.append(e)
    update=temp.split()

    found=False
    for w in range(len(update)):
        if update[w] in data.Liquid_Measurements or update[w] in data.Solid_Measurements:
            if w>0:
                quantity=float(update[w-1])
            unit=update[w]
            name=" ".join(update[w+1:])
            found=True
            break
    if not found:
        quantity=float(words[0])
        unit="Count"
        name=update[1:]
    print("Quantity: ",quantity)
    print("Unit: ",unit)
    print("Name: ",name)

def key_info(dish):
    dic=defaultdict(str)
    html = requests.get(dish)
    print(html)
    bs=BeautifulSoup(html.content, features="html.parser")
    i = 1
    ingredients=[]
    description={}
    quantity=[]
    det=True
    res=bs.find_all("span",attrs={"class": "ingredients-item-name"})
    for ele in res:
        process_ingredients(ele.get_text())
        print(ele.get_text())
    return dic

if __name__ == '__main__':
    main()
