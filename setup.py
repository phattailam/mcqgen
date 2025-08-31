from setuptools import setup, find_packages

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Tai Lam",
    author_email="lamtai2105@gmail.com",
    description="A package for generating multiple-choice questions using AI.",
    install_requires=[
        "openai",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],  
    packages=find_packages()
)