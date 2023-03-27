import streamlit as st 
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title = 'Fashionapp',page_icon='')

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.header("Welcome to our Fashion App 👕")

lottie_url = "https://assets3.lottiefiles.com/private_files/lf30_ecnepkno.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json)

sidebar  = st.sidebar


