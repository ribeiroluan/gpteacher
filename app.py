import streamlit as st
import time
from create_quiz import CreateQuizData

st.set_page_config(
     page_title="GPTeacher",
     page_icon=":brain:",
     layout="centered",
     initial_sidebar_state="expanded")

st.title(":brain: GPTeacher")
st.write("Welcome to GPTeacher! This app allow you to test your knowledge on a variety of topics!")
    
with st.sidebar:
    st.header("I am a sidebar")

with st.form(key="user_input"):
    DISCIPLINE = st.text_input("Enter the discpline you want to be tested on (e.g. math, geography, history)")
    TOPIC = st.text_input("Enter the topic within the discipline you want to be tested on (e.g. trigonometry, U.S geography, ancient history)")
    AMOUNT = st.slider("Enter the number of questions you want to answer", min_value = 3, max_value = 10)
    DIFFICULTY = st.radio(
        "Set the difficulty",
        options=["Easy", "Medium", "Hard"],
    )

    submitted = st.form_submit_button("Generate my quiz!")

if submitted:
    
    with st.spinner("Crafting your quiz...🤓"):
        quiz_object = CreateQuizData(discipline=DISCIPLINE, topic=TOPIC, difficulty=DIFFICULTY, amount = AMOUNT)
        quiz_data = CreateQuizData(discipline=DISCIPLINE, topic=TOPIC, difficulty=DIFFICULTY, amount = AMOUNT).create()
        
        ############ CONTINUE FROM HERE ############
        with st.form(key="quiz_form"):
            st.subheader("Quiz time: test your knowledge!", anchor=False)
            for i, q in enumerate(quiz_data):
                options = quiz_data[i][1]
                response = st.radio(q[0], options)
                user_choice_index = options.index(response)

            results_submitted = st.form_submit_button(label='Unveil My Score!')