import streamlit as st
from os import getenv
from dotenv import load_dotenv
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain


def create_quiz(discipline: str, topic: str, difficulty: str, amount:int) -> list:

    #Getting API key
    load_dotenv()
    openai.api_key = getenv("OPENAI_API_KEY")

    template = f"""
        You are an education specialist with a vast knowledge in various fields. A teacher wants help with creating a questionaire for her students and you will help her based on four parameters: discipline (like math, geography, english or history), topic (like trigonometrics, geometry, literature), difficulty (easy, medium, hard) and number of questions (1 to 10).

        Create 5 questions assuming the following paramenters
        1. Discipline: {discipline}
        2. Topic: respiratory {topic}
        3. Difficulty: {difficulty}
        4. Number of questions: {amount}

        For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 
        Your output should be shaped as follows:

        1. An outer list that contains inner lists for each question.
        2. Each inner list represents a set of question and answers, and contains exactly 4 strings in this order:
        - The generated question.
        - Correct answer
        - Incorrect answer
        - Incorrect answer
        - Incorrect answer
        - Justification for the correct answer


        Your output should mirror this structure:
        [
            ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2", "Incorrect Answer 1.3", "Justification for the correct answer 1"],
            ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2", "Incorrect Answer 2.3", "Justification for the correct answer 2"],
            ...
        ]

        It is crucial that you adhere to this format as it's optimized for further Python processing.
        """

    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=template,
        max_tokens=300
    )

    generated_questions = response.choices[0].text.strip().split('[[')[1].strip().split(']]')[0].split('],')

    questions_list = []
    for question in generated_questions:
        items = question.strip().strip('[[').strip(']]').split('","')
        questions_list.append([item.strip('"') for item in items])

    return questions_list

print(create_quiz("math", "trigonometry", "hard", "3"))