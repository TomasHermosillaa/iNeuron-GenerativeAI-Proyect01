# Import libraries
import os
import json
import pandas as pd
import traceback
import PyPDF2
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

# Langchain imports
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

# Load enviroment variables from the .env file
load_dotenv()

# Get the OpenAI key in a variable
KEY = os.getenv("OPENAI_API_KEY")

# Pick the model and initialize the API
llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-3.5-turbo", temperature=0.7)

# Prompt template
TEMPLATE ="""
Text:{text1}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

# Charge the prompt inputs and template
quiz_prompt = PromptTemplate(
    input_variables=["text1", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

# Create the llm chain, which execute the prompt and store the output in quiz
quiz_chain=LLMChain(llm=llm, prompt=quiz_prompt, verbose=True, output_key='quiz')

# Create a Template 2 and prompt for quiz evaluation
TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
quiz_evaluation_prompt = PromptTemplate(input_variables=['subject', 'quiz'], template=TEMPLATE2)
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key='review', verbose= True)


# Sequential chain tha mix both chains
seq_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text1", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)

