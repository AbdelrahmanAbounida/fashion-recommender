import streamlit as st 
from streamlit_option_menu import option_menu 
from utils.imgs import load_image
from utils.model import CustomFashionClassifier, CustomFashionRecommender
from utils.dataset import dataset

options = option_menu('',["Image", 'Camera', 'Text'], icons=['image', 'camera', 'card-text'],orientation="horizontal")

if options == "Image":
    gender = st.selectbox(
                'Choose the gender',
                ('Male', 'Female'))
    uploaded_img = st.file_uploader("Upload an image")
    if st.button('Submit'):
        if uploaded_img:
            img = load_image(uploaded_img)
            if not gender:
                st.error("Gender shouldn't be none")
            else:
                st.image(img)
                with st.spinner("Processing...."):
                    cloth_type = CustomFashionClassifier(dataset=dataset).classify(img)
                    recommendations = CustomFashionRecommender().recommend(cloth_type, gender)

                # print(recommendations.replace('\n','').split(','))
                st.write(cloth_type)
                st.write(gender)
                recommendations = recommendations.replace('\n','').split(',')
                if '[' in recommendations:
                    recommendations = recommendations.split('[')[1]
                if ']' in recommendations:
                    recommendations = recommendations.split(']')[0]

                st.json(recommendations[0:-2])


if options == "Camera":
    gender = st.selectbox(
                'Choose the gender',
                ('Male', 'Female'))
    pic = st.camera_input("Take a camera pic")
    if st.button('Submit'):
        if pic:
            if not gender:
                st.error("Gender shouldn't be none")
            else:
                st.image(pic)
                with st.spinner("Processing...."):
                    cloth_type = CustomFashionClassifier(dataset=dataset).classify(load_image(pic))
                recommendations = CustomFashionRecommender().recommend(cloth_type, gender)
                st.write(cloth_type)
                st.write(gender)
                recommendations = recommendations.replace('\n','').split(',')
                # if '[' in recommendations:
                #     recommendations = recommendations.split('[')[1]
                # if ']' in recommendations:
                #     recommendations = recommendations.split(']')[0]

                st.json(recommendations[0:-2])

if options == "Text":
    text = st.text_input("Enter a cloth type")
    gender = st.selectbox(
                'Choose the gender',
                ('Male', 'Female'))
    
    if st.button('Submit'):
        if text:
            if not gender:
                st.error("Gender shoudn't be none")
            with st.spinner("Processing...."):
                recommendations = CustomFashionRecommender().recommend(cloth_type=text, gender=gender)
            st.write(text)
            recommendations = recommendations.replace('\n','').split(',')
            st.json(recommendations)