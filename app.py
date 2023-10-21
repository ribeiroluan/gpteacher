import streamlit as st
import pyautogui 
from create_quiz import CreateQuizData

st.set_page_config(
     page_title="GPTeacher",
     page_icon=":brain:",
     layout="centered",
     initial_sidebar_state="expanded")

if 'first_time' not in st.session_state:
    st.toast(body="Welcome! Ready to crush some quizzes?", icon="😎")
    st.session_state.first_time = False

st.title(":brain: GPTeacher")
st.write("Welcome to GPTeacher! This app allows you to test your knowledge on a variety of topics. Are you ready?")
    
with st.expander("Video tutorial"):
    video_file = open('GPTeacher_video.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

with st.form(key="user_input"):
    DISCIPLINE = st.text_input("Enter the discpline you want to be tested on (e.g. math, geography, history)")
    TOPIC = st.text_input("Enter the topic within the discipline you want to be tested on (e.g. trigonometry, U.S geography, ancient history)")
    AMOUNT = st.slider("Enter the number of questions you want to answer", min_value = 1, max_value = 10)
    DIFFICULTY = st.radio(label="Set the difficulty level", options=["Easy", "Medium", "Hard"])
    OPENAI_API_KEY = st.text_input("Lastly, an OpenAI API key is necessary to generate the questions", type="password")
    submitted = st.form_submit_button("Generate my quiz!")

if submitted or ('quiz_data_list' in st.session_state):
    with st.spinner("Thinking about the questions...🤓"):
        if submitted:
            quiz_object = CreateQuizData(discipline=DISCIPLINE, topic=TOPIC, difficulty=DIFFICULTY, amount=AMOUNT, api_key=OPENAI_API_KEY)
            quiz_data = quiz_object.create()
            st.session_state.quiz_data_list = quiz_data

            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []
            if 'justifications' not in st.session_state:
                st.session_state.justifications = []

            for q in st.session_state.quiz_data_list:
                st.session_state.randomized_options.append(q[1])
                st.session_state.correct_answers.append(q[2])
            
        with st.form(key="quiz_form"):
            st.subheader("Quiz time: test your knowledge!", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(label=q[0], options=options)
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index

            results_submitted = st.form_submit_button(label='Unveil my score!')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

                if score == len(st.session_state.quiz_data_list):  # Check if all answers are correct
                    st.balloons()

                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                
                    if incorrect_count == 1:
                        st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                    else:
                        st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        st.info(f"Question: {q[0]}")
                        if ro[ua] == ca:
                            st.success(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")
                        else:
                            st.error(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")
                        st.info(f"Explanation: {q[3]}")

        st.subheader(":point_right: Want to get tested again? Click the Reset button below!")
        if st.button("Reset"):
            pyautogui.hotkey("ctrl","R")