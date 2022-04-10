import pandas as pd
from datetime import datetime
import altair as alt
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cycler
from pandas.plotting import register_matplotlib_converters





alpha = 44.26 #coefficient de normalisation

covid = pd.read_csv('covid_latest.csv', sep= ';', usecols=['date','vac_statut','nb_PCR+','nb_PCR+_sympt','HC','SC'])


covid['date'] = covid['date'].apply( lambda date : datetime.strptime(date, "%Y-%m-%d") )







# creation of 2 categories : vaccinated, non-vaccinated
covid['vac_statut'] = covid['vac_statut'].replace(['Non-vaccinés','Primo dose récente'],'vaccinés' )

covid['vac_statut'] = covid['vac_statut'].replace(['Complet de moins de 3 mois - avec rappel',
                                                'Complet entre 3 mois et 6 mois - sans rappel',
                                                'Complet de moins de 3 mois - sans rappel', 'Primo dose efficace',
                                                'Complet entre 3 mois et 6 mois - avec rappel',
                                                'Complet de 6 mois et plus - sans rappel',
                                                'Complet de 6 mois et plus - avec rappel'],'non-vaccinés' )







covid = covid.groupby(['date','vac_statut']).sum().reset_index()

covid = covid.sort_values(by=["date"],ascending=True )

covid= covid.set_index('date')

start_date = st.sidebar.date_input('Start date',value = min(covid.index), min_value= min(covid.index),  max_value=max(covid.index))

st.sidebar.success(f'Start date from :  {start_date}')

covid = covid.loc[start_date:]

norr = st.sidebar.checkbox('Normalize the data ?')

if norr:

    covid.iloc[:,1:] = covid.iloc[:,1:].apply(lambda x : x/ alpha)


smooth = st.sidebar.checkbox('smooth it ? ')

if smooth:

    covid.iloc[:,1:] = covid.iloc[:,1:].rolling(7).mean()






nn_vac = covid[covid['vac_statut']=='non-vaccinés']

vac = covid[covid['vac_statut']=='vaccinés']

nn_vac.drop(columns=['vac_statut'],inplace = True)

vac.drop(columns=['vac_statut'],inplace = True)

st.title('Covid Cases tracking in France')




date_axe = sorted(list(vac.index))


graph_letter = st.sidebar.selectbox(
    "what graph would you like to visualize?",
    ("a","b","c","d")
)



if graph_letter == 'a':
    chart_nn_vac = alt.Chart(nn_vac.reset_index(),title="'Nombre de Test+'").mark_line(color = 'red').encode( x='date', y='nb_PCR+')

    
    chart_vac = alt.Chart(vac.reset_index()).mark_line( color = 'blue').encode( x='date', y='nb_PCR+')


    st.altair_chart(chart_nn_vac+chart_vac, use_container_width=True)

if graph_letter == 'b':
    chart_nn_vac = alt.Chart(nn_vac.reset_index(),title='nb_PCR+_sympt').mark_line(color = 'red').encode( x='date', y='nb_PCR+_sympt')

    
    chart_vac = alt.Chart(vac.reset_index()).mark_line( color = 'blue').encode( x='date', y='nb_PCR+_sympt')


    st.altair_chart(chart_nn_vac+chart_vac, use_container_width=True)

if graph_letter == 'c':
    chart_nn_vac = alt.Chart(nn_vac.reset_index(),title='Hospitalisation').mark_line(color = 'red').encode( x='date', y='HC')

    
    chart_vac = alt.Chart(vac.reset_index()).mark_line( color = 'blue').encode( x='date', y='HC')


    st.altair_chart(chart_nn_vac+chart_vac, use_container_width=True)


if graph_letter == 'd':
    chart_nn_vac = alt.Chart(nn_vac.reset_index(),title='Entrées en soins critiques').mark_line(color = 'red').encode( x='date', y='SC')

    
    chart_vac = alt.Chart(vac.reset_index()).mark_line( color = 'blue').encode( x='date', y='SC')


    st.altair_chart(chart_nn_vac+chart_vac, use_container_width=True)



st.write('rouge = non vaccinées')
st.write('bleu = vaccinées')





    

        









