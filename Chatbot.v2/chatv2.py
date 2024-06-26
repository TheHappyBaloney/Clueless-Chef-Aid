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

st.sidebar.title("Dasboard")
app_mode =  st.sidebar.selectbox("Choose the app mode", ["Home", "About Clueless Chef's Aid", "About the Developer"])

# Main Page 
if app_mode == "Home":
    st.markdown("<h1 style='text-align: center;'>Clueless Chef's Aid</h1>", unsafe_allow_html=True)
    st.write("\n")
    img_path = "/workspaces/Clueless-Chef-Aid/Banner.jpg"
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image(img_path, use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Ask Chef Baloney anything about cooking and recipes</h3>", unsafe_allow_html=True)
    st.write("\n")
    user_input = st.text_input("Ask Chef Baloney", "")
    if st.button("Ask"):
        response = get_gemini_response(user_input)
        st.write(response.text)


# About Clueless Chef's Aid
if app_mode == "About Clueless Chef's Aid":
    st.markdown("<h1 style='text-align: center;'> What is Clueless Chef's Aid? </h1>", unsafe_allow_html=True)
    st.write("\n")
    st.markdown("<h1 style=' text-align: left; font-size: 25px; color: orange;'> Clueless Chef's Aid is a zero-waste recipe generator. It's for those who have few things left at home, but many dreams of eating gourmet. Chef Baloney is here to help you with your cooking queries across 100+ cusines.</h1>", unsafe_allow_html=True)
    st.link_button("Go To Home :house: ","app_mode = 'Home'", help=None, type="primary", disabled=False, use_container_width=False )
    st.write("\n")
    st.subheader("How to use Clueless Chef's Aid?")
    st.subheader("About the Dataset")
    st.text("The dataset used to train the model is a collection of images of fruits and vegetables. The dataset contains 100+ classes of fruits and vegetables. Check it out!")
    st.link_button(":orange[Explore The Dataset] :computer:", "https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition", help=None, type="secondary", disabled=False, use_container_width=False)

# About Clueless Chef's Aid
if app_mode == "About the Developer":
    st.markdown("<h1 style='text-align: center;'> Who created Clueless Chef's Aid? </h1>", unsafe_allow_html=True)
    st.write("\n")
