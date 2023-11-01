import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# import datetime as dt

# create request header
headers = {'User-Agent': "jinhuang922@address.com"}

st.write(""" # Finance App by Calling SEC EDGAR API""")

st.title("Stock Market Info")

st.header("Data Science Web App")
st.sidebar.header("Jin Huang \n Finance Web App ...")


# get ticker input from user
ticker_list = ['Select a top 10 American company by market cap',
               'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'BRK-B', 'TSLA', 'LLY', 'V']

cik_dict = {"AAPL": "320193", "MSFT": "789019", "GOOGL": "1652044", "AMZN": "1018724", "NVDA": "1045810",
            "META": "1326801", "BRK-B": "1067983", 'TSLA': "1318605", 'LLY': "59478", 'V': "1403161"}

ticker = st.selectbox('Select a stock', ticker_list)

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
    stock = ticker
    cik_str = ""

    # get the raw cik str
    for key in cik_dict:
        if key == stock:
            cik_str += cik_dict[key]
    st.write(cik_str)

    # add leading 0s
    cik_str = cik_str.zfill(10)
    st.write(cik_str)

    data_category_list = ["Select a category ", "Company 10-Q data"]
    data_category = st.selectbox("Select a category ", data_category_list)
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
