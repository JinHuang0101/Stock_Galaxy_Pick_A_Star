# https://www.sec.gov/edgar/sec-api-documentation

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt


# create request header
headers = {'User-Agent': "jinhuang922@address.com"}

st.title("The Financial Health of Top 10 American Companies by Market Cap")
st.write(""" # Information Source: The SEC EDGAR API""")

#st.header("Data Science Web App")
st.sidebar.header("Dig Into the Top 10 U.S. Companies \n Navigate the App by Simple Clicking")


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
    st.write("Category 1: SEC Form 10-Q. It is a comprehensive report of financial performance that must be submitted quarterly by all public companies to the SEC. In the 10-Q, firms are required to disclose relevant information regarding their finances as a result of their business operations. The 10-Q is generally an unaudited report.--Investopedia")
    st.write("Select the Company 10-Q data if you want to review the metada of a company's 10-Q data in the past 10 year or more and see a visual representation of how the company's asset value changed in the past 10 years or more.")
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

    data_category_list = ["Select a category ", "Company 10-Q data"]
    data_category = st.selectbox("Click on the dropdown menue. Select an information category ", data_category_list)
    # get company filing metadata
    # get company facts data

    if data_category == "Company 10-Q data":
        # get company concept data
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

        # get assets from 10Q forms and reset index
        assets10Q = assetsData[assetsData.form == '10-Q']
        assets10Q = assets10Q.reset_index(drop=True)

        # display the 10Q dataframe
        st.dataframe(assets10Q)

        # diplay the 10Q pyplot graph
        assets10Q.plot(x='end', y='val')
        st.pyplot(plt.gcf())
