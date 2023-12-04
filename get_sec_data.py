import requests
from env import headers
import pandas as pd
from input_to_req import selectToAPI, new_no_data_dict 
import streamlit as st 

# function to get the type of data
@st.cache_data 
def getData(cik_str, data_str, stock):
    try:
        data_result = requests.get(
            (
            f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_str}'
            f'/us-gaap/{data_str}.json'
            ),
            headers=headers 
        )
        if data_result.status_code == 404:
            raise Exception("No current data available")
        return data_result
    except Exception as e:    
        st.text(f"{stock} currently has no {data_str} data")
        if data_str not in new_no_data_dict:
            new_no_data_dict[data_str] = []
            new_no_data_dict[data_str].append(stock)
        else:
            if stock not in new_no_data_dict[data_str]:
                new_no_data_dict[data_str].append(stock)
        # st.write(new_no_data_dict) 

# function to convert json data to dataframe
@st.cache_data 
def jsonToDF(_json_data, data_str, stock):
    try:    
        if data_str in ["EarningsPerShareBasic", "EarningsPerShareDiluted", "10-K Earnings Per Share Basic", "10-K Earnings Per Share Diluted"]:
            df_data = pd.DataFrame.from_dict(
                (_json_data.json()['units']['USD/shares'])
            )
        else:
            df_data = pd.DataFrame.from_dict(
                (_json_data.json()['units']['USD'])
            )
        #st.write("Result after json to DF is: ", type(df_data))
        #st.write(df_data)
        return df_data
    except:
        st.text(f"Error parsing {stock} json") 

# function to get 10-k data from df data
@st.cache_data
def ten_k_data(df_data):
    df_data = df_data[df_data.form=='10-K']
    df_data = df_data.reset_index(drop=True)
    return df_data

# get ten k data for all top 10 companies
@st.cache_data 
def data_top(cik_dict, input_data_str):
    latest_top_dict = {"stock":[],"latest_value":[],"filed_date":[]}
    data_str = selectToAPI[input_data_str]
    for stock in cik_dict:
        cik_str = cik_dict[stock][2]
        data_result = getData(cik_str, data_str, stock)
        # st.write(data_result)
        # if data_result is not None:
        if data_result is None:
            continue
        df_data = jsonToDF(data_result, data_str, stock)
        if df_data is None:
            continue
        
        #st.write("The df_data from jsonToDF is: ", type(df_data))
        # st.write(df_data)
        ten_k_result = ten_k_data(df_data)
        # st.write("ten_k_result is: ", type(ten_k_result))

        if ten_k_result is not None:
            try:
            # get the latest eps basic data for each company (last row)
                latest_data = ten_k_result.iloc[-1]
            except:
                st.text(f"Getting {stock} ten k result has out of bound error")
                continue 
            #st.write("latest_data is: ", type(latest_data))
        # latest_top[stock] = [latest_data.filed, latest_data.val]
        latest_top_dict["stock"].append(stock) 
        latest_top_dict["latest_value"].append(latest_data.val) 
        latest_top_dict["filed_date"].append(latest_data.filed) 

   
    latest_top_df = pd.DataFrame.from_dict(latest_top_dict) 
    latest_top_df_sorted = latest_top_df.sort_values(by="latest_value", ascending=False)
   # st.write(latest_top_df_sorted)
    latest_top_df_sorted = latest_top_df_sorted.reset_index(drop=True)
    #st.write(latest_top_df_sorted)

    # st.write(latest_top_df)

    st.write(f"**{len(latest_top_df_sorted)} valid records for this metric is returned.**")    
    return latest_top_df_sorted