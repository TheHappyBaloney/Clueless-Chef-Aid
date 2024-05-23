import streamlit as st
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
    response.resolve()  
    return response

st.set_page_config(page_title="Clueless Chef's Aid", page_icon="🍳", layout="wide")
st.markdown("<h1 style='text-align: center;'>Ask Chef Baloney</h1>", unsafe_allow_html=True)
st.write("\n")

st.sidebar.title("Dasboard")
app_mode =  st.sidebar.selectbox("Choose the app mode", ["Home", "About Clueless Chef's Aid", "About the Developer"])

# Main Page 
if app_mode == "Home":
    st.markdown("<h2 style='text-align: center;'>Welcome to Clueless Chef's Aid</h2>", unsafe_allow_html=True)
    img_path = "/workspaces/Clueless-Chef-Aid/Banner2-removebg-preview.png"
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image(img_path)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Ask Chef Baloney anything about cooking and recipes</h3>", unsafe_allow_html=True)
    st.write("\n")
    user_input = st.text_input("Ask Chef Baloney", "")
    if st.button("Ask"):
        response = get_gemini_response(user_input)
        st.write(response.text)