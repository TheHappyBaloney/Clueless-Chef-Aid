from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai
import streamlit.components.v1
import config

API_KEY= config.GOOGLE_API_KEY
genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(user_prompt):
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

def get_recipe_name(ingredients):
    prompt = f"""Based on the ingredients provided ({ingredients}), please generate a name for a recipe."""
    recipe_name_response = get_gemini_response(prompt)
    recipe_name = recipe_name_response.candidates[0].content.parts[0].text
    return recipe_name

def get_recipe_steps(recipe_name):
    prompt = f"""Generate numbered recipe steps for the recipe "{recipe_name}"."""
    recipe_steps_response = get_gemini_response(prompt)
    recipe_steps = recipe_steps_response.candidates[0].content.parts[0].text
    return recipe_steps

def format_output(recipe_name, recipe_steps):
    output = f"Based on the ingredients you have, I have generated a recipe for you. The name of the recipe is {recipe_name}\n"
    output += f"Here are the steps to make the recipe:\n{recipe_steps}"
    return output

if submit and user_input:
    st.session_state['chat_history'].append(("You", user_input))
    st.subheader("Chef Baloney's Response")
    recipe_name = get_recipe_name(user_input)
    recipe_steps = get_recipe_steps(recipe_name)
    output = format_output(recipe_name, recipe_steps)
    st.write(output)
    st.session_state['chat_history'].append(("Chef Baloney", output))

footer_placeholder = st.empty()

st.markdown("<h1 style='font-size: 17px; text-align: center; color:  #cb202d;'> Pro Tip: In case you're too lazy to cook, order good food from  <a href='https://play.google.com/store/apps/details?id=com.application.zomato&hl=en_IN&gl=US' target='_blank'>Zomato</a>. </h1>  <h2 style='font-size: 25px; text-align: center; color:  #cb202d;'> But don't you dare order anything from Swiggy!!!! </h2> <h3 style='font-size: 17px; text-align: center; color:  #cb202d;'> They made @thehappybaloney sad by not commenting under their reel. </h3>", unsafe_allow_html=True)

footer_placeholder.markdown("""
    <div style="position: bottom; width: 100%; text-align: center;">
        <h1 style='font-size: 18px;'>This site is brought to you by thehappybaloney. If you have any queries, or suggestions on how this site can be made better feel free to reach out to me on Twitter or Github (@thehappybaloney).</h1>
    </div>
""", unsafe_allow_html=True)
