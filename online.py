import sys
import numpy as np
import pandas as pd
import altair as alt
import Utils as utils
import streamlit as st
import pydeck as pdk
import datetime
from datetime import datetime as dt


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

st.sidebar.markdown(
    ("Tutti i codici Open Source possono essere trovati qua  ")
    + "[GitHub](https://github.com/LorenzoFramba/CoronaVirus_in_Italy)."
)


st.sidebar.markdown(
    ("Questo sito è frutto di lavoro individuale e autosostenuto. Se hai la possibilità di fare una donazione, lo apprezzerei tantissimo!  ")
    + "[PayPal](paypal.me/rappasta)."
)


st.success(
    ("Questo sito è frutto di lavoro individuale e autosostenuto. Se hai la possibilità di fare una donazione, lo apprezzerei tantissimo!  ")
    + "[PayPal](paypal.me/rappasta)."
)


st.markdown(
    (  "Tutti i dati visualizzati in questo sito provengono dal Ministero della Salute, elaborati dal Dipartimento di Protezione Civile. "
        "I loro dati sono visualizzabili [COVID-19 Italia - Monitoraggio situazione](https://github.com/pcm-dpc/COVID-19) su licenza "
        "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
        "I DATI SONO SEMPRE AGGIORNATI IN TEMPO REALE ALLE 18 DI OGNI GIORNO. "
    )
)


regioni=utils.getLocations(df, True)
province=utils.getLocations(df_prov, False)

###########################################################################



st.subheader('Dati nel Complesso per Regione')


regioni_selezionate = st.multiselect("Regioni", regioni, regioni[:5])  
azione = st.selectbox("Azione",utils.azioni,format_func=utils.cols.get)


alt_plot = utils.altair_scatter(df.loc[df['denominazione_regione'].isin(regioni_selezionate)], "data", azione,"denominazione_regione" )

st.altair_chart(alt_plot)




###########################################################################




st.subheader('Dati nel Complesso per Provincia')

province_selezionate = st.multiselect("Province", province, province[:5])  
alt_plot_prov = utils.altair_scatter(df_prov.loc[df_prov['denominazione_provincia'].isin(province_selezionate)], "data", "totale_casi","denominazione_provincia" )

st.altair_chart(alt_plot_prov)

###########################################################################




#


today = datetime.date.today()- datetime.timedelta(days=1) #
inizio = datetime.date(2020, 2, 24)


#data_scelta = st.slider(f"Seleziona giornata da analizzare tra {today} e {inizio}", inizio, today, today)


st.success(
    ("Questo sito è frutto di lavoro individuale e autosostenuto. Se hai la possibilità di fare una donazione, lo apprezzerei tantissimo!  ")
    + "[PayPal](paypal.me/rappasta)."
)


chosen_date = st.date_input(f"Seleziona giornata da analizzare tra {inizio} e {today}", today)
if  chosen_date > inizio  and chosen_date <= (today):
    filtered_data = df_prov[df_prov["data"] == chosen_date]
    df,prov = utils.filtra(filtered_data)
    prov=prov.reset_index()
    province_da_visualizzare = st.slider('Province piú infette da Visualizzare', 3, 15, 5)
    
    st.altair_chart(utils.altair_chart(prov.head(province_da_visualizzare), "Provincia", "Casi" ))
    
    
    #st.dataframe(prov[:province_da_visualizzare])
    st.pydeck_chart(utils.crea_mappa(df))
else:
    st.error( f"Selezionare un giorno compreso tra {inizio} e {today} ")









