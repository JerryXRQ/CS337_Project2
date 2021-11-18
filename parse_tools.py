'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import data
import random
from fractions import Fraction
from math import floor

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
        temp=temp.replace(" ¼",".25")
        temp = temp.replace("¼", ".25")
        temp=temp.replace(" ¾",".75")
        temp = temp.replace("¾", ".75")
        temp=temp.replace(" ½",".5")
        temp = temp.replace("½", ".5")
        temp=temp.replace(" ⅓",".33")
        temp = temp.replace("⅓", ".33")
        temp = temp.replace("- ", "")
        temp=temp.replace("-inch"," inch")
        temp=temp.replace(" or more","")
        temp = temp.replace(" or to taste", "")
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
                if ")" in words[e]:
                    desc.replace(")","")
                    temp = temp.replace(words[e], "")
                    temp = temp.replace("  ", " ")
                    break
                else:
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
        if update[0][0] in set([".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]) and update[1] not in data.Liquid_Measurements and update[1] not in data.Solid_Measurements:
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
                        try:
                            q = float(Fraction(update[w - 1]))
                            unit=update[w]
                            name=" ".join(update[w+1:])
                            found=True
                        except:
                            found=False
                elif w>0:
                    try:

                        q=float(update[w-1])
                        unit=update[w]
                        name = name.replace(update[w], "")
                        name = name.replace(update[w - 1], "")
                        name = name.replace("  ", "")
                        additional.append(str(q)+" "+unit)
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
        if len(name)==0:
            return None
        if name[0]==" ":
            name=name[1:]
        if len(name)==0:
            return None
        if name[len(name)-1]==" ":
            name=name[:len(name)-1]
        name=name.replace("for","")
        name=name.replace("  "," ")
        name = name.replace(" or", "")
        name = name.replace(" and","")
        name = name.replace("and ", "")
        name=name.replace(" as needed","")
        name = name.replace("as needed", "")
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
        for k in data.Tools_to_Method:
            if k in temp:
                counter[data.Tools_to_Method[k]]+=1
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
            sentence=sentence.replace(" 1/2"," .5")
            sentence=sentence.replace("1/2", ".5")
            sentence=sentence.replace(" 1/4"," .25")
            sentence=sentence.replace("1/4", ".25")
            sentence = sentence.replace(" 3/4", " .75")
            sentence = sentence.replace("3/4", ".75")
            sentence=sentence.replace(",","")
            sentence=sentence.replace(";","")
            dic={}
            temp={}
            for st in ["   step 1   ","   step 2   ","   step 3   ","   step 4   ","   step 5   ","   step 6   ","   step 7   ","   step 8   ","   step 9   ","   step 10   "]:
                sentence=sentence.replace(st,"")
            dic["raw"] = sentence
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
                elif ele[-1]=="s" and ele[:len(ele)-1] in sentence and ele[:len(ele)-1] not in dic["ingredients"]:
                    dic["ingredients"].append(ele)
                else:
                    for kw in ele.split():
                        if kw in sentence and kw not in dic["ingredients"]:
                            dic["ingredients"].append(kw)
                        elif kw[-1]=="s" and kw[:len(kw)-1] in sentence:
                            dic["ingredients"].append(kw)
            for ele in data.Meat_Parts:
                if ele in sentence and ele not in dic["ingredients"] and ele not in " ".join(dic["ingredients"]):
                    dic["ingredients"].append(ele)
            if len(dic["ingredients"])>0 or len(dic["methods"])>0 or len(dic["tools"])>0 or len(dic["time"])>0:
                steps.append(dic)
        return steps

    def process_methods_bs(self,res):
        pm = defaultdict(int)
        for ele in res:
            s = self.process_methods_primary(ele.get_text())
            for keys in s:
                pm[keys] += s[keys]
        self.primary_method = [k for k in pm.keys()]
        self.primary_method.sort(key=lambda x: pm[x], reverse=True)
        # Find Primary Method

        sm = defaultdict(int)
        for ele in res:
            t = self.process_methods_secondary(ele.get_text())
            for keys in t:
                sm[keys] += t[keys]
        self.secondary_method = [k for k in sm.keys()]
        self.secondary_method.sort(key=lambda x: sm[x], reverse=True)
        #Find Secondary Method

    def process_methods(self,res):
        pm = defaultdict(int)
        for ele in res:
            s = self.process_methods_primary(ele["raw"])
            for keys in s:
                pm[keys] += s[keys]
        #print(pm)
        self.primary_method = [k for k in pm.keys()]
        self.primary_method.sort(key=lambda x: pm[x], reverse=True)
        # Find Primary Method

        sm = defaultdict(int)
        for ele in res:
            t = self.process_methods_secondary(ele["raw"])
            for keys in t:
                sm[keys] += t[keys]
        self.secondary_method = [k for k in sm.keys()]
        self.secondary_method.sort(key=lambda x: sm[x], reverse=True)
        #Find Secondary Method


    def to_Vegetarian(self):
        replaced=[]
        replacement=[]
        match={}
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
                for sw in ele.split():
                    match[sw]=find[0]
        if len(replaced) == 0:
            print("Sorry, we fail to find a replacement. This recipe is already vegetarian.")
            return True
        else:
            print("We found the following items that need to be replaced: ", replaced)
            print("We replaced them with: ", replacement)
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
            new_lis = []
            for ele in replaced:
                if ele in self.steps[i]["raw"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, replacement[replaced.index(ele)])
                elif ele[-1] == "s" and ele[:len(ele) - 1] in self.steps[i]["raw"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele[:len(ele) - 1],
                                                                        replacement[replaced.index(ele)])

            sp = self.steps[i]["raw"].split()
            for ele in sp:
                if ele in data.descriptors["meat"] or ele in data.descriptors["dairy"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, "")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace("  ", "")
                elif ele in data.Meat_Parts:
                    chos = random.choice(replacement)
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, chos)
                elif ele in match:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, match[ele])

            sentence = self.steps[i]["raw"]
            for ele in self.ingredients:
                if ele in sentence and ele not in new_lis:
                    new_lis.append(ele)
                elif ele[-1] == "s" and ele[:len(ele) - 1] in sentence and ele[:len(ele) - 1] not in new_lis:
                    new_lis.append(ele)
                else:
                    for kw in ele.split():
                        if kw in sentence and kw not in new_lis:
                            new_lis.append(kw)
                        elif kw[-1] == "s" and kw[:len(kw) - 1] in sentence and kw not in new_lis:
                            new_lis.append(kw)
            self.steps[i]["ingredients"] = new_lis

        return True

    def to_Vegan(self):
        replaced = []
        replacement = []
        replaced_m=[]
        replacement_m=[]
        match={}
        for ele in self.ingredients.keys():
            meat = False
            for words in ele.split():
                if words in data.Non_Vegan["meat"]:
                    meat = True
                    break
            if meat:
                replaced.append(ele)
                replaced_m.append(ele)
                find = random.sample(data.Vegan_Protein, 1)
                while find[0] in replacement and len(replacement) < len(data.Vegan_Protein):
                    find = random.sample(data.Vegan_Protein, 1)
                replacement.append(find[0])
                replacement_m.append(find[0])
                for sw in ele.split():
                    match[sw]=find[0]
        for ele in self.ingredients.keys():
            for words in ele.split():
                if words in data.Vegan:
                    replaced.append(ele)
                    replacement.append(data.Vegan[words])
        if len(replaced) == 0:
            print("Sorry, we fail to find a replacement. This recipe is already vegan.")
            return True
        else:
            print("We found the following items that need to be replaced: ", replaced)
            print("We replaced them with: ", replacement)
        for ele in range(len(replaced)):
            dic={}
            dic["name"]=replacement[ele]
            dic["quantity"]=self.ingredients[replaced[ele]]["quantity"]
            dic["unit"]=self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = []
            for w in self.ingredients[replaced[ele]]["descriptions"]:
                if w not in data.descriptors["meat"] and w not in data.descriptors["dairy"]:
                    dic["descriptions"].append(w)

            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]]=dic


        for i in range(len(self.steps)):
            new_lis=[]
            for ele in replaced:
                if ele in self.steps[i]["raw"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, replacement[replaced.index(ele)])
                elif ele[-1]=="s" and ele[:len(ele)-1] in self.steps[i]["raw"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele[:len(ele)-1], replacement[replaced.index(ele)])

            sp = self.steps[i]["raw"].split()
            for ele in sp:
                if ele in data.descriptors["meat"] or ele in data.descriptors["dairy"]:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, "")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace("  ", " ")
                elif ele in data.Meat_Parts:
                    chos = random.choice(replacement_m)
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, chos)
                elif ele in match:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ele, match[ele])

            sentence=self.steps[i]["raw"]
            for ele in self.ingredients:
                if ele in sentence and ele not in new_lis:
                    new_lis.append(ele)
                elif ele[-1] == "s" and ele[:len(ele) - 1] in sentence and ele[:len(ele) - 1] not in new_lis:
                    new_lis.append(ele)
                else:
                    for kw in ele.split():
                        if kw in sentence and kw not in new_lis:
                            new_lis.append(kw)
                        elif kw[-1] == "s" and kw[:len(kw) - 1] in sentence:
                            new_lis.append(kw)
            self.steps[i]["ingredients"]=new_lis


        return True


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
        if len(replaced)==0:
            print("Sorry, we fail to find a replacement. This recipe is already non-vegetarian.")
            return False
        else:
            print("We found the following items that need to be replaced: ",replaced)
            print("We replaced them with: ",replacement)

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
            sp=self.steps[i]["raw"].split()
            for ele in sp:
                if ele in replaced:
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(ele,replacement[replaced.index(ele)])
                elif ele in data.descriptors["veggie"]:
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(ele,"")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace("  ", "")


            self.steps[i]["ingredients"] = new_lis
        return True

    def to_Healty(self):
        replaced = []
        replacement = []
        det=False
        present=defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Make_Healthy["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Make_Healthy["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1],replacement[-1]])
                det=True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Make_Healthy["approach"]:
                    present["Method Change: "].append([app, data.Make_Healthy["approach"][app]])
                    det=True
            for app in self.steps[i]["tools"]:
                if app in data.Make_Healthy["tools"]:
                    present["Tool Change: "].append([app, data.Make_Healthy["tools"][app]])
                    det=True
        if not det:
            print("Sorry, we cannot find any transformations that can make this recipe healthier")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys,present[keys])

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
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing


            for app in self.steps[i]["methods"]:
                if app in data.Make_Healthy["approach"]:
                    new_lis_app.append(data.Make_Healthy["approach"][app])
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(app,data.Make_Healthy["approach"][app])
                else:
                    new_lis_app.append(app)

            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Make_Healthy["tools"]:
                    new_lis_tools.append(data.Make_Healthy["tools"][app])
                    self.steps[i]["raw"]=self.steps[i]["raw"].replace(app, data.Make_Healthy["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True

    def to_Unhealthy(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Make_Unhealthy["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Make_Unhealthy["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Make_Unhealthy["approach"]:
                    present["Method Change: "].append([app, data.Make_Unhealthy["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.Make_Unhealthy["tools"]:
                    present["Tool Change: "].append([app, data.Make_Unhealthy["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations that can make this recipe more unhealthy")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

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
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing


            for app in self.steps[i]["methods"]:
                if app in data.Make_Unhealthy["approach"]:
                    new_lis_app.append(data.Make_Unhealthy["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Make_Unhealthy["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Make_Unhealthy["tools"]:
                    new_lis_tools.append(data.Make_Unhealthy["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Make_Unhealthy["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True


    def scale(self,ratio):
        for ele in self.ingredients.keys():
            self.ingredients[ele]["quantity"]*=ratio

        for ele in range(len(self.steps)):
            if len(self.steps[ele]["time"])==2:
                num=self.steps[ele]["time"]["quantity"]
                num*=ratio**0.5
                num=floor(num)
                self.steps[ele]["time"]["quantity"]=num

            s=self.steps[ele]["raw"].split()
            #print(s)
            change_pos=[]
            for pos in range(len(s)):
                if len(self.steps[ele]["time"])>0 and s[pos] in self.steps[ele]["time"]["unit"]:
                    #print(s,ele)
                    try:
                        change_pos.append([pos-1,floor(float(s[pos-1])*ratio**0.5)])
                    except:
                        continue
                elif s[pos] in data.Liquid_Measurements or s[pos] in data.Solid_Measurements:
                    try:
                        change_pos.append([pos - 1, float(s[pos - 1]) * ratio])
                    except:
                        continue
            for pair in change_pos:
                s[pair[0]]=str(pair[1])
            self.steps[ele]["raw"]=" ".join(s)


    def gluten_free(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Gluten_Free:
                replaced.append(ele)
                replacement.append(data.Gluten_Free[ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True

        if not det:
            print("Sorry, we cannot find any transformation. This recipe is already gluten free")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing
        return True


    def chinese(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Chinese["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Chinese["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Chinese["approach"]:
                    present["Method Change: "].append([app, data.Chinese["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.Chinese["tools"]:
                    present["Tool Change: "].append([app, data.Chinese["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations. This particular recipe could not be made in Chinese style.")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app = []
            new_lis_tools = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing

            for app in self.steps[i]["methods"]:
                if app in data.Chinese["approach"]:
                    new_lis_app.append(data.Chinese["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Chinese["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Chinese["tools"]:
                    new_lis_tools.append(data.Chinese["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Chinese["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True

    def mexico(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        for ele in self.ingredients.keys():
            if ele in data.Mexican["ingredients"]:
                replaced.append(ele)
                replacement.append(data.Mexican["ingredients"][ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True
        for i in range(len(self.steps)):
            for app in self.steps[i]["methods"]:
                if app in data.Mexican["approach"]:
                    present["Method Change: "].append([app, data.Mexican["approach"][app]])
                    det = True
            for app in self.steps[i]["tools"]:
                if app in data.Mexican["tools"]:
                    present["Tool Change: "].append([app, data.Mexican["tools"][app]])
                    det = True
        if not det:
            print("Sorry, we cannot find any transformations. This particular recipe could not be made in Chinese style.")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = self.ingredients[replaced[ele]]["descriptions"]
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            new_lis_app = []
            new_lis_tools = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])
                else:
                    new_lis_ing.append(ing)
            self.steps[i]["ingredients"] = new_lis_ing

            for app in self.steps[i]["methods"]:
                if app in data.Mexican["approach"]:
                    new_lis_app.append(data.Mexican["approach"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Mexican["approach"][app])
                else:
                    new_lis_app.append(app)
            self.steps[i]["methods"] = new_lis_app

            for app in self.steps[i]["tools"]:
                if app in data.Mexican["tools"]:
                    new_lis_tools.append(data.Mexican["tools"][app])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(app, data.Mexican["tools"][app])
                else:
                    new_lis_tools.append(app)
            self.steps[i]["tools"] = new_lis_tools
        self.process_methods(self.steps)
        return True

    def lactose_free(self):
        replaced = []
        replacement = []
        det = False
        present = defaultdict(list)
        des_rep=set()

        for ele in self.ingredients.keys():
            if ele in data.Lactose_Free:
                replaced.append(ele)
                replacement.append(data.Lactose_Free[ele])
                present["Ingredient Change: "].append([replaced[-1], replacement[-1]])
                det = True

        if not det:
            print("Sorry, we cannot find any transformation. This recipe is already lactose free")
            return False
        else:
            print("We found the following substitutions: ")
            for keys in present:
                print(keys, present[keys])

        for ele in range(len(replaced)):
            dic = {}
            dic["name"] = replacement[ele]
            dic["quantity"] = self.ingredients[replaced[ele]]["quantity"]
            dic["unit"] = self.ingredients[replaced[ele]]["unit"]
            dic["prep"] = self.ingredients[replaced[ele]]["prep"]
            dic["descriptions"] = []
            for w in self.ingredients[replaced[ele]]["descriptions"]:
                if w not in data.descriptors["dairy"]:
                    dic["descriptions"].append(w)
                else:
                    des_rep.add(w)
            dic["additional"] = self.ingredients[replaced[ele]]["additional"]
            self.ingredients.pop(replaced[ele])
            self.ingredients[replacement[ele]] = dic

        for i in range(len(self.steps)):
            new_lis_ing = []
            for ing in self.steps[i]["ingredients"]:
                if ing in replaced:
                    new_lis_ing.append(replacement[replaced.index(ing)])
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(ing, replacement[replaced.index(ing)])

                else:
                    new_lis_ing.append(ing)
            spl=self.steps[i]["raw"].split()
            for words in spl:
                if words in des_rep:
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace(words,"")
                    self.steps[i]["raw"] = self.steps[i]["raw"].replace("  ", " ")
            self.steps[i]["ingredients"] = new_lis_ing
        return True

    def initialize(self,url):
        self.ingredients = {}
        self.primary_method = []
        self.secondary_method = []
        self.steps = []
        self.__init__(url)

    def __init__(self,dish):
        html = requests.get(dish)

        bs=BeautifulSoup(html.content, features="html.parser")

        res=bs.find_all("span",attrs={"class": "ingredients-item-name"})
        for ele in res:
            #print(ele.get_text())
            s=ele.get_text().split()
            separate=-1
            for i in range(len(s)):
                if s[i]=="and" and i>0 and s[i-1] not in data.prep:
                    separate=i
            if separate==-1:
                temp=self.process_ingredients(ele.get_text())
                self.ingredients[temp['name']]=temp
            else:
                temp = self.process_ingredients(" ".join(s[:separate]))
                if temp:
                    self.ingredients[temp['name']] = temp
                temp = self.process_ingredients(" ".join(s[separate+1:]))
                if temp and len(temp['name'])>3:
                    self.ingredients[temp['name']] = temp
        print("Ingredients Parsing Finished")
        #Find Ingredients

        res = bs.find_all("li", attrs={"class": "subcontainer instructions-section-item"})

        self.process_methods_bs(res)
        #Find Secondary Method

        for ele in res:
            #print(ingredients.keys())
            self.steps+=self.process_steps(ele.get_text())


