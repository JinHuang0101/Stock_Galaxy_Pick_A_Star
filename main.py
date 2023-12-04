# https://www.sec.gov/edgar/sec-api-documentation

import streamlit as st
import pandas as pd
import numpy as np 
from pathlib import Path 
from input_to_req import selectToAPI
from get_sec_data import getData, jsonToDF, ten_k_data, data_top
from plot_graph import plotGraph, plotBar
from chatbot import chatbot_query

# get the top company tickers and cik strs from SEC doc
filepath = Path.cwd().joinpath('companyDataKeys').joinpath('company_tickers.json')
sec_dict = pd.read_json(filepath).to_dict()
max_company_number = len(sec_dict)

st.header("Stock Galaxy:stars: Discover a Star:star2:", divider='rainbow')
st.write(f"""You can find the 10-K data of all :rainbow[{max_company_number}] SEC-listed companies here. That's a lot... Why not browse the companies by groups? See if you can discover a :star:""")
st.subheader("First: Select a group of stocks to browse")
st.write(f"""For example, if you want to browse the 50 biggest companies, enter 1 in :orange[From] and 50 in :orange[To]. Or if you want to browse the 20 companies from the 100th to the 119th biggest, enter 100 in :orange[From] and 119 in :orange[To]. In the SEC database, all :rainbow[{max_company_number}] companies are sorted by market cap from the biggest to the smallest. You can select any range of them with any group size in this app.""")

col3, col4 = st.columns(2)
with col3:
    top_comp = st.number_input(f"""**:orange[From]**: """, min_value=1, max_value=max_company_number, step=1, placeholder=f"Type a number from 1 to {max_company_number}")
with col4:
    bottomn_comp = st.number_input(f"""**:orange[To]** : """, min_value=top_comp, max_value=max_company_number, step=1, placeholder=f"Type a number from {top_comp} to {max_company_number}")

st.subheader("Next: Two ways to browse side-by-side")


# st.sidebar.write("the ", top_comp, "th", "to the ", bottomn_comp, "th", "biggest companies")

# get the top company tickers and cik strs from SEC doc
cik_dict = {}
for i in range(top_comp-1, bottomn_comp):
    cik_dict[sec_dict[i]['ticker']]=[]
    cik_dict[sec_dict[i]['ticker']].append(str(sec_dict[i]['cik_str']))
    cik_dict[sec_dict[i]['ticker']].append(str(sec_dict[i]['title']))

for stock in cik_dict:
    cik_str = ""
    cik_dict[stock].append(cik_dict[stock][0].zfill(10))

col1, col2 = st.columns(2)


st.sidebar.text("Click to navigate")
# st.sidebar.text("Need explanation?")
st.sidebar.text("Stuck? Ask a chatbot")
title=st.sidebar.text_input("Hi, I am a chatbot powered by OpenAI. No question is too silly to ask. Like, what is a company's 10-K report? Why does the 10-K matter?")
chatbot_query(title)



sorted_list = sorted(list(cik_dict))
# st.write(sorted_list)

ticker_list = [f'Select a ticker'] + sorted_list
# st.write(cik_dict)

stats_list = ['Select a metric', 
              'Latest Assets', 'Latest Income', 'Latest Revenues',
              'Latest Gross Profit', 'Latest Costs', 'Latest Operating Expenses',
              'Latest Operating Income Loss', 'Latest EPS Basic',
              'Latest Depreciation', 'Latest EPS Diluted'
              ]

info_list = ['10-K Assets', '10-K Revenues', '10-K Gross Profit', 
            '10-K Costs', '10-K Operating Expenses', '10-K Operating Income Loss', 
            "10-K Net Income Loss", "10-K Earnings Per Share Basic", "10-K Earnings Per Share Diluted",
            "10-K Depreciation", "10-K Cash"]

# Rank all top companies on one metric 
with col1:
    if bottomn_comp - top_comp +1 > 1:
        st.markdown(f"""**Rank :orange[All] :orange[{bottomn_comp - top_comp+1}] Companies by :orange[1] Metric in the :orange[Latest] 10-K**""")
    else:
        st.markdown(f"""**Rank :orange[All] Companies by :orange[1] Metric in the :orange[Latest] 10-K**""")
    statsAnalysis = st.selectbox(f'Pick a metric. Companies ranked in a **descending** order. ', stats_list)
    
    if statsAnalysis == "Latest Revenues":
        sorted_latest_revenues_df = data_top(cik_dict, "10-K Revenues")
        st.write(sorted_latest_revenues_df)
        st.write(f"""**{sorted_latest_revenues_df.iloc[0, 0]}** has the **biggest** Revenues of {sorted_latest_revenues_df.iloc[0, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_revenues_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_revenues_df.iloc[-1, 0]}** has the **smallest** Revenues of {sorted_latest_revenues_df.iloc[-1, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_revenues_df.iloc[-1, 2]}""")
        
    elif statsAnalysis == "Latest Income":
        sorted_latest_income_df = data_top(cik_dict, "10-K Net Income Loss")
        st.write(sorted_latest_income_df)
        st.write(f"""**{sorted_latest_income_df.iloc[0, 0]}** has the **biggest** Income of {sorted_latest_income_df.iloc[0, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_income_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_income_df.iloc[-1]["stock"]}** has the **smallest** Income of  {sorted_latest_income_df.iloc[-1]["latest_value"]/1000000} million in the most recent 10-K report filed on {sorted_latest_income_df.iloc[-1]["filed_date"]}""")
    
    elif statsAnalysis == "Latest Assets":
        sorted_latest_assets_df = data_top(cik_dict, "10-K Assets")
        st.write(sorted_latest_assets_df)
        st.write(f"""**{sorted_latest_assets_df.iloc[0, 0]}** has the **biggest** Assets of {sorted_latest_assets_df.iloc[0, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_assets_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_assets_df.iloc[-1, 0]}** has the **smallest** Assets of {sorted_latest_assets_df.iloc[-1, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_assets_df.iloc[-1, 2]}""")


    elif statsAnalysis == "Latest Gross Profit":
        sorted_latest_gross_profit_df = data_top(cik_dict, "10-K Gross Profit")
        st.write(sorted_latest_gross_profit_df)
        st.write(f"""**{sorted_latest_gross_profit_df.iloc[0, 0]}** has the **biggest** Gross Profit of {sorted_latest_gross_profit_df.iloc[0, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_gross_profit_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_gross_profit_df.iloc[-1, 0]}** has the **smallest** Gross Profit of {sorted_latest_gross_profit_df.iloc[-1, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_gross_profit_df.iloc[-1, 2]}""")

    elif statsAnalysis == "Latest Costs":
        sorted_latest_costs_df = data_top(cik_dict, "10-K Costs")
        st.write(sorted_latest_costs_df)
        st.write(f"""**{sorted_latest_costs_df.iloc[0, 0]}** has the **biggest** Costs of {sorted_latest_costs_df.iloc[0, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_costs_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_costs_df.iloc[-1, 0]}** has the **smallest** Costs of {sorted_latest_costs_df.iloc[-1, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_costs_df.iloc[-1, 2]}""")

    elif statsAnalysis == "Latest Operating Expenses":
        sorted_latest_operating_exp_df = data_top(cik_dict, "10-K Operating Expenses")
        st.write(sorted_latest_operating_exp_df)
        st.write(f"""**{sorted_latest_operating_exp_df.iloc[0, 0]}** has the **biggest** Operating Expenses of {sorted_latest_operating_exp_df.iloc[0, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_operating_exp_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_operating_exp_df.iloc[-1, 0]}** has the **smallest** Operating Expenses of {sorted_latest_operating_exp_df.iloc[-1, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_operating_exp_df.iloc[-1, 2]}""")

    elif statsAnalysis == "Latest Operating Income Loss":
        sorted_latest_operating_inc_df = data_top(cik_dict, "10-K Operating Income Loss")
        st.write(sorted_latest_operating_inc_df)
        st.write(f"""**{sorted_latest_operating_inc_df.iloc[0, 0]}** has the **biggest** Operating Income Loss of {sorted_latest_operating_inc_df.iloc[0, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_operating_inc_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_operating_inc_df.iloc[-1, 0]}** has the **smallest** Operating Income Loss of {sorted_latest_operating_inc_df.iloc[-1, 1]/1000000} million in the most recent 10-K report filed on {sorted_latest_operating_inc_df.iloc[-1, 2]}""")

    elif statsAnalysis == "Latest EPS Basic":
        sorted_latest_eps_basic_df = data_top(cik_dict,  "10-K Earnings Per Share Basic")
        st.write(sorted_latest_eps_basic_df)
        st.write(f"""**{sorted_latest_eps_basic_df.iloc[0, 0]}** has the **biggest** EPS Basic of {sorted_latest_eps_basic_df.iloc[0, 1]} in the most recent 10-K report filed on {sorted_latest_eps_basic_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_eps_basic_df.iloc[-1, 0]}** has the **smallest** EPS Basic of {sorted_latest_eps_basic_df.iloc[-1, 1]} in the most recent 10-K report filed on {sorted_latest_eps_basic_df.iloc[-1, 2]}""")

    elif statsAnalysis == "Latest Depreciation":
        sorted_latest_depc_df = data_top(cik_dict,  "10-K Depreciation")
        st.write(sorted_latest_depc_df)
        st.write(f"""**{sorted_latest_depc_df.iloc[0, 0]}** has the **biggest** Depreciation of {sorted_latest_depc_df.iloc[0, 1]} in the most recent 10-K report filed on {sorted_latest_depc_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_depc_df.iloc[-1, 0]}** has the **smallest** Depreciation of {sorted_latest_depc_df.iloc[-1, 1]} in the most recent 10-K report filed on {sorted_latest_depc_df.iloc[-1, 2]}""")

    elif statsAnalysis == "Latest EPS Diluted":
        sorted_latest_eps_diluted_df = data_top(cik_dict,  "10-K Earnings Per Share Diluted")
        st.write(sorted_latest_eps_diluted_df)
        st.write(f"""**{sorted_latest_eps_diluted_df.iloc[0, 0]}** has the **biggest** EPS Diluted of {sorted_latest_eps_diluted_df.iloc[0, 1]} in the most recent 10-K report filed on {sorted_latest_eps_diluted_df.iloc[0, 2]}""")
        st.write(f"""**{sorted_latest_eps_diluted_df.iloc[-1, 0]}** has the **smallest** EPS Diluted of {sorted_latest_eps_diluted_df.iloc[-1, 1]} in the most recent 10-K report filed on {sorted_latest_eps_diluted_df.iloc[-1, 2]}""")

# Query data of one company
with col2:
    st.markdown(f"""**Browse :orange[All] Historical Data of :orange[1] Company**""")
    ticker = st.selectbox('Pick a ticker. Sorted alphabetically.', ticker_list)
 
    if ticker != f"Select a ticker":
        company_name = cik_dict[ticker][1]

        stock = ticker
        st.text(f"""{stock}: {company_name}""")

        # get the zfilled 10 digit cik_str for API calls
        cik_str = cik_dict[stock][2]

        data_category_list = ["Select a metric "] + info_list

        data_category = st.selectbox("Pick a financial metric to review ", data_category_list)

        if data_category == "10-K Assets":
            # call API and get json data
            companyConcept=getData(cik_str, selectToAPI["10-K Assets"], stock)
            if companyConcept is not None:
                # parse json data and return df data 
                assetsData = jsonToDF(companyConcept, "10-K Assets", stock)
                # get 10-K data and reset index
                assets10K = ten_k_data(assetsData)
                if assets10K is not None:
                    # display the 10K dataframe
                    st.dataframe(assets10K)
                    plotGraph(assets10K, 'Assets')
            
        elif data_category == "10-K Revenues":        
            companyConcept=getData(cik_str, selectToAPI["10-K Revenues"], stock)
            if companyConcept is not None:
                revenuesData = jsonToDF(companyConcept, "10-K Revenues", stock)
                if revenuesData is not None:
                    revenues10K = ten_k_data(revenuesData)
                    st.dataframe(revenues10K)
                    plotGraph(revenues10K, "Revenues")

        elif data_category == "10-K Gross Profit":
            companyConcept=getData(cik_str, selectToAPI["10-K Gross Profit"], stock)
            if companyConcept is not None:
                profitData = pd.DataFrame.from_dict(
                    (companyConcept.json()['units']['USD']))
                profitData = jsonToDF(companyConcept, "10-K Gross Profit", stock)
                if profitData is not None:
                    profit10K = ten_k_data(profitData)
                    st.dataframe(profit10K)
                    plotGraph(profit10K, "Gross Profit")
        
        elif data_category == "10-K Costs":
            # get company concept/Assets data
            companyConcept=getData(cik_str, selectToAPI["10-K Costs"], stock)
            if companyConcept is not None:
                costData = jsonToDF(companyConcept, "10-K Costs", stock)
                if costData is not None:
                    cost10K = ten_k_data(costData)
                    st.dataframe(cost10K)
                    plotGraph(cost10K, "Cost Of Goods And Services Sold")

        elif data_category == "10-K Operating Expenses":
            companyConcept=getData(cik_str, selectToAPI["10-K Operating Expenses"], stock)
            if companyConcept is not None:
                operatingExpData = jsonToDF(companyConcept, "10-K Operating Expenses", stock)
                if operatingExpData is not None:
                    operatingExp10K = ten_k_data(operatingExpData)
                    st.dataframe(operatingExp10K)
                    plotGraph(operatingExp10K, "Operating Expenses")
    
        elif data_category == "10-K Operating Income Loss":
            companyConcept=getData(cik_str, selectToAPI["10-K Operating Income Loss"], stock)
            if companyConcept is not None:
                operatingIncomeData = jsonToDF(companyConcept, "10-K Operating Income Loss", stock)
                if operatingIncomeData is not None:
                    operatingIncome10K = ten_k_data(operatingIncomeData)
                    st.dataframe(operatingIncome10K)
                    plotGraph(operatingIncome10K, "Operating Income Loss")
        
        elif data_category == "10-K Net Income Loss":
            companyConcept=getData(cik_str, selectToAPI["10-K Net Income Loss"], stock)
            if companyConcept is not None:
                netOperatingIncomeData = jsonToDF(companyConcept, "10-K Net Income Loss", stock)
                if netOperatingIncomeData is not None:
                    netOperatingIncome10K = ten_k_data(netOperatingIncomeData)
                    st.dataframe(netOperatingIncome10K)
                    plotGraph(netOperatingIncome10K, "Net Operating Income Loss")
        
        elif data_category == "10-K Earnings Per Share Basic":
            companyConcept=getData(cik_str, selectToAPI["10-K Earnings Per Share Basic"], stock)
            if companyConcept is not None:
                epsData = jsonToDF(companyConcept, "10-K Earnings Per Share Basic", stock)
                if epsData is not None:
                    eps10K = ten_k_data(epsData)
                    st.dataframe(eps10K)
                    plotGraph(eps10K, "Earnings Per Share Basic")

        elif data_category == "10-K Depreciation":
            companyConcept=getData(cik_str, selectToAPI["10-K Depreciation"], stock)
            if companyConcept is not None:
                depreciationData = jsonToDF(companyConcept, "10-K Depreciation", stock)
                if depreciationData is not None:
                    depreciation10K = ten_k_data(depreciationData)
                    st.dataframe(depreciation10K)
                    plotGraph(depreciation10K, "Depreciation")

        elif data_category == "10-K Earnings Per Share Diluted":
            companyConcept=getData(cik_str, selectToAPI["10-K Earnings Per Share Diluted"], stock)
            if companyConcept is not None:
                epsDilutedData = jsonToDF(companyConcept, "10-K Earnings Per Share Diluted", stock)
                if epsDilutedData is not None:
                    epsDiluted10K = ten_k_data(epsDilutedData)
                    st.dataframe(epsDiluted10K)
                    plotGraph(epsDiluted10K, "Earnings Per Share Diluted")
        
        elif data_category == "10-K Cash":
            companyConcept=getData(cik_str, selectToAPI["10-K Cash"], stock)
            if companyConcept is not None:
                cashData = jsonToDF(companyConcept, "10-K Cash", stock)
                if cashData is not None:
                    cash10K = ten_k_data(cashData)
                    st.dataframe(cash10K)
                    plotGraph(cash10K, "Cash")

