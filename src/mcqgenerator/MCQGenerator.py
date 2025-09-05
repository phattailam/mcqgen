import os 
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

#importing necessary packages from langchain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


load_dotenv()

key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=key, temperature=0.3)

template = """
Text: {text}
You are an expert MCCQ maker. Given the above text, it is your job to\
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be comforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
### RESPONSE_JSON:
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


template2 = """
You are an expert english grammarican and writer. Given a Multiple Choice Quiz for {subject} students,\
You need to evaluate the complexity of the questions and give a complete analysis of the quiz. Only use at max 50 words for complexity \
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the students abilities.\
Quiz_MCQs:
{quiz}

Check from an expert english writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],    
    template=template2
)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(chains=[quiz_chain, review_chain],
                                          input_variables=["text", "number", "subject", "tone", "response_json"],
                                          output_variables=["quiz", "review"],
                                          verbose=True)

