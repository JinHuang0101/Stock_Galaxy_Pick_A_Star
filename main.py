# https://www.sec.gov/edgar/sec-api-documentation

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# import OpenAI package 
import openai
openai.api_key = "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"
model_engine = "text-davinci-003"

# create request header to call SEC API
headers = {'User-Agent': "jinhuang922@address.com"}

st.title("The Financial Health of Top 10 American Companies by Market Cap")
st.write(""" # Information Source: The SEC EDGAR API""")

#st.header("Data Science Web App")
st.sidebar.header("Dig Into the Top 10 U.S. Companies \n Navigate the app by clicking; Get explanations by asking a chatbot")
title=st.sidebar.text_input("Hi, I am a chatbot powered by OpenAI. I can help you learn financial information presented on this web app. Ask me any question. For example, what does financial health mean for a company? What does a company\'s 10-K data mean?")
if len(title) != 0:
    st.sidebar.write("Your question is: ", title)
    prompt = title 

    # prompt="List the top ten United States companies by market cap"
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.6,
    )
    response = completion.choices[0].text 
    st.sidebar.write(response)

# get ticker input from user
ticker_list = ['Select a top 10 American company by market cap',
               'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'BRK-B', 'TSLA', 'LLY', 'V']

cik_dict = {"AAPL": "320193", "MSFT": "789019", "GOOGL": "1652044", "AMZN": "1018724", "NVDA": "1045810",
            "META": "1326801", "BRK-B": "1067983", 'TSLA': "1318605", 'LLY': "59478", 'V': "1403161"}

ticker = st.selectbox('Interested in a company? Click on the dropdown menue. Select the stock ticker of the company. ', ticker_list)

if ticker != "Select a top 10 American company by market cap":
    # Markdown and confirmation
    html_str = f"""
    <style>
    p.a {{
    font: bold 30px Courier;
    }}
    </style>
    <p class="a">{ticker}</p>
    """
    st.markdown(html_str, unsafe_allow_html=True)
    st.write("What financial information do you want to review?")
    st.write("Category 1: 10-K Assets.Category 2: 10-K Revenues.")
    # st.write("Select the Company 10-K data if you want to review the metada of a company's 10-K data in the past 10 year or more and see a visual representation of how the company's asset value changed in the past 10 years or more.")

    stock = ticker
    cik_str = ""

    # get the raw cik str
    for key in cik_dict:
        if key == stock:
            cik_str += cik_dict[key]
    #st.write(cik_str)

    # add leading 0s
    cik_str = cik_str.zfill(10)
    #st.write(cik_str)

    data_category_list = ["Select a category ", "10-K Assets", "10-K Revenues"]
    data_category = st.selectbox("Click on the dropdown menue. Select an information category ", data_category_list)
    # get company filing metadata
    # get company facts data

    if data_category == "10-K Assets":
        # get company concept/Assets data
        companyConcept = requests.get(
            (
                f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_str}'
                f'/us-gaap/Assets.json'
            ),
            headers=headers
        )

        # get filings data
        assetsData = pd.DataFrame.from_dict(
            (companyConcept.json()['units']['USD']))

        # get assets from 10K forms and reset index
        assets10K = assetsData[assetsData.form == '10-K']
        assets10K = assets10K.reset_index(drop=True)

        # display the 10K dataframe
        st.dataframe(assets10K)

        # diplay the 10K pyplot graph
        assetsPlot = assets10K.plot(x='end', y='val', title='Assets Reported in 10-K')
        assetsPlot.set_xlabel("Report Date")
        assetsPlot.set_ylabel("Assets")

        st.pyplot(plt.gcf())
    
    elif data_category == "10-K Revenues":
        # get company concept/Assets data
        companyConcept = requests.get(
            (
                f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_str}'
                f'/us-gaap/Revenues.json'
            ),
            headers=headers
        )

        # get filings data
        revenuesData = pd.DataFrame.from_dict(
            (companyConcept.json()['units']['USD']))

        # get assets from 10K forms and reset index
        revenues10K = revenuesData[revenuesData.form == '10-K']
        revenues10K = revenues10K.reset_index(drop=True)

        # display the 10K dataframe
        st.dataframe(revenues10K)

        # diplay the 10K pyplot graph
        revenuesPlot = revenues10K.plot(x='end', y='val', title='Revenues Reported in 10-K')
        revenuesPlot.set_xlabel("Report Date")
        revenuesPlot.set_ylabel("Revenues")

        st.pyplot(plt.gcf())
