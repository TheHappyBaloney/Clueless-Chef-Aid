import streamlit as st
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

CHEF_API_KEY = os.getenv("CHEF_API_KEY")
def get_gemini_response(user_prompt):
    response = chat.send_message(user_prompt, stream = True)
    response.resolve() 
    return response

st.set_page_config(page_title="Chef Baloney", page_icon="🍳", layout="wide")
st.markdown("<h1 style='text-align: center;'>Ask Chef Baloney</h1>", unsafe_allow_html=True)
st.write("\n")

# Side Bar
st.sidebar.title("Explore")
app_mode = st.sidebar.selectbox("Choose the app mode", ["Home", "About Clueless Chef's Aid", "About the Developer"])

# Main Page
if app_mode == "About Clueless Chef's Aid":
        st.title("About Clueless Chef's Aid")
        st.write("Clueless Chef's Aid is a recipe recommendation system that helps you find recipes based on the ingredients you have at home. Simply upload the ingredients you have and we will provide you with a list of recipes you can make.")
        st.write("The system uses a generative model to generate recipe names and steps based on the ingredients provided by the user. The generative model is trained on a large dataset of recipes and can generate realistic recipes that are easy to follow.")
        st.write("Clueless Chef's Aid is designed to help you make the most of the ingredients you have at home and discover new recipes that you can try out. Whether you are a beginner cook or an experienced chef, Clueless Chef's Aid can help you find new and exciting recipes to try out.")
        st.write("Get started with Clueless Chef's Aid today and discover the joy of cooking!")

if app_mode == "About the Developer":
        st.title("About the Developer 👋🏾")
        st.write("Clueless Chef's Aid is developed by [TheHappyBaloney](https://github.com/TheHappyBaloney). TheHappyBaloney is an AI enthusiast who loves to explore the world of Machine Learning and Generative AI and create innovative solutions using the latest AI technologies.")
        st.write("Thank you for using Clueless Chef's Aid and for supporting Baloney. We look forward to helping you discover new recipes and explore the world of cooking with our AI-powered solutions.")
        st.write("Happy cooking!")

if app_mode == "Home":
    st.header("Welcome to Clueless Chef's Aid!")
    st.write("Chef baloney is here to help you find recipes based on the ingredients you have at home. Simply upload the ingredients you have and we will provide you with a list of recipes you can make.")
    st.write("Let's get started!")
    st.write("Write down the ingredients you have at home and upload the list below.")
    
# Initialize chat_history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    st.write("1. Ingredients list can include any vegetables, fruits, meats, leftover dishes, condiments and spices that you have at home.")
    st.write("2. Please separate each ingredient with a comma.")
    st.write("3. If you do not have the whole vegetable but instead a component of it, that you would like to incorporate in. for e.g. if you only have the lemon peel of a whole lemon, you can write 'lemon peel' in the ingredient list.")
    st.write("4. Before incorporating any ingredient or dish, please make sure that it is safe to consume.")
    st.write("5. Please select any allergens that you are allergic to.")
    st.write("6. Please select any dietary restrictions that you may have.")
    st.write("7. Click on the 'Ask Chef Baloney' button to get the recipe.")
    st.write("8. Enjoy cooking!")

    # Ingredients
    ingredients = st.text_input("Ingredients", key="ingredients")
    # Split the user's input into words
    words = ingredients.split()
    # Join the words with commas
    ingredients = ', '.join(words)

    # Allergens
    allergens = st.multiselect("Allergens", ["Peanuts", "Tree Nuts", "Soy", "Dairy", "Eggs", "Fish", "Shellfish", "Wheat","Others","None"], key="allergens")
    if allergens == "Others":
        st.text_input("Others", height=100, key="others")
    allergens_str = ", ".join(allergens)
    
    # Dietary Restrictions
    dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten Free", "Keto", "Paleo", "Low Carb", "Low Fat", "Low Sodium", "Others", "None"], key="dietary_restrictions")
    if dietary_restrictions == "Others":
        st.text_input("Others", height=100, key="others")
    dietary_restrictions_str = ", ".join(dietary_restrictions)

    def get_recipe_name(ingredients, dietary_restrictions_str, allergens_str):
        prompt = f"""Based on the ingredients provided ({ingredients}), dietary restrictions({dietary_restrictions_str}) and allergens({allergens_str}), please generate a name for a recipe."""
        recipe_name_response = get_gemini_response(prompt)
        recipe_name = recipe_name_response.candidates[0].content.parts[0].text
        return recipe_name

    def get_recipe_steps(recipe_name):
        prompt = f"""Generate numbered recipe steps for the recipe "{recipe_name}"."""
        recipe_steps_response = get_gemini_response(prompt)
        recipe_steps = recipe_steps_response.candidates[0].content.parts[0].text
        return recipe_steps

    def format_output(recipe_name, recipe_steps):
        output = f"Here's a recipe for you to try out. The name of the recipe is {recipe_name}\n"
        output += f"Here are the steps to make the recipe:\n{recipe_steps}"
        return output

# Find Recipes
    if st.button("Ask Chef Baloney"):
       st.write("Finding Recipes...")
       st.session_state['chat_history'].append(("You", ingredients))
       st.subheader("Chef Baloney's Response")
       recipe_name = get_recipe_name(ingredients, dietary_restrictions_str, allergens_str)
       recipe_steps = get_recipe_steps(recipe_name)
       output = format_output(recipe_name, recipe_steps)
       st.write(output)
       st.session_state['chat_history'].append(("Chef Baloney", output))

    footer_placeholder = st.empty()

