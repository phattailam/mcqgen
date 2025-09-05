import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import streamlit as st
from langchain.callbacks import get_openai_callback 
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


# loading json file
with open("/home/tailam/SSL/Generative_AI/Generative_AI_course_1/mcqgen/Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)


# creating a title for the app
st.title("MCQs Generator Application with LangChain")

# creat a form using st.form
with st.form("user_inputs"):
    # file upload
    uploaded_file = st.file_uploader("Upload a text file", type=["txt", "pdf"])
    
    # input fields
    mcq_count = st.number_input("Number of MCQs", min_value=3, max_value=50)
    
    # creating a selectbox to select the subject
    subject = st.text_input("Insert subject", max_chars=50)
    
    # creating a selectbox to select the tone
    tone = st.text_input("Complexity level of questions", max_chars=50, placeholder="Simple")
    
    # creating a submit button
    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                # Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )

            except Exception as e:
                traceback.print_exception(type(e), value=e, tb=e.__traceback__)
                st.error(f"An error occurred: {e}")

            else:
                print(f"Total tokens: {cb.total_tokens}")
                print(f"Prompt tokens: {cb.prompt_tokens}")
                print(f"Completion tokens: {cb.completion_tokens}")
                print(f"Total cost (USD): {cb.total_cost}")

                if isinstance(response, dict):
                    # Extracting quiz data from response
                    quiz = response.get("quiz", None)

                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Displaying the review in a text box
                            st.text_area(label="review", value=response.get("review"))
                        else:
                            st.error("Error in the table data")

                else:
                    st.write(response)


# streamlit run StreamLitAPP.py