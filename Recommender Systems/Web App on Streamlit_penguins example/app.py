import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

st.title('Welcome to my first streamlit app!')
st.write('**Starting** the *build* of `penguin app` :penguin :smile:')
st.write('Data is taken from [palmerpenguins](https://allisonhorst.github.io/palmerpenguins/)')

st.header('Data')
df = pd.read_csv('penguins_extra.csv')
#st.write('Display a sample of 20 datapoints', df.sample(20))

species = st.selectbox(f'Select species', df.species.unique())
st.write(f'Displaying a sub data from {species}:', df[df['species']==species])


#examples for plotting
fig,ax = plt.subplots()
ax = sns.scatterplot(
    data = df,
    x = 'bill_length_mm',
    y = 'flipper_length_mm',
    hue = 'species' 
)
st.pyplot(fig)

st.bar_chart(df.groupby('island')['species'].count())

st.map(df)

slider_choice = st.sidebar.selectbox('You have the following options', ['yes', 'no'])
if slider_choice == 'yes':
    st.write('yes selected')

else:
    st.write('no selected')

data = st.sidebar.file_uploader('Upload data', type = ['csv'])

if data is not None:
    df = pd.read_csv(data)
    st.write(df)

st.markdown(f"""
<style>
.stApp{{
    background-image: url(https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8cGVuZ3VpbnN8ZW58MHx8MHx8&auto=format&fit=crop&w=800&q=60);
    background-size: cover;
}}
</style>
""",unsafe_allow_html=True)