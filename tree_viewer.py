import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from st_pages import Page, show_pages, add_page_title

add_page_title()

show_pages(
	[
		Page("tree_viewer.py", "Tree Explorer"),
		Page("pages/pretty_trees.py", "San Francisco Trees"),
		Page("pages/data_quality.py", "SF Tree Dataset Data Quality")
	]
)

st.set_page_config(layout='wide')
st.title("Tree Viewer")
st.write(
	"""
	This app analyzes trees in the selected city using a dataset kindly provided by McCoy et. al. (https://datadryad.org/stash/dataset/doi:10.5061/dryad.2jm63xsrf). Select a city to get started.
	""")

cities = os.listdir('./data')
cities = [city.split('.')[0] for city in cities]

selected_city = st.sidebar.selectbox("City", cities, placeholder='Choose A City', index=None)

if not selected_city:
	st.stop()

tree_path = os.path.join('data', selected_city+'.csv')
df = pd.read_csv(tree_path)

sp_col = 'common_name'
species = df[sp_col].unique()
if len(species)<=1 and np.all(np.isnan(species)):
	sp_col = 'scientific_name'
	species = df[sp_col].unique()

select_species = st.sidebar.multiselect("Species", species)

if select_species:
	trees_df = df[df[sp_col].isin(select_species)]
else:
	trees_df = df

tab1, tab2, tab3 = st.tabs(['Tree Map', 'Species Count', 'Tree Condition'])

with tab1:
	coordinates = trees_df.dropna(subset=['longitude_coordinate', 'latitude_coordinate'])
	coordinates = coordinates.rename(columns={'longitude_coordinate': 'longitude',
										  'latitude_coordinate': 'latitude'})
	if len(coordinates)>0:
		coordinates = coordinates.sample(
			n=int(.1*len(trees_df)), replace=True)
		st.map(coordinates, use_container_width=True)
	else:
		st.write('This dataset does not contain latitude and longitude information.')

sp_count = df.groupby(sp_col).count().iloc[:,0]

with tab2:
	fig = px.bar(sp_count)
	fig.update_xaxes(title_text='Name', categoryorder='total descending')
	fig.update_yaxes(title_text='Count')
	fig.update_layout(showlegend=False)
	st.plotly_chart(fig, use_container_width=True)

conditions = df['condition'].isna().all()

with tab3:
	if conditions:
		st.write('This dataset does not contain information about tree conditions.')
	else:
		cond = df.groupby('condition').count().iloc[:,0]
		fig = px.bar(cond)
		fig.update_xaxes(title_text='Condition')
		fig.update_yaxes(title_text='Count')
		fig.update_layout(showlegend=False)
		st.plotly_chart(fig, use_container_width=True)



