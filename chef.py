import streamlit as st
import tensorflow as tf
import numpy as np
import os
import key
from dotenv import load_dotenv
load_dotenv()
from pred import model_prediction

CHEF_API_KEY = os.getenv("CHEF_API_KEY")

# Side Bar
st.sidebar.title("Explore")
app_mode = st.sidebar.selectbox("Choose the app mode", ["Home", "About Clueless Chef's Aid", "About the Developer"])

# Main Page
if app_mode == "Home":
    st.title("Clueless Chef's Aid")
    st.header("Welcome to Clueless Chef's Aid!")
    st.write("Chef baloney is here to help you find recipes based on the ingredients you have at home. Simply upload the ingredients you have and we will provide you with a list of recipes you can make.")
    st.write("Let's get started!")
    

    
    