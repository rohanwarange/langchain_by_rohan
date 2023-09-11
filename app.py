import streamlit as st
import pdfplumber
import bs4 as bs
import urllib.request
from transformers import pipeline

st.sidebar.header("© rohan.sanjay.warange@accenture.com")
st.title('🤗💬 Nationwide Chat App')

st.sidebar.markdown("This app allows users to input text of their choice using the tools provided (PDF, Wikipedia article, or Textbox), and ask questions with the answer being extracted from the text.")
st.sidebar.markdown("_When running the app the first time, it may take some time to initialize due to the requirements needing to be downloaded._")
tool = st.sidebar.selectbox("Tool", ["PDF Q&A", "Wikipedia Q&A", "Textbox Q&A"])
st.write('Made with ❤️ by [Rohan](https://www.linkedin.com/in/rohan-warange-1246ab238)')

# Create the nlp pipeline for question answering
nlp = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", revision="626af31")

def generateAnswer(question, context):
    answer = nlp(question=question, context=context)
    return answer['answer']

# Helper function to extract text from PDF
def extract_data(feed):
    data = ""
    with pdfplumber.open(feed) as pdf:
        pages = pdf.pages
        for p in pages:
            data += p.extract_text()
    return data

# PDF Q&A
def pdf_qna():
    heading = """
    # PDF Q&A
    """
    heading
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    question = st.text_input("Question:")
    if st.button("Get Answer"):
        if uploaded_file is not None:
            context = extract_data(uploaded_file)
            answer = generateAnswer(question, context)
            st.header("Your answer is")
            st.write(answer)

# Wikipedia Q&A
def wikipedia_qna():
    heading = """
    # Wikipedia Q&A
    """
    parsed_article = bs.BeautifulSoup(article, 'lxml')

    heading
    user_input = st.text_input("Wikipedia Link:", value="https://en.wikipedia.org/wiki/Machine_learning")
    question = st.text_input("Question:")

    if st.button("Summarise"):
        scraped_data = urllib.request.urlopen(user_input)
        article = scraped_data.read()

        parsed_article = bs.BeautifulSoup(article,'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""
        for p in paragraphs:
            article_text += p.text

        answer = generateAnswer(question, article_text)
        st.header("Answer")
        st.write(answer)

# Textbox Q&A
def textbox_qna():
    heading = """
    # Textbox Q&A
    Example text from this article: https://www.bbc.co.uk/news/science-environment-53119686
    """
    heading
    dummy_text = '''
    ... (the long text) ...
    '''

    user_input = st.text_area("Text:", value=dummy_text)
    question = st.text_input("Question:")

    if st.button("Answer"):
        answer = generateAnswer(question, user_input)
        st.header("Answer")
        st.write(answer)

if tool == "PDF Q&A":
    pdf_qna()

if tool == "Wikipedia Q&A":
    wikipedia_qna()

if tool == "Textbox Q&A":
    textbox_qna()
