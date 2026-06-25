import streamlit as st

# Title
st.title("My First Streamlit App")

# Text
st.write("Welcome to Streamlit!")

# Input box
name = st.text_input("Enter your name")

# Button
if st.button("Submit"):
    st.success("Hello " + name)