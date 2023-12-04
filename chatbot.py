import streamlit as st 
import openai 
from env import model_engine, open_ai_api_key

openai.api_key = open_ai_api_key

def chatbot_query(title):
    if len(title) != 0:
        st.sidebar.write("Your question is: ", title)
        prompt = title 

        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            temperature=0.6,
        )
        response = completion.choices[0].text 
        st.sidebar.write(response)