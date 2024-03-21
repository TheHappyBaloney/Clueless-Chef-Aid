from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
import streamlit.components.v1

API_KEY= os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(user_prompt):
    chat = genai.Chat()
    response = chat.send_message(user_prompt, stream = True)
    response.resolve()  # Ensure the response has completed its iteration
    return response

st.set_page_config(page_title="Chef Baloney", page_icon="🍳", layout="wide")
st.markdown("<h1 style='text-align: center;'>Ask Chef Baloney</h1>", unsafe_allow_html=True)
st.write("\n")

st.markdown("<h1 style='font-size: 25px; color: orange;'> Chef Baloney is here to help you with your cooking queries. Ask away!</h1>", unsafe_allow_html=True)
st.write(" We can generate recipes across 100+ cuisines for you based on the ingridients you mention below.")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Enter the list of ingredients you have: ", key="input")

# Split the user's input into words
words = user_input.split()

# Join the words with commas
user_input = ', '.join(words)
submit = st.button("Ask Chef Baloney")

def name_recipe(ingridents):   

    name_prompt = """ You are a chef who can improvise a recipe even when not all the ingredients needed are there. 
    A user is wondering what to cook based on the few ingredients they have at home. 
    Based on the list of ingridents, generate the name of a name of a recipe. """
    
    rec_name = get_gemini_response(name_prompt)
    
    return rec_name

def recipe_steps(rec_name):

    recipe_prompt = """ You are a chef who can improvise a recipe even when not all the ingredients needed are there. 
    Can you generate numbered receipe steps for the recipe [recipe_name]?"""
    
    rec_steps = get_gemini_response(recipe_prompt)
    
    return rec_steps

def output_recipe(rec_name, rec_steps):
    st.write(f"Based on the ingridents you have, I have generated a recipe for you. The name of the recipe is {rec_name}")
    st.write(f"Here are the steps to make the recipe: {rec_steps}")

name_recipe = name_recipe(user_input)
recipe_steps = recipe_steps(name_recipe)

if submit and user_input:
    st.session_state['chat_history'].append(("You", user_input))
    st.subheader("Chef Baloney's Response")
    for chunk in chat.send_message(user_input, stream=True):
        print(output_recipe(name_recipe, recipe_steps))
        
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Chef Baloney", chunk.text))

st.markdown("<h1 style='font-size: 17px; text-align: center; color:  #cb202d;'> Pro Tip: In case you're too lazy to cook, order good food from  <a href='https://play.google.com/store/apps/details?id=com.application.zomato&hl=en_IN&gl=US' target='_blank'>Zomato</a>. </h1>  <h2 style='font-size: 25px; text-align: center; color:  #cb202d;'> But don't you dare order anything from Swiggy!!!! </h2> <h3 style='font-size: 17px; text-align: center; color:  #cb202d;'> They made @thehappybaloney sad by not commenting under their reel. </h3>", unsafe_allow_html=True)

footer_placeholder = st.empty()
footer_placeholder.markdown("""
    <div style="position: bottom; width: 100%; text-align: center;">
        <h1 style='font-size: 18px;'>This site is brought to you by thehappybaloney. It's a work-in progress. If you have any queries, or suggestions on how this site can be made better feel free to reach out to me on Twitter or Github (@thehappybaloney).</h1>
    </div>
""", unsafe_allow_html=True)
