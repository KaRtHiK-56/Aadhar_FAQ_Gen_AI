import streamlit as st 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


st.title("Next-Gen AI Solution for Efficient Aadhaar Card FAQs")
text = st.text_area("Please enter your query or doubts related to Aadhar FAQ:",height = 200)

def aadhar(text):
    page = PyPDFLoader("AadharFAQ.pdf")

    page = page.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splitter = text_splitter.split_documents(page)


    embeddings=HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device':'cpu'},
        encode_kwargs={'normalize_embeddings':True}

    )
    db = Chroma.from_documents(splitter, embeddings)


    llm = Ollama(model="llama2",temperature=0)

    from langchain_core.prompts import ChatPromptTemplate
    prompt = ChatPromptTemplate.from_template(""" You are a helpful assistant in the field of inidan government and you are in a role of
                                              helping people that has doubt in AAdhar card services. Think step by step before answering the question.
                                              <context>
                                              {context}
                                              </context>
                                              question : {input} """)

    chain = create_stuff_documents_chain(llm,prompt)

    retriver = db.as_retriever()


    chains = create_retrieval_chain(retriver,chain)

    answer = chains.invoke({"input":text})

    return answer['answer']

submit = st.button("Submit")

if submit:
    st.write(aadhar(text))
