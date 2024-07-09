import requests 
import streamlit as st
import pandas as pd
import altair as alt
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = 'https://3.0.175.195'
def historyPage():
    st.title('History')
    st.markdown('')
    
    endpoint = '/api/history'
    r = requests.get(url + endpoint, verify=False)
    if r.status_code == 200:
        data = r.json()
        balance = 100
        for d in data:
            balance -= d['profit']/d['lot']
    else:
        st.error(f'Error code : {r.status_code}', icon="🚨")
    text = '{:.2f}'.format(balance)
    st.markdown(f'## Balance : {text}')
    df = pd.DataFrame(data)
    # Chart     
    df['create_date'] = pd.to_datetime(df['create_date'])
    df['adjusted_profit'] = df['profit'] * -1
    chart_data = df[['create_date','adjusted_profit']]
    chart_data = chart_data.rename(columns={"create_date": "Date", "adjusted_profit": "Profit"})
    chart = alt.Chart(chart_data).mark_bar().encode(
        x='Date:T',
        y='Profit:Q',
        color=alt.condition(
            alt.datum.Profit > 0,
            alt.value('red'),
            alt.value('green')
        )
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )
    st.markdown('<div class="custom-padding"></div>', unsafe_allow_html=True)
    st.altair_chart(chart,use_container_width=True)

    # DataFrame
    st.markdown('')
    df = df.drop(columns=['id','adjusted_profit'])
    df.columns = ['Date','Symbol','Entry Price','Market Price','Profit','Lot']
    df = df.reindex(columns=['Symbol','Entry Price','Market Price','Profit','Lot','Date'])
    st.dataframe(df, height=800,width=800,on_select="ignore")

def focusPage():
    st.title('Focus')
    st.markdown('')
    endpoint = '/api/focus'
    r = requests.get(url + endpoint, verify=False)
    if r.status_code == 200:
        data = r.json()
    else:
        st.error(f'Error code : {r.status_code}', icon="🚨")

    df = pd.DataFrame(data)
    df = df.drop(columns=['id'])
    df.columns = ['Symbol','Change(%)']
    st.dataframe(df,width=800,on_select="ignore")


def ordersPage():
    st.title('Orders')
    st.markdown('')
    endpoint = '/api/orders'
    r = requests.get(url + endpoint, verify=False)
    if r.status_code == 200:
        data = r.json()
    else:
        st.error(f'Error code : {r.status_code}', icon="🚨")
    
    df = pd.DataFrame(data)
    df = df.drop(columns=['id'])
    df.columns = ['Symbol','Type','Entry Price','Stoploss','Takeprofit']
    st.dataframe(df,width=800,on_select="ignore")

st.sidebar.title('Aximorph API')
page = st.sidebar.radio("Go to", ("Focus", "Orders", "History"))

if page == "History":
    historyPage()
elif page == "Focus":
    focusPage()
elif page == "Orders":
    ordersPage()