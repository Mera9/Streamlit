import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
import datetime

st.set_page_config(
    page_title="Аналіз покупок",
    page_icon="📊",
)
st.title('Аналіз покупок у супермаркеті')
name = st.text_input('Як Вас звати?')
if name:
    st.write(f"Вітаємо, {name}!")

DATE_COLUMN = 'Date'
DATA_URL = ('https://docs.google.com/spreadsheets/d/e/2PACX-1vQf1s4z3C0iRAKOu6ClRTZbqN4ocTWoJX5KLynr7iB_ieK2bP5eZXmX7zyHBr9lmLud1ec4Ve71544L/pub?gid=335944704&single=true&output=csv')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done!")

if st.checkbox('Переглянути дані'):
    row_range = st.slider(
        'Оберіть з якого по який рядочки даних ви хочете переглянути',
        0,
        len(data) - 1,
        (1000, 10000)
    )
    selected_data = data.iloc[row_range[0]:row_range[1] + 1]
    st.dataframe(selected_data)
    
show_histograms = st.sidebar.checkbox('Показати гістограми')

selected_histograms = []

if show_histograms:
    selected_histograms = st.sidebar.multiselect(
        'Виберіть показники для гістограм',
        ['Amount', 'Net Bill Amount', 'GST', 'Gross Bill Amount', '% Profit Margin', '% Operating Cost', '% Product Cost', 'Profit Margin', 'Operating Cost', 'Product Cost']
    )

for col in selected_histograms:
    if col in data.columns:
        fig = px.histogram(data, x=col, title=f'Histogram for {col}')
        st.plotly_chart(fig)
           

selected_dynamic_average = st.sidebar.checkbox('Показати середні показники в динаміці за датою')

if selected_dynamic_average:
    
    date_range = st.slider(
        'Оберіть діапазон дат',
        pd.to_datetime(data[DATE_COLUMN]).min().to_pydatetime(),
        pd.to_datetime(data[DATE_COLUMN]).max().to_pydatetime(),
        (datetime.datetime(2016, 1, 1, 0, 0), pd.to_datetime(data[DATE_COLUMN]).max().to_pydatetime())
    )

    start_date, end_date = date_range

    for col in st.sidebar.multiselect(
        'Виберіть показники для графіків',
        ['Amount', 'Net Bill Amount', 'GST', 'Gross Bill Amount', '% Profit Margin', '% Operating Cost', '% Product Cost', 'Profit Margin', 'Operating Cost', 'Product Cost']
    ):
        if col in data.columns:
            filtered_data = data[(pd.to_datetime(data[DATE_COLUMN]) >= start_date) & (pd.to_datetime(data[DATE_COLUMN]) <= end_date)]
            fig = px.line(filtered_data, x=DATE_COLUMN, y=col, title=f'Dynamic Average Plot for {col}')
            st.plotly_chart(fig)