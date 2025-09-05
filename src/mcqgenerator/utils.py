import os
import json
import traceback
import PyPDF2


def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
        
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise Exception("Unsupported file format. Please upload a PDF or TXT file.")
    

def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option} -> {option_value}" for option, option_value in value.get("options").items()
                ]
            )

            correct = value.get("correct")
            quiz_table_data.append({"MCQ": mcq, "Options": options, "Correct": correct})

        return  quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), value=e, tb=e.__traceback__)
        return False