'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import data
import random
from fractions import Fraction

class recipe():
    ingredients = {}
    primary_method = []
    secondary_method=[]
    steps=[]
    def print_ingredients(self):
        for ele in self.ingredients.keys():
            print("Name: ", ele)
            print("Quantity: ", self.ingredients[ele]["quantity"])
            print("Unit: ", self.ingredients[ele]["unit"])
            print("Preparation: ", self.ingredients[ele]["prep"])
            print("Descriptions: ", self.ingredients[ele]["descriptions"])
            print("Additional Instruction: ", self.ingredients[ele]["additional"])
            print("\n")

        return

    def print_steps(self):
        counter=1
        for ele in self.steps:
            for e in ele.keys():
                print("Step ",counter,e,": ",ele[e])
            print("\n")
            counter+=1

    def print_methods(self):
        print("Primary Method: ",self.primary_method[0])
        print("Secondary Method: ", self.secondary_method[:min(len(self.secondary_method), 3)])


    def process_ingredients(self,ele):
        temp=ele.replace(",","")
        temp=temp.replace("¼",".25")
        temp=temp.replace("¾",".75")
        temp=temp.replace("½",".5")
        temp=temp.replace("⅓",".33")
        temp = temp.replace("- ", "")
        dic={}
        #ele.replace()
        prep_result=set(["into","to"])
        words=temp.split()
        quantity=0
        unit=""
        name=""
        additional=[]
        prep=[]
        descriptions=[]
        #print(words)
        e=0
        while e < len(words):
            if words[e][0]=="(":
                desc=words[e][1:]
                temp = temp.replace(words[e], "")
                temp = temp.replace("  ", " ")
                e+=1
                while e<len(words) and words[e][-1]!=")":
                    temp=temp.replace(words[e],"")
                    temp=temp.replace("  "," ")
                    desc+=" "+words[e]
                    e+=1
                temp = temp.replace(words[e], "")
                temp = temp.replace("  ", " ")
                desc+=words[e][:len(words[e])-1]
            e+=1
        update=temp.split()

        found=False
        if words[0][0] in set([".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
            quantity = float(words[0])
            unit = "Count"
            name = " ".join(update[1:])
            found=True
        for w in range(len(update)):
            if update[w] in data.Liquid_Measurements or update[w] in data.Solid_Measurements:
                if w>0 and not found:
                    try:
                        quantity=float(update[w-1])
                        unit=update[w]
                        name=" ".join(update[w+1:])
                        found=True
                    except:
                        found=False
                elif w>0:
                    try:
                        q=float(update[w-1])
                        unit=update[w]
                    except:
                        try:
                            q = float(Fraction(update[w - 1]))
                            add = str(q)+" "+update[w]
                            additional.append(add)
                            name=name.replace(update[w],"")
                            name=name.replace(update[w-1],"")
                            name=name.replace("  ","")
                        except:
                            continue
        if not found:
                quantity=0
                name=" ".join(update)
                unit="Based on Preference"
        print(name.split())
        split=name.split()
        for index in range(len(split)):
            if split[index] in data.prep:
                name=name.replace(split[index],"")
                name=name.replace("  "," ")
                if index+1<len(split) and split[index+1]in prep_result:
                    name=name.replace(split[index+1],"")
                    name=name.replace("  "," ")
                prep.append(split[index])

            for types in data.descriptors.keys():
                if split[index] in data.descriptors[types]:
                    name = name.replace(split[index], "")
                    name = name.replace("  ", " ")
                    descriptions.append(split[index])
        if name[0]==" ":
            name=name[1:]
        if name[len(name)-1]==" ":
            name=name[:len(name)-1]
        name=name.replace("for","")
        name=name.replace("  "," ")
        name = name.replace(" or", "")
        name = name.replace(" and","")
        name=name.replace(" as needed","")
        name=name.replace(" to taste","")
        dic["quantity"]=quantity
        dic["unit"]=unit
        dic["name"]=name.lower()
        dic["prep"]=prep
        dic["descriptions"]=descriptions
        dic["additional"]=additional

        return dic

    def process_methods_primary(self,step):
        counter=defaultdict(int)
        temp=step.lower()
        for ele in temp.split():
            if ele in data.Method_Primary:
                counter[ele]+=1
        return counter

    def process_methods_secondary(self,step):
        counter=defaultdict(int)
        temp=step.lower()
        for ele in temp.split():
            if ele in data.Method_Secondary:
                counter[ele]+=1
        return counter

    def process_steps(self,step):
        target=step.lower()
        steps=[]
        sentences=target.split(".")

        #print(sentences)
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
                if items in sentence and items not in dic["methods"]:
                    dic["methods"].append(items)

            dic["ingredients"]=[]
            for ele in self.ingredients:
                if ele in sentence and ele not in dic["ingredients"]:
                    dic["ingredients"].append(ele)
            if len(dic["ingredients"])>0 or len(dic["methods"])>0 or len(dic["tools"])>0 or len(dic["time"])>0:
                steps.append(dic)
        return steps

    def to_Vegetarian(self):
        replaced=[]
        replacement=[]
        for ele in self.ingredients.keys():
            meat=False
            for words in ele.split():
                if words in data.Non_Vegan["meat"]:
                    meat=True
                    break
            if meat:
                replaced.append(ele)
                find=random.sample(data.Vegan_Protein,1)
                while find[0] in replacement and len(replacement)<len(data.Vegan_Protein):
                    find=random.sample(data.Vegan_Protein,1)
                replacement.append(find[0])
        print(replaced,replacement)
        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = []
            for w in self.ingredients[replaced[ele]]["descriptions"]:
                if w not in data.descriptors["meat"]:
                    dic["descriptions"].append(w)

            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]]=dic

        for i in range(len(self.steps)):
            new_lis=[]
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis.append(replacement[replaced.index(ing)])
                else:
                    new_lis.append(ing)
            self.steps[i]["ingredients"]=new_lis


    def to_Non_Vegetarian(self):
        replaced=[]
        replacement=[]
        for ele in self.ingredients.keys():
            vege=False
            for words in ele.split():
                if words in data.Vegetable:
                    vege=True
                    break
            if vege:
                replaced.append(ele)
                find=random.sample(data.Non_Vegan["meat"],1)
                while find[0] in replacement and len(replacement)<len(data.Non_Vegan["meat"]):
                    find=random.sample(data.Non_Vegan["meat"],1)
                replacement.append(find[0])
        print(replaced,replacement)
        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = []
            for w in self.ingredients[replaced[ele]]["descriptions"]:
                if w not in data.descriptors["veggie"]:
                    dic["descriptions"].append(w)

            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]]=dic

        for i in range(len(self.steps)):
            new_lis = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis.append(replacement[replaced.index(ing)])
                else:
                    new_lis.append(ing)
            self.steps[i]["ingredients"] = new_lis


    def to_Healty(self):
        replaced = []
        replacement = []
        for ele in self.ingredients.keys():
            if ele in data.Make_Healthy["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Make_Healthy["ingredients"][ele])

        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]]=dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app=[]
            new_lis_tools=[]
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing


            for app in self.steps[i]["methods"]:
                if app in data.Make_Healthy["approach"]:
                    new_lis_app.append(data.Make_Healthy["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Make_Healthy["tools"]:
                    new_lis_tools.append(data.Make_Healthy["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools







    def __init__(self,dish):
        html = requests.get(dish)

        bs=BeautifulSoup(html.content, features="html.parser")

        res=bs.find_all("span",attrs={"class": "ingredients-item-name"})
        for ele in res:
            #print(ele.get_text())
            temp=self.process_ingredients(ele.get_text())
            self.ingredients[temp['name']]=temp
        print("Ingredients Parsing Finished")
        #Find Ingredients

        res = bs.find_all("li", attrs={"class": "subcontainer instructions-section-item"})
        pm=defaultdict(int)
        for ele in res:
            s=self.process_methods_primary(ele.get_text())
            for keys in s:
                pm[keys]+=s[keys]
        self.primary_method=[k for k in pm.keys()]
        self.primary_method.sort(key=lambda x: pm[x],reverse=True)
        #Find Primary Method


        sm=defaultdict(int)
        for ele in res:
            t=self.process_methods_secondary(ele.get_text())
            for keys in t:
                sm[keys]+=t[keys]
        self.secondary_method = [k for k in sm.keys()]
        self.secondary_method.sort(key=lambda x: sm[x], reverse=True)

        #Find Secondary Method

        for ele in res:
            #print(ingredients.keys())
            self.steps+=self.process_steps(ele.get_text())


if __name__ == '__main__':
    main()
