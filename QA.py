import os
import warnings
import streamlit as st
import time

# langchain libraries
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

### -------- SESSION STATE ---------
if 'memories' not in st.session_state:
    st.session_state.memories = []
if 'state' not in st.session_state:
    st.session_state.state = None

# Suppress warnings related to date parsing
warnings.filterwarnings("ignore")

# openai API key
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# Page config
st.set_page_config(page_title="Q&A", page_icon="🤖")

# webapp title
st.title('Course Assistant')

# Vector DB
embeddings = OpenAIEmbeddings()
vector_db = FAISS.load_local("vector_db", embeddings, allow_dangerous_deserialization=True)

### ---------- FUNCTIONS ------------
def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.04)

def get_context(preference):
    docs_faiss = vector_db.similarity_search_with_relevance_scores(preference, k=10)
    return docs_faiss


# function to ask llm model question and generate answer
def generate_response(context, query) -> str:
    with st.spinner('Thinking...'):
        # Define the role of the assistant and prepare the prompt
        system = """You are a data science instructor. Answer the student's question professionally and concisely, using only the information provided within the given context. 
        Avoid introducing any external information. Refer to previous conversations when relevant to provide a clear and thorough response, addressing any lingering doubts. 
        Ensure that your answer includes the following:
        - The name(s) of the relevant Section(s)
        - The name(s) of the specific Lecture(s)
        """
        # prompt template, format the system message and user question
        TEMPLATE = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("system", "Chat history: {chat_history}"),
            ("system", "Context: {context}"),
            ("human", "Question: {query}"),
        ]
        )
        prompt = TEMPLATE.format(chat_history= st.session_state.memories, context= context, query=query)

        model = ChatOpenAI(model="gpt-4o")
        response_text = model.invoke(prompt).content
        st.session_state.memories.append({"role": "assistant", "content": response_text})

    with st.chat_message("assistant"):
        st.write_stream(stream_data(response_text))


### ----------- APP -------------
for memory in st.session_state.memories:
    with st.chat_message(memory["role"]):
        st.write(memory["content"])

if st.session_state.state == None:
    with st.chat_message("assistant"):
        intro = """
                 Hello! Do you have any questions I can help with today?
                  \n"""
        st.write(intro)
    # Add intro message to chat history
    st.session_state.memories.append({"role": "assistant", "content": intro})
    st.session_state.state = 'q-a'

# Accept user input
if user_input := st.chat_input("Say Something"):
    st.session_state.input = user_input
    # Add user message to chat history
    st.session_state.memories.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(user_input)
    
    context = get_context(user_input)
    generate_response(context, user_input)