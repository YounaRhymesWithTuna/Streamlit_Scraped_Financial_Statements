import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import streamlit as st
import numpy as np

st.title('Apple Inc. Finanical Statement Scraping and Analysis Project')
st.write('The following financial statements are Scraped from Yahoo Finance for analysis purposes.' )
st.text('')
st.markdown('<div style="text-align: center;">Note that 0 may indicate missing values.</div>', unsafe_allow_html=True)



header={'User-Agent': 'Mozilla/5.0 '}
statement=['financials','balance-sheet', 'cash-flow']

for page in statement:
    url=f'https://finance.yahoo.com/quote/AAPL/{page}?p=AAPL'
    request=requests.get(url, headers=header)
    soup=BeautifulSoup(request.content, 'lxml')

    names=soup.find_all('div', class_='D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined' )
    title=[name.get('title') for name in names]

    pattern=re.compile("^Ta\(c\) Py\(6px\) Bxz\(bb\)*.")
    numbers_div= soup.find_all('div',class_=pattern)
    number=[num.get_text('span') for num in numbers_div]
    n_list=[]
    for n in number:
        n=n.replace(',','')
        n=n.replace('-','0')
        n_list.append(n)

    if page=='balance-sheet':
        count = 1
        list_2022=[]
        list_2021=[]
        list_2020=[]
        list_2019=[]

        for j in n_list:
            if count % 4 == 0:
                list_2019.append(j)
            elif count % 4 == 1:
                list_2022.append(j)
            elif count % 4 == 2:
                list_2021.append(j)
            else:
                list_2020.append(j)
            count+=1  

        d = {'name':title,  '9/30/2022': list_2022[1:], '9/30/2021':list_2021[1:], '9/30/2020':list_2020[1:], '9/30/2019':list_2019[1:]}
        df_balance_sheet = pd.DataFrame(data=d)
        df_manually_added=pd.DataFrame({'name':['Current Assets','Inventory','Current Liabilities','Retained Earnings'],'9/30/2022':[135405000, 4946000,153982000,-3068000],'9/30/2021':[134836000,6580000,125481000,5562000],'9/30/2020':[143713000,4061000,105392000,14966000],'9/30/2019':[162819000,4106000,105718000,45898000]})
        df_balance_sheet=pd.concat([df_balance_sheet,df_manually_added],ignore_index=True)
        for column in df_balance_sheet[['9/30/2022', '9/30/2021','9/30/2020','9/30/2019']]:
            df_balance_sheet[column] = pd.to_numeric(df_balance_sheet[column], errors='coerce')
        
        print(df_balance_sheet,0)
        st.text('Balance Sheet:')
        st.dataframe(df_balance_sheet,0)
    
    else: 
        count = 1
        list_ttm=[]
        list_2022=[]
        list_2021=[]
        list_2020=[]
        list_2019=[]

        for j in n_list:
            if count % 5 == 0:
                list_2019.append(j)
            elif count % 5 == 1:
                list_ttm.append(j)
            elif count % 5 == 2:
                list_2022.append(j)
            elif count % 5== 3:
                list_2021.append(j)
            else:
                list_2020.append(j)
            count+=1  

        d = {'name':title, 'ttm': list_ttm[1:], '9/30/2022': list_2022[1:], '9/30/2021':list_2021[1:], '9/30/2020':list_2020[1:], '9/30/2019':list_2019[1:]}
        if page=='financials':
            df_income_st = pd.DataFrame(data=d)
            df_manually_added2=pd.DataFrame({'name':['Net Income'],'ttm':[95171000],'9/30/2022':[99803000],'9/30/2021':[94680000],'9/30/2020':[57411000], '9/30/2019':[55256000] })
            df_income_st=pd.concat([df_income_st,df_manually_added2],ignore_index=True)
            for column in df_income_st[['ttm','9/30/2022', '9/30/2021','9/30/2020','9/30/2019']]:
                df_income_st[column] = pd.to_numeric(df_income_st[column], errors='coerce')

            print(df_income_st)
            st.text('Income Statement:')
            st.dataframe(df_income_st)
        else:
            df_cash=pd.DataFrame(data=d)
            for column in df_cash[['ttm','9/30/2022', '9/30/2021','9/30/2020','9/30/2019']]:
                df_cash[column] = pd.to_numeric(df_cash[column], errors='coerce')
                
            print(df_cash)
            st.text('Cash-Flow:')
            st.dataframe(df_cash)


st.title('Financial Statement Analysis: ')


def analyze():
    print('','\n','Financial Statements Analysis:')

    sales_growth= [(df_income_st.at[0,'9/30/2020']/df_income_st.at[0,'9/30/2019'])-1, df_income_st.at[0,'9/30/2021']/df_income_st.at[0,'9/30/2020']-1, (df_income_st.at[0,'9/30/2022']/df_income_st.at[0,'9/30/2021'])-1]
    ebit_growth= [(df_income_st.at[22,'9/30/2020']/df_income_st.at[22,'9/30/2019'])-1, df_income_st.at[22,'9/30/2021']/df_income_st.at[22,'9/30/2020']-1, (df_income_st.at[22,'9/30/2022']/df_income_st.at[22,'9/30/2021'])-1]
    change_COGS=[(df_income_st.at[1,'9/30/2020']/df_income_st.at[1,'9/30/2019'])-1, df_income_st.at[1,'9/30/2021']/df_income_st.at[1,'9/30/2020']-1, (df_income_st.at[1,'9/30/2022']/df_income_st.at[1,'9/30/2021'])-1]
    o_cashflow=[(df_cash.at[0,'9/30/2020']/df_cash.at[0,'9/30/2019'])-1, df_cash.at[0,'9/30/2021']/df_cash.at[0,'9/30/2020']-1, (df_cash.at[0,'9/30/2022']/df_cash.at[0,'9/30/2021'])-1]
    print('Percent Growth of Net Sales: ', np.round(sales_growth,2), '\n', 'Percent Growth of Earnings before Interest, Tax, Depreciation, Amortization: ', np.round(ebit_growth,2), '\n',
            'Percent change for Cost Of Goods Sold: ', np.round(change_COGS,2), '\n', 'Percent growth of operating cash flow: ',np.round(o_cashflow,2), '\n', 'Note: Percent changes seem consistent from 2019 to 2020 and 2021 to 2022. Most prosperous years are from 2020 to 2021. There are no red flags seen.' )
    st.write('Percent Growth of Net Sales: ', np.round(sales_growth,2), '\n', 'Percent Growth of Earnings before Interest, Tax, Depreciation, Amortization: ', np.round(ebit_growth,2), '\n',
            'Percent change for Cost Of Goods Sold: ', np.round(change_COGS,2), '\n', 'Percent growth of operating cash flow: ',np.round(o_cashflow,2), '\n', 'Note: Percent changes seem consistent from 2019 to 2020 and 2021 to 2022. Most prosperous years are from 2020 to 2021. There are no red flags seen.' )

    print('\n','Liquidity (Current) Ratio: ')
    st.write('Liquidity (Current) Ratio:')
    current_ratio=df_balance_sheet.iloc[13,1:]/df_balance_sheet.iloc[15,1:]
    print(current_ratio, '\n', 'Note: Shows short term liquidity growing. > 1 is ideal.' )
    st.write(current_ratio, '\n', 'Note: Shows short term liquidity growing. > 1 is ideal.')

    print('\n','Leverage and Solvency Ratios: ', '\n')
    st.header('Leverage and Solvency Ratios: ')

    debt_ratio=df_balance_sheet.iloc[1,1:]/df_balance_sheet.iloc[0,1:]
    print('Total debt ratio (liability/asset): ', '\n', debt_ratio, '\n', 'Note: Amount of debt for every $1 of asset. We see ratio decreasing, which is a good indicator.','\n')
    st.write('Total debt ratio (liability/asset): ', '\n', debt_ratio, '\n', 'Note: Amount of debt for every $1 of asset. We see ratio decreasing, which is a good indicator.','\n')

    debt_equity_ratio=df_balance_sheet.iloc[9,1:]/df_balance_sheet.iloc[2,1:]
    print('Debt to Equity ratio: ', '\n' ,debt_equity_ratio, '\n', 'Note: Generally, we want this value to be below one. The ratio is decreasing gradually.', '\n')
    st.write('Debt to Equity ratio: ', '\n' ,debt_equity_ratio, '\n', 'Note: Generally, we want this value to be below one. The ratio is decreasing gradually.', '\n')

    tat=df_income_st.iloc[0,1:]/df_balance_sheet.iloc[0,1:]
    print('Total Asset Turnover: ', '\n' ,tat, '\n','Note: Amount of sale for every $1 asset. Efficiency is increasing.', '\n')
    st.write('Total Asset Turnover: ', '\n' ,tat, '\n','Note: Amount of sale for every $1 asset. Efficiency is increasing.', '\n')

    ci_ratio=df_balance_sheet.iloc[0,1:]/df_income_st.iloc[0,1:]
    print('Capital Intensity Ratio: ', '\n' ,ci_ratio, '\n', 'Note: Amount of capital needed to make $1. The ratio is decreasing.' ,'\n')
    st.write('Capital Intensity Ratio: ', '\n' ,ci_ratio, '\n', 'Note: Amount of capital needed to make $1. The ratio is decreasing.' ,'\n')

    print('\n','Asset Utilization Ratio: ', '\n')
    st.header('Asset Utilization Ratio: ')

    inventory_turnover=df_income_st.iloc[1,1:]/df_balance_sheet.iloc[14,1:]
    print('Inventory_turnover: ','\n' ,inventory_turnover, '\n', 'Shows how many times we use up inventory and restock.','\n')
    st.write('Inventory_turnover: ','\n' ,inventory_turnover, '\n', 'Shows how many times we use up inventory and restock.','\n')

    print('Profitability Ratio: ', '\n')
    st.header('Profitability Ratio: ')

    return_on_asset=df_income_st.iloc[30,1:]/df_balance_sheet.iloc[0,1:]
    print('Return on Asset: ','\n' ,return_on_asset, '\n', 'Note: Profit per $1 asset. Profit is increasing.','\n')
    st.write('Return on Asset: ','\n' ,return_on_asset, '\n', 'Note: Profit per $1 asset. Profit is increasing.','\n')

    return_on_equity=return_on_asset*(1+ debt_equity_ratio)
    print('Return on Equity: ','\n' ,return_on_equity, '\n', 'Note: ROE doubled from 2020 to 2021', '/n' )
    st.write('Return on Equity: ','\n' ,return_on_equity, '\n', 'Note: ROE doubled from 2020 to 2021', '/n')

    print('Growth Ratio: ')
    st.header('Growth Ratio: ')
    plowback_ratio= df_balance_sheet.iloc[16,1:]/df_income_st.iloc[30,1:]
    internal_growth_rate=(return_on_asset*plowback_ratio)/((1-return_on_asset)*plowback_ratio)
    print('Internal Growth Rate: ','\n' ,internal_growth_rate, 'Note: Maximum growth possible wihout new debt or new equity.', '\n')
    st.write('Internal Growth Rate: ','\n' ,internal_growth_rate, 'Note: Maximum growth possible wihout new debt or new equity.', '\n')

    sustainable_growth_rate=(return_on_equity*plowback_ratio)/((1-return_on_equity)*plowback_ratio)
    print('Sustainable Growth Rate: ', '\n',sustainable_growth_rate, '\n', 'Note: Maximum growth possible without external financing (new equity) except to keep D/E ratio.')
    st.write('Sustainable Growth Rate: ', '\n',sustainable_growth_rate, '\n', 'Note: Maximum growth possible without external financing (new equity) except to keep D/E ratio.')

analyze()