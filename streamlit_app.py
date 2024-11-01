import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from PIL import Image

st.title(""" :rainbow[Real_Time_Stock_market]""")
# st.image('stock copy.jpg',width=500,channels='RGB')
st.sidebar.title(""" :rainbow[Please provied the following]""")
ticker_symbol=st.sidebar._selectbox('enter the ticker:',['AAPL','F','MSFT','SBI','GOOG','TSLA','UBER','SNAP','LCID','T','INTC','SOFI'])                
start_date=st.sidebar.date_input("start_date",value=None)
end_date=st.sidebar.date_input("end_date",value=None)

ticker=yf.Ticker(ticker_symbol)
historical_data=ticker.history(start=start_date,end=end_date)
if start_date is not None and end_date is not None:
    stockdata=yf.download(ticker_symbol,start=start_date,end=end_date)

price_tab,chart_tab,hist,fund,news=st.tabs(['Price Movement','Charts','Historical Data','Fundamental','TOP10 NEWS'])
with price_tab:
    st.write(f""" :rainbow[Price Movement {ticker_symbol}]""")
    st.write(stockdata)
    csv=stockdata.to_csv().encode('utf-8')
    st.download_button(label=""" :rainbow[Download CSV]""",data=csv,file_name=f"{ticker_symbol}_Pricedata.csv",mime='text/csv')
with hist:
    st.write(f""" :rainbow[Historical Data {ticker_symbol}]""")
    st.write(historical_data)
    csv=historical_data.to_csv().encode('utf-8')
    st.download_button(label=""":rainbow[Download CSV]""",data=csv,file_name=f"{ticker_symbol}_historicaldata.csv",mime='text/csv')
with chart_tab:
    historical_data['50-DAY']=historical_data['Close'].rolling(window=50).mean()
    historical_data['200-DAY']=historical_data['Close'].rolling(window=200).mean()
    st.subheader(f""" :rainbow[Line chart {ticker_symbol}]""")
    st.line_chart(historical_data[['Close','50-DAY','200-DAY']])
    st.subheader(f""" :rainbow[Area chart  {ticker_symbol}]""")
    st.area_chart(historical_data[['Close','50-DAY','200-DAY']])

from alpha_vantage.fundamentaldata import FundamentalData
with fund:
    key='AW9L6GL4UWRNBQIL'
    fd=FundamentalData(key,output_format='pandas')
    st.subheader(""" :rainbow[BALANCE SHEET]""")
    balance_sheet=fd.get_balance_sheet_annual(ticker_symbol)[0]
    bs=balance_sheet.T[2:]
    bs.columns=list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader(""" :rainbow[INCOME STATEMENT]""")
    income_statement=fd.get_income_statement_annual(ticker_symbol)[0]
    is1=income_statement.T[2:]
    is1.columns=list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader(""" :rainbow[CASH FLOW STATEMENT]""")
    cash_flow=fd.get_cash_flow_annual(ticker_symbol)[0]
    cf=cash_flow.T[2:]
    cf.columns=list(cash_flow.T.iloc[0])
    st.write(cf)

from stocknews import StockNews
with news: 
    st.header(f""" :rainbow[NEWS OF {ticker}]""")
    sn=StockNews(ticker_symbol,save_news=False)
    df_news=sn.read_rss()
    for i in range(10):
        st.subheader(f'NEWS{i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment=df_news['sentiment_title'][i]
        st.write(f'Title sentiment{title_sentiment}')
        news_sentiment=df_news['sentiment_summary'][i]
        st.write(f'News sentiment{news_sentiment}')




