from setuptools import setup, find_packages

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Tai Lam",
    author_email="lamtai2105@gmail.com",
    description="A package for generating multiple-choice questions using AI.",
    install_requires=[
        "openai==1.37.1",
        "langchain==0.1.20",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],  
    packages=find_packages()
)