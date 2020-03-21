import sys
import numpy as np
import pandas as pd
import altair as alt
import Utils as utils
import streamlit as st
import pydeck as pdk


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


#crime_type = st.multiselect('Select the list of crimes you\'d like to filter by',
 #                           list(df.category.unique()), list(df.category.unique()))

# Streamlit's integration with DeckGL. 
# DataFrame is easily filtered based on the output from the multiselect
#st.deck_gl_chart(
 #   viewport={
  #      'latitude':df_prov['lat'],
   #     'longitude':df_prov['lon'],
    #    'zoom':12
    #},
    #layers = [{
    #'data': df_prov.totale_casi.to_json(),
    #'type': 'ScatterplotLayer',
    #'radiusScale':0.1,
    #'pickable':True
#}])

dfa = pd.DataFrame(
    df_prov.totale_casi,
    columns=[df_prov.lat, df_prov.lon])



st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=df_prov.lat[3],
         longitude=df_prov.lon[3],
         zoom=5,
         pitch=20,
     ),
     layers=[
         #pdk.Layer(
          #  'HexagonLayer',
        #    data=dfa,
         #   get_position='[lon, lat]',
          #  radius=200,
        #    width_min_pixels=50,
         #  get_color='[255, 147, 0, 150]',
          #  elevation_scale=50,
           # elevation_range=[0, 100000],
    #        #pickable=True,
     #       extruded=True,
      #   ),
         pdk.Layer(
              'ScatterplotLayer',     # Change the `type` positional argument here
              data=dfa,
              get_position=['lon', 'lat'],
              auto_highlight=True,
              width_min_pixels=5,
              get_radius=1000,          # Radius is given in meters
              get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
              pickable=True
              ),
         #pdk.Layer(
          #   'ScatterplotLayer',
           #  data=dfa,
    #         width_min_pixels=5,
     #        get_position='[lon, lat]',
      #       get_color='[2000, 300, 0, 1600]',
       #      get_radius=20000,
        # ),
     ],
 ))




