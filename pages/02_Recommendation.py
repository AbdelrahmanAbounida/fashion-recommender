import streamlit as st 
from streamlit_option_menu import option_menu 
from utils.imgs import load_image
from utils.model import CustomFashionClassifier, CustomFashionRecommender
from utils.dataset import dataset

options = option_menu('',["Image", 'Camera', 'Text'], icons=['image', 'camera', 'card-text'],orientation="horizontal")
openai_key = st.text_input("Write your openaikey")

if options == "Image":
    gender = st.selectbox(
                'Choose the gender',
                ('Male', 'Female'))
    uploaded_img = st.file_uploader("Upload an image")
    if st.button('Submit'):

        if not openai_key:
            st.error("Please Enter your openaikey")
        else:
            if uploaded_img:
                img = load_image(uploaded_img)
                if not gender:
                    st.error("Gender shouldn't be none")
                else:
                    st.image(img)
                    with st.spinner("Processing...."):
                        cloth_type = CustomFashionClassifier(dataset=dataset).classify(img)

                        try:
                            recommendations = CustomFashionRecommender(openai_key=openai_key).recommend(cloth_type, gender)
                        except:
                            st.error("Please Check your openai key")
                            recommendations =""

                    # print(recommendations.replace('\n','').split(','))
                    st.write(cloth_type)
                    st.write(gender)
                    recommendations = recommendations.replace('\n','').split(',')
                    if '[' in recommendations:
                        recommendations = recommendations.split('[')[1]
                    if ']' in recommendations:
                        recommendations = recommendations.split(']')[0]

                    st.json(recommendations[0:-2])
            else:
                st.error("Please Upload an image first")


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
                try:
                    recommendations = CustomFashionRecommender(openai_key=openai_key).recommend(cloth_type, gender)
                except:
                    st.error("Please Check your openai key")
                    recommendations =""
                
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
            if not openai_key:
                st.error("Please Enter your openaikey")
            else:
                if not gender:
                    st.error("Gender shoudn't be none")
                else:
                    with st.spinner("Processing...."):
                        try:
                            recommendations = CustomFashionRecommender(openai_key=openai_key).recommend(cloth_type=text, gender=gender)
                        except:
                            st.error("Please Check your openai key")
                            recommendations =""
                    st.write(text)
                    recommendations = recommendations.replace('\n','').split(',')
                    st.json(recommendations)
        else:
            st.error("Cloth type shoudn't be none")