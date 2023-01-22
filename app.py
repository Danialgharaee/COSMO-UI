import requests
import streamlit as st
from streamlit_chat import message
from config import HF_token
key = HF_token
headers = {"Authorization": f"Bearer {key}"}
API_URL = "https://api-inference.huggingface.co/models/allenai/cosmo-xl"

def query(past_user_inputs, generated_responses, text):
    payload = {
        "inputs": {
            "past_user_inputs": past_user_inputs,
            "generated_responses": generated_responses,
            "text": f"{text}"
        },
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

def chatgpt_clone(past_user_inputs, generated_responses, text):
    response = query(past_user_inputs, generated_responses, text)
    return response.json()["generated_text"]

#Streamlit App
st.set_page_config(
    page_title="CosmoChat - Demo",
    page_icon="random"
)

st.header("CosmoChat with Streamlit")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = chatgpt_clone(st.session_state['past'], st.session_state['generated'], user_input)
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
