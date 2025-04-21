from model_helper import predict
import streamlit as st


st.set_page_config(
    page_title="Car Damage Detector",  # Tab title
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="auto"
)



st.title('Car Damage Detection')

uploaded_file = st.file_uploader("Upload an image of a car", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_path = 'temp_file.jpg'
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        st.image(image_path, caption='Uploaded File', use_column_width=True)
        prediction = predict(image_path)
        st.info(f"Prediction Class: {prediction}")
