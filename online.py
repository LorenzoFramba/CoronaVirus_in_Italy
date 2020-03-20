import sys
import numpy as np
import pandas as pd

import Utils as utils
import streamlit as st
import plotly.express as px


st.title('COVID-19 IN ITALIA')


@st.cache



def load_Data(tipo:str):
    if tipo=='regioni':
        data = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv" )
    if tipo=='province':
        data = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv" )
    data["data"] = pd.to_datetime(data["data"]).apply(lambda x: x.date())
    return data   

data_load_state = st.text('Loading data...')

df = load_Data('regioni')

data_load_state.text('Loading data...done!')

if st.checkbox('Guarda i Dati'):
    st.subheader('Raw data')
    st.write(df)


st.subheader('Number of pickups by hour')

hist_values = np.histogram(df.tamponi)
st.bar_chart(hist_values)




values = st.sidebar.slider("deceduti", float(df.deceduti.min()), float(df.deceduti.max()), (200., 700.))
f = px.histogram(df.query(f"deceduti.between{values}"), x="data", nbins=200, title="Deceduti")
f.update_xaxes(title="Price")
f.update_yaxes(title="Deceduti")
st.plotly_chart(f)


cols = ["deceduti", "data", "tamponi"]
st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)


#utils.TotaleValori(True,'Veneto',df,'totale_casi')



