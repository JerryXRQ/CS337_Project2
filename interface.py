'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
import parse_tools
import copy

def search(dish):

    search_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'
    target_url = search_url % (dish.replace(" ", "+"))
    html = requests.get(target_url)
    bs = BeautifulSoup(html.content, features="html.parser")
    return bs


def main():
    print("Welcome to Recipe Master!")
    dish = input("Please enter the url of the recipe: ")
    if dish=="quit":
        return

    original=parse_tools.recipe(dish)
    original.print_ingredients()
    original.print_steps()
    det=True
    while det:
        action=input("What action do you want to perform: ")
        if action=="quit":
            det=False
        elif action=="vegetarian":
            original.to_Vegetarian()
            original.print_ingredients()
            original.print_steps()
        elif action=="meat":
            original.to_Non_Vegetarian()
            original.print_ingredients()
            original.print_steps()
        elif action=="healthy":
            original.to_Healty()
            original.print_ingredients()
            original.print_steps()
        elif action=="unhealthy":
            original.to_Unhealthy()
            original.print_ingredients()
            original.print_steps()
        elif action=="double":
            original.scale(2.0)
            original.print_ingredients()
            original.print_steps()
        elif action=="half":
            original.scale(0.5)
            original.print_ingredients()
            original.print_steps()
        else:
            print("We do not understand this. Please try again.")
    return

if __name__ == '__main__':
    main()
