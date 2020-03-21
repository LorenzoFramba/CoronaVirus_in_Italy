import sys
import numpy as np
import pandas as pd
import altair as alt
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
df_prov = load_Data('province')
df_prov = df_prov[(df_prov[['lat','long']] != 0).all(axis=1)]



data_load_state.text('Loading data...done!')


if st.checkbox('Guarda i Dati'):
    st.subheader('Raw data')
    st.write(df)
    st.write(df_prov)

regioni=utils.getLocations(df, True)
province=utils.getLocations(df_prov, False)

###########################################################################


st.subheader('Dati nel Complesso per Provincia')

province_selezionate = st.multiselect("Province", province, province[:5])  
alt_plot_prov = utils.altair_scatter(df_prov.loc[df_prov['denominazione_provincia'].isin(province_selezionate)], "data", "totale_casi","denominazione_provincia" )

st.altair_chart(alt_plot_prov)

###########################################################################

st.subheader('Dati nel Complesso per Regione')


regioni_selezionate = st.multiselect("Regioni", regioni, regioni[:5])  
azione = st.selectbox("Azione",utils.azioni,format_func=utils.cols.get)


alt_plot = utils.altair_scatter(df.loc[df['denominazione_regione'].isin(regioni_selezionate)], "data", azione,"denominazione_regione" )

st.altair_chart(alt_plot)

###########################################################################




selection = alt.selection_multi(fields=['year'])



[]




test = st.selectbox("AZIONE",regioni)


st.line_chart(regioni_selezionate)


cols = ["deceduti", "data", "tamponi"]
regioni_selezionate = st.multiselect("Columns", df.columns.tolist(), default=cols)


values = st.slider("deceduti", float(df.deceduti.min()), float(df.deceduti.max()), (200., 700.))
f = px.histogram(df.query(f"deceduti.between{values}"), x="data", nbins=200, title="Deceduti")
f.update_xaxes(title="Price")
f.update_yaxes(title="Deceduti")
st.plotly_chart(f)





#utils.TotaleValori(True,'Veneto',df,'totale_casi')



