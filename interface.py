'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
import parse_tools

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
    transformed=[]
    while det:
        action=input("What action do you want to perform: ")
        if action=="quit":
            det=False
        elif action=="vegetarian":
            modified=parse_tools.recipe(dish)
            modified.to_Vegetarian()
            modified.print_ingredients()
            modified.print_steps()

    return

if __name__ == '__main__':
    main()
