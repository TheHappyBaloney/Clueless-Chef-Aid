from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(user_prompt):
    response = chat.send_message(user_prompt, stream = True)
    return response

st.set_page_config(page_title="Chef Baloney", page_icon="🍳", layout="wide")
st.markdown("<h1 style='text-align: center;'>Ask Chef Baloney</h1>", unsafe_allow_html=True)
st.write("\n")
st.markdown("<h1 style='font-size: 25px; color: orange;'> Chef Baloney is here to help you with your cooking queries. Ask away!</h1>", unsafe_allow_html=True)
st.write(" We can generate recipes across 100+ cuisines for you based on the ingridients, utensils and appliances you mention below.")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("You: ", key="input")

# Split the user's input into words
words = user_input.split()

# Join the words with commas
user_input = ', '.join(words)
submit = st.button("Ask Chef Baloney")

user_prompt = f"Based on the ingredients mentioned by user{user_input}, combine all ingreients and generate recipe of one simple dish across various cuisines, provided the ingredients available with the user apart from the ones that they have mentioned are salt, sugar and water. The only appliances the user got is a gas stove and microwave and the only utensils user got are spoon, fork, knife, plate and mug. Present the response in the following format : Name of the dish, Preparation time, Ingredients, Steps to prepare the dish. Avoid adding any ingredients not mentioned in the prompt."


if submit and user_input:
    st.session_state['chat_history'].append(f"You: {user_prompt}")
    
    response = get_gemini_response(user_input)
    
    st.session_state['chat_history'].append(f"Chef Baloney: {response}")
    st.subheader("Chef Baloney's Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Chef Baloney", chunk.text))

