import sys
import numpy as np
import pandas as pd
import altair as alt
import Utils as utils
import streamlit as st
from vega_datasets import data
import pydeck as pdk
import datetime



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

df.rename(columns={'long':'lon'},  inplace=True)
df_prov.rename(columns={'long':'lon'},  inplace=True)



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


#day_to_filter = st.slider('day', df_prov["data"].min, df_prov["data"].max, df_prov["data"].min)


#filtered_data = df_prov[df_prov["data"].dt.hour == day_to_filter]



st.subheader('CASI PER PROVINCIA')



dfa = pd.DataFrame(
    df_prov,
    columns=[df_prov.lat, df_prov.lon])


filtered_data = df_prov
filtered_data["days_passed"] = filtered_data["data"].apply(
        lambda x: (x - datetime.date(2020, 2, 24)).days)
n_days = filtered_data["days_passed"].unique().shape[0] - 1

st.markdown(
        "Scegli che data visualizzare come numero di giorni dalla prima raccolta dati, il 24 febbraio:"
)
chosen_n_days = st.slider("Giorni:", min_value=0, max_value=n_days, value=n_days,)
st.markdown(
        f"Data scelta: {datetime.date(2020, 2, 24) + datetime.timedelta(days=chosen_n_days)}"
)
filtered_data = df_prov[df_prov["days_passed"] == chosen_n_days]

zeri =[]
for i,val in filtered_data.iterrows():
    if val.totale_casi!=0:
        for index in range((val.totale_casi)):
            zeri.append([val.lat,val.lon])
            
df = pd.DataFrame(zeri) 
df.rename(columns={1:'lon',
                          0:'lat'}, 
                 inplace=True)


#filtered_data.drop(['data', 'stato','codice_regione','denominazione_regione','denominazione_provincia','codice_provincia','sigla_provincia','totale_casi','days_passed'], axis = 1, inplace=True)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=41.902782,
         longitude=12.496366,
         zoom=4.5,
         get_radius=1000,
         pitch=20,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=1000,
            elevation_scale=50,
            elevation_range=[0, 3000],
            #pickable=True,
            extruded=True,
            coverage=10,
         ),
     ],
 ))

#st.pydeck_chart(pdk.Deck(




