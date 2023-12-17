import pandas as pd 
import streamlit as st 
from st_pages import add_page_title

st.title("SF Trees Data Quality App")
st.write(
	"""
	This app is a data quality tool for the SF Trees Dataset. Edit the data and save to a new file!
	""")

trees_df = pd.read_csv('trees.csv')
trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df_filtered = trees_df[trees_df["legal_status"]=="Private"]
st.dataframe(trees_df)




