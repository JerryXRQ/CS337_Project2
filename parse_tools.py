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
    temp=temp.replace("⅓",".33")
    temp = temp.replace("- ", "")
    dic={}
    #ele.replace()
    words=temp.split()
    quantity=0
    unit=""
    name=""
    additional=[]
    prep=[]
    descriptions=[]
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
        if words[0][0] in set([".","0","1","2","3","4","5","6","7","8","9"]):
            quantity=float(words[0])
            unit="Count"
            name=" ".join(update[1:])
        else:
            quantity=0
            name=" ".join(update)
            unit="Based on Preference"
    for elements in name.split():
        if elements in data.prep:
            name=name.replace(elements,"")
            name=name.replace("  "," ")
            prep.append(elements)

        for types in data.descriptors:
            if elements in data.descriptors[types]:
                name = name.replace(elements, "")
                name = name.replace("  ", " ")
                descriptions.append(elements)
    if name[0]==" ":
        name=name[1:]
    if name[len(name)-1]==" ":
        name=name[:len(name)-1]
    dic["quantity"]=quantity
    dic["unit"]=unit
    dic["name"]=name.lower()
    dic["prep"]=prep
    dic["descriptions"]=descriptions
    dic["additional"]=additional
    print("Quantity: ",quantity)
    print("Unit: ",unit)
    print("Name: ",name.lower())
    print("Preparation: ",prep)
    print("Descriptions: ",descriptions)
    print("Additional Instruction: ",additional)
    print("\n")
    return dic

def process_methods_primary(step):
    counter=defaultdict(int)
    temp=step.lower()
    for ele in temp.split():
        if ele in data.Method_Primary:
            counter[ele]+=1
    return counter

def process_methods_secondary(step):
    counter=defaultdict(int)
    temp=step.lower()
    for ele in temp.split():
        if ele in data.Method_Secondary:
            counter[ele]+=1
    return counter

def process_steps(step,ingredients):
    target=step.lower()
    steps=[]
    sentences=target.split(".")

    print(sentences)
    for sentence in sentences:
        dic={}
        temp={}
        lis=sentence.split()
        for ele in range(len(lis)):
            if lis[ele] in data.Time_Units:
                temp["unit"]=lis[ele]
                try:
                    temp["quantity"]=float(lis[ele-1])
                except:
                    temp["quantity"]=1
        dic["time"]=temp
        #Update Time in the step

        dic["tools"]=[]
        for items in data.Tools:
            if items in sentence:
                dic["tools"].append(items)
        #Update Tools used

        dic["methods"]=[]
        for items in data.Method_Primary:
            if items in sentence:
                dic["methods"].append(items)

        for items in data.Method_Secondary:
            if items in sentence:
                dic["methods"].append(items)

        dic["ingredients"]=[]
        for ele in ingredients:
            if ele in sentence:
                dic["ingredients"].append(ele)
        if len(dic["ingredients"])>0 or len(dic["methods"])>0 or len(dic["tools"])>0 or len(dic["time"])>0:
            steps.append(dic)
            print(dic)
    return steps

def key_info(dish):
    html = requests.get(dish)

    bs=BeautifulSoup(html.content, features="html.parser")
    ingredients= {}
    res=bs.find_all("span",attrs={"class": "ingredients-item-name"})
    for ele in res:
        print(ele.get_text())
        temp=process_ingredients(ele.get_text())
        ingredients[temp['name']]=temp
    print("Ingredients Parsing Finished")
    #Find Ingredients

    res = bs.find_all("li", attrs={"class": "subcontainer instructions-section-item"})
    pm=defaultdict(int)
    for ele in res:
        s=process_methods_primary(ele.get_text())
        for keys in s:
            pm[keys]+=s[keys]
    lis=[k for k in pm.keys()]
    lis.sort(key=lambda x: pm[x],reverse=True)
    print("Primary Method: ",lis[0])
    #Find Primary Method


    sm=defaultdict(int)
    for ele in res:
        t=process_methods_secondary(ele.get_text())
        for keys in t:
            sm[keys]+=t[keys]
    lis2 = [k for k in sm.keys()]
    lis2.sort(key=lambda x: sm[x], reverse=True)
    print("Secondary Method: ", lis2[:min(len(lis2),3)])
    #Find Secondary Method

    for ele in res:
        #print(ingredients.keys())
        process_steps(ele.get_text(),set(ingredients.keys()))


if __name__ == '__main__':
    main()
