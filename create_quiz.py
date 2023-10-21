import openai
import streamlit as st

import ast
import random

class CreateQuizData:

    def __init__(self, discipline: str, topic: str, difficulty: str, amount:int, api_key:str) -> None:
        self.discipline = discipline
        self.topic = topic
        self.difficulty = difficulty
        self.amount = amount
        self.api_key = api_key

    def quiz_data_str(self) -> str:
        openai.api_key = self.api_key

        system = f"You are an education specialist with a vast knowledge in various fields and specializes in creating questionnaires. You will create python lists"
        user = f"""
           A teacher needs help creating questions to assess her students learning. You will create questionnaires based on four parameters: discipline (like math, geography, english or history), topic (like trigonometrics, geometry, literature), difficulty (easy, medium, hard) and number of questions (1 to 10).

            Create questions assuming the following paramenters
            1. Discipline: {self.discipline}
            2. Topic: {self.topic}
            3. Difficulty: {self.difficulty}
            4. Number of questions: {self.amount}

            For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 
            Your output should be shaped as follows:

            1. An outer list that contains an inner lists for each question
            2. Each inner list represents a set of question and answers, and contains exactly 4 strings in this order:
            - The generated question.
            - Correct answer
            - Incorrect answer
            - Incorrect answer
            - Incorrect answer
            - Justification for the correct answer

            Your output should mirror this exact structure. Do not include any further comments or explanation:
            [
                ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2", "Incorrect Answer 1.3", "Justification for the correct answer 1"],
                ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2", "Incorrect Answer 2.3", "Justification for the correct answer 2"],
                ...
            ]
            """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [
                    {
                        "role": "system",
                        "content": system
                    },
                    {
                        "role": "user",
                        "content": user
                    },
                    {
                        "role": "assistant",
                        "content": ""
                    }
                ],
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.0
            )
            return response.choices[0]["message"]["content"]
        except:
            st.error(f"The OpenAI key you provided is not valid.")
            st.stop()


    def string_to_list(self, s) -> list:
        try:
            return ast.literal_eval(s)
        except (SyntaxError, ValueError) as e:
            st.error(f"Error: The provided input is not correctly formatted. {e}")
            st.stop()

    def get_randomized_options(self, options) -> tuple:
        question = options[0]
        correct_answer = options[1]
        justification = options[5]
        shuffled_options = options[1:5]
        random.shuffle(shuffled_options)
        return question, shuffled_options, correct_answer, justification
    
    def create(self):
        final_questions_list = []
        for q in self.string_to_list(self.quiz_data_str()):
            output = self.get_randomized_options(q)
            final_questions_list.append(output)
        #print(final_questions_list)
        return final_questions_list
