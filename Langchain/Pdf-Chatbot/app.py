import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.question_answering import load_qa_chain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    vectorstore.save_local("faiss_index")

def get_conversation_chain():
    prompt_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    {context}
    Question: {question}
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = load_qa_chain(
        llm=GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3),
        chain_type="stuff",
        prompt=PROMPT
    )
    
    return chain    


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True,
    )

    chain = get_conversation_chain()
    docs = vectorstore.similarity_search(user_question)

    response = chain(
        {
            "input_documents": docs, "question": user_question
        } , return_only_outputs=True
    )

    st.write("Response: ", response["output_text"])



def main():
    st.set_page_config(page_title="PDF Chatbot", page_icon=":books:")
    st.header("Chat with multiple PDFs :books:")

    user_question = st.text_input("Ask a question about your documents:")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                # Get PDF text
                raw_text = get_pdf_text(pdf_docs)

                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # Create vector store
                get_vectorstore(text_chunks)
                st.success("Processing complete. You can now ask questions about your documents.") 


main()