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
st.header(" Chef Baloney ")
st.title(" Ask Chef Baloney ")
st.write(" Chef Baloney is here to help you with your cooking queries. Ask away! ")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("You: ", key="input")
submit = st.button("Ask Chef Baloney")

user_prompt = f"Based on the ingredients mentioned by user{user_input}, generate simple recipes, provided the ingredients available with the user apart from the ones that they have mentioned are salt, sugar and water, the only appliances the user got is a gas stove and microwave and the only utensils user got are spoon, fork, knife, plate and mug."

if submit and user_input:
    st.session_state['chat_history'].append(f"You: {user_prompt}")
    response = get_gemini_response(user_input)
    st.session_state['chat_history'].append(f"Chef Baloney: {response}")
    st.subheader("Chef Baloney's Response")
    for chunk in response.split("\n"):
        st.write(chunk.text)
        st.session_state['chat_history'].append(f"Chef Baloney: {chunk.text}")
        st.subheader("The Chat History is")
    
        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")
        