import streamlit as st
import time

def create_quiz(discipline: str, topic: str, difficulty: str, amount:int) -> list:
    time.sleep(5)
    return("Generating quiz")


st.set_page_config(
     page_title="GPTeacher",
     page_icon=":male-teacher:",
     layout="centered",
     initial_sidebar_state="expanded")

st.title(":brain: GPTeacher")
st.write("Welcome to GPTeacher! This app allow you to test your knowledge on a variety of topics!")
    
with st.sidebar:
    st.header("I am a sidebar")

with st.form("user_input"):
    DISCIPLINE = st.text_input("Enter the discpline you want to be tested on (e.g. math, geography, history)")
    TOPIC = st.text_input("Enter the topic within the discipline you want to be tested on (e.g. trigonometry, U.S geography, ancient history)")
    AMOUNT = st.slider("Enter the number of questions you want to answer", min_value = 1, max_value = 10)
    DIFFICULTY = st.radio(
        "Set the difficulty",
        options=["Easy", "Medium", "Hard"],
    )

    submitted = st.form_submit_button("Generate my quiz!")

if submitted:
    
    with st.spinner("Crafting your quiz...🤓"):
        st.write(create_quiz(discipline=DISCIPLINE, topic=TOPIC, difficulty=DIFFICULTY, amount = AMOUNT))
