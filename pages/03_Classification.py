import streamlit as st 
from streamlit_option_menu import option_menu
from utils.imgs import load_image
from utils.model import CustomFashionClassifier
from utils.dataset import dataset

st.header("Classification")

options = option_menu('',["Image", 'Camera'], icons=['image', 'camera'],orientation="horizontal")

if options == "Image":
    uploaded_img = st.file_uploader("Upload an image")
    if uploaded_img:
        img = load_image(uploaded_img)
        st.image(img)

        # Classifiy image here
        with st.spinner("Processing...."):
            cloth_type = CustomFashionClassifier(dataset=dataset).classify(img)
        st.success(f'This cloth is: {cloth_type}')

if options == "Camera":
    pic = st.camera_input("Take a camera pic")
    if pic:
        st.image(pic)
        with st.spinner("Processing...."):
            cloth_type = CustomFashionClassifier(dataset=dataset).classify(load_image(pic))
        st.success(f'This cloth is: {cloth_type}')

