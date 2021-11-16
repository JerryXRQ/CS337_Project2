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
        try:
            original = parse_tools.recipe(dish)
            #original.print_ingredients()
            #original.print_steps()
            urlin=False
        except:
            print("Something went wrong when retrieving information from the url.")
        if urlin:
            print("We have successfully parsed the recipe. Please use option verbose to see more details.")
    det=True
    while det:
        all_actions = ['verbose',"methods",'vegetarian', 'vegan', 'meat', 'healthy', 'unhealthy', 'double', 'half', 'gluten free', 'chinese','lactose']
        print(f"Available actions: {all_actions}")
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
        elif action == "gluten free":
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
        elif action == "vegan":
            if original.to_Vegan():
                print("If you want more details, please use the option verbose.")
                # original.print_ingredients()
                # original.print_steps()
    return


if __name__ == '__main__':
    main()
