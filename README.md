# recipe-project-master
Recipe Parser
Group 2
Members: Jerry Xu, Daniel Wang, Jonathan Katz
Github Link: https://github.com/JerryXRQ/CS337_Project2

The packages necessary to run our code are included in the file final_requirements.txt.

To run our code, please use the command python interface.py. The program will ask the user for a link to the recipe. If the input does not come from allrecipes.com, it will ask the user for a valid address. If errors occur during parsing, they will be captured, and a message will be displayed. Otherwise, it will display the available options.

There are six types of options. To display the parsed information, the user can use "verbose" or "methods". Verbose will display the internal representations used by the parser, including steps and ingredients. Methods will display the primary and secondary approaches used in this recipe.

We also support several ingredient requirements. Vegetarian removes the meat ingredients in a recipe. Vegan further removes dairy and egg from the recipe. The kosher option will transform the recipe based on kosher requirements. The meat command will replace some vegetables with meat. The gluten option replaces ingredients containing gluten, and the lactose option makes the recipe lactose-free.

We have two health-related transformations: healthy and unhealthy. Both of them replace ingredients and cooking methods based on the requirements. They will also update the tools required based on the transformations.

For quantity change, we have implemented three options. The user can use the double instruction to double the recipe or use half to reduce it. We also try to adjust the cooking time accordingly. There is also a unit conversion option called weight. It will convert all units to grams.

For style change, we implemented Chinese, Mexican, and Cajun styles. They will transform both ingredients and cooking approaches.

Additionally, the code can also change the primary cooking method to stir-fry, deep-fry, and steam. Additional ingredients and tools will be added if necessary.

We also added an undo function. It allows us to undo the previous transformation and restore the recipe. However, do note that if multiple transformations have been performed on the recipe, the only way to restore the original recipe is to enter the URL again.

If the code does not detect ingredients or methods that can be replaced, it will display a message saying that the transformation cannot be performed.

To quit the program, simply use the command quit. To parse a new recipe, just enter the URL, and the code will reset automatically.

# Extra Tasks Completed

We have finished the following extra tasks.

Ingredients: We included descriptor and preparation.

Methods: We added secondary cooking methods finder.

Transformation: For the style of cuisine, we have included Chinese, Indian, Mexican, Cajun, and French. For quantity change, we implemented double, half, and weight conversion. For cooking method change, we added switch to stir-fry, deep-fry, and steam. These transformations include necessary ingredient and step additions. For special food constraints, we included kosher, gluten-free, and lactose-free.

Control Features: We allowed the user to restore the previous recipe with command "undo".

Testing Tools: We built a tester that checks all program features on a selected set of recipes.

Additional Tasks in Assignment Description: 14 (Excluding one required style change)
Additional Tasks we Propose: 4



# Work Distribution


### Jerry Xu:
Designed the parsing framework.
Added extra tasks Mexican transform, scaling, gluten-free, lactose-free, and all three cooking method change functions.
Wrote the README file.



### Daniel Wang:
Added Chinese, Indian, and French transformations.
Added undo feature.


### Jonathan Katz:
Added kosher, Cajun, and unit conversion functions.
Designed the tester.
