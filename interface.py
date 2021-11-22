'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
import parse_tools
import copy
import re


def search(dish):

    search_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'
    target_url = search_url % (dish.replace(" ", "+"))
    html = requests.get(target_url)
    bs = BeautifulSoup(html.content, features="html.parser")
    return bs


def main():
    print("Welcome to Recipe Master!")
    urlin=True
    original=None
    while urlin:
        dish = input("Please enter the url of the recipe: ")
        if dish=="quit":
            return
        if not re.search('allrecipes.com', dish):
            print("Input should be a link from allrecipes.com. Please try again.")
            continue
        #try:
        original = parse_tools.recipe(dish)
            #original.print_ingredients()
            #original.print_steps()
        urlin=False
        #except:
        print("Something went wrong when retrieving information from the url.")
        if not urlin:
            print("We have successfully parsed the recipe. Please use option verbose to see more details.")
    det=True
    while det:
        all_actions = ['verbose',"methods",'vegetarian', 'vegan', "weight", 'meat', "kosher", 'healthy', 'unhealthy', 'double', 'half', 'gluten', 'chinese',"mexican", "cajun", 'indian', 'lactose','stir-fry','deep-fry','region']
        print("Available actions: ")
        print("Result Display: [verbose, methods, region]")
        print("Ingredients Requirements: [vegetarian, vegan, kosher, meat, gluten, lactose]")
        print("Health Related: [healthy, unhealthy]")
        print("Quantity Change: [double, half, weight]")
        print("Style Change: [chinese, mexican, cajun, indian]")
        print("Cooking Method Change: [stir-fry, deep-fry]")
        print('\n')
        action = input("What action do you want to perform: ")
        if action == "quit":
            det = False
        elif len(action)>4 and action[:4]=="http":
            original.initialize(action)
            #original.print_ingredients()
            #original.print_steps()
            print("reset successfully")
        elif action not in all_actions:
            print("We do not understand this. Please try again.")

        elif action=="verbose":
            original.print_ingredients()
            original.print_steps()

        elif action=="methods":
            original.print_methods()

        elif action == "vegetarian":
            if original.to_Vegetarian():
                print("If you want more details, please use the option verbose.")
                #original.print_ingredients()
                #original.print_steps()
        elif action == "weight":
            if original.weight():
                print("If you want more details, please use the option verbose.")
                #original.print_ingredients()
                #original.print_steps()
        elif action == "meat":
            if original.to_Non_Vegetarian():
                print("If you want more details, please use the option verbose.")
                #original.print_ingredients()
                #original.print_steps()
        elif action == "healthy":
            if original.to_Healty():
                print("If you want more details, please use the option verbose.")
                #original.print_ingredients()
                #original.print_steps()
        elif action == "unhealthy":
            if original.to_Unhealthy():
                print("If you want more details, please use the option verbose.")
                #original.print_ingredients()
                #original.print_steps()
        elif action == "double":
            original.scale(2.0)
            print("If you want see the modified recipe, please use the option verbose.")
            #original.print_ingredients()
            #original.print_steps()
        elif action == "half":
            original.scale(0.5)
            print("If you want see the modified recipe, please use the option verbose.")
            # original.print_ingredients()
            # original.print_steps()
        elif action == "gluten":
            if original.gluten_free():
                print("If you want more details, please use the option verbose.")
                #original.print_ingredients()
                #original.print_steps()
        elif action == "lactose":
            if original.lactose_free():
                print("If you want more details, please use the option verbose.")
                #original.print_ingredients()
                #original.print_steps()
        elif action == "chinese":
            if original.chinese():
                print("If you want more details, please use the option verbose.")
                # original.print_ingredients()
                # original.print_steps()
        elif action == "indian":
            if original.indian():
                print("If you want more details, please use the option verbose.")
                # original.print_ingredients()
                # original.print_steps()
        elif action == "kosher":
            if original.kosher():
                print("If you want more details, please use the option verbose.")
        elif action == "vegan":
            if original.to_Vegan():
                print("If you want more details, please use the option verbose.")
                # original.print_ingredients()
                # original.print_steps()
        elif action=="mexican":
            if original.mexico():
                print("If you want more details, please use the option verbose.")
        elif action=="cajun":
            if original.cajun():
                print("If you want more details, please use the option verbose.")
        elif action=="stir-fry":
            if original.to_stir_fry():
                print("If you want more details, please use the option verbose.")
        elif action=='deep-fry':
            if original.to_deep_fry():
                print("If you want more details, please use the option verbose.")
        elif action=="region":
            reg,ing=original.original_cuisine()
            if len(reg)>0:
                print("We found the following likely styles: ", reg)
                print("These decisions are based on the following ingredients: ", ing)
            else:
                print("We cannot find a good match for this recipe.")
            print('\n')
    return


if __name__ == '__main__':
    main()
