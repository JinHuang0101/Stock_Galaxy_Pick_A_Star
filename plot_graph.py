import streamlit as st 
import matplotlib.pyplot as plt

# function to plot graph
@st.cache_data 
def plotGraph(curr_df, df_name):
    thisPlot = curr_df.plot(x='end', y='val', title = f'{df_name} Reported in 10-K', color = 'lime')
    thisPlot.set_xlabel("Report Date")
    thisPlot.set_ylabel(f'{df_name}')
    thisPlot.grid(axis = 'x')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt.gcf())

@st.cache_data
def plotBar(curr_df):
    # st.write(curr_df)
    # st.write(len(curr_df))
    x_array = []
    y_array = []
    for i in range(len(curr_df)):
        for key, value in curr_df.items():
            x_array.append(key)
            y_array.append(value[0])
    # st.write(x_array)
    # st.write(y_array)
    x = x_array
    y = y_array
    thisPlot = plt.bar(x, y, color = 'lime')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt.gcf())