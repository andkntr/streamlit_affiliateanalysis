import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from datetime import date, datetime,timedelta
import plotly.express as px
import matplotlib as plt
import altair as alt

st.set_page_config(page_title='MT分析ダッシュボード',layout='wide')

#使ってない関数
@st.cache
def conn_db(dp):
    dbpath = dp
    conn = sqlite3.connect(dbpath)
    df = pd.read_sql_query('SELECT * FROM affiliate_data',conn)
    print(df.head())
    cursor.close()
    conn.close()
    return print(df.head())





dbpath = '/Users/Ken/affiliates_data.db'
conn = sqlite3.connect(dbpath)
df=pd.read_sql_query('SELECT Date,Tier1AffiliateID,MerchantID,ProductName,Quantity,UnitPrice,Commission,TotalOrderValue,CampaignName,BannerName,FirstReferer FROM affiliate_data',conn)
conn.close()

df['Date']=pd.to_datetime(df['Date'],format='%Y/%m/%d')


df_2021 = df[(df['Date']>='2021/1/1')&(df['Date']<'2022/1/1')]
df_2022 = df[(df['Date']>='2022/1/1')&(df['Date']<'2023/1/1')]

st.title('アフィリエイト分析ダッシュボード')
#1ヶ月の合計報酬金額＆前月比
#--------日付指定----------
starting_date = st.date_input('開始日')
closing_date = st.date_input('終了日')

#--------比較用日付指定----------
datedelta = abs(starting_date-closing_date) #日数の差を計算
datedelta = datedelta.days+1 #+1しないと比較用と1日かぶる
compare_starting_date=starting_date-timedelta(days=datedelta) #比較用開始日
compare_closing_date=closing_date-timedelta(days = datedelta) #比較用終了日

#--------指定した日付期間をデータフレーム化--------
starting_date = datetime.strptime(str(starting_date), "%Y-%m-%d").strftime("%Y/%m/%-d")
closing_date = datetime.strptime(str(closing_date), "%Y-%m-%d").strftime("%Y/%m/%-d")
df1 = df[(df['Date']>=str(starting_date))&(df['Date']<=str(closing_date))]

#指定した日付期間分過去のデータフレーム（比較用）
compare_starting_date = datetime.strptime(str(compare_starting_date), "%Y-%m-%d").strftime("%Y/%m/%-d")
compare_closing_date = datetime.strptime(str(compare_closing_date), "%Y-%m-%d").strftime("%Y/%m/%-d")
df_comparison = df[(df['Date']>=str(compare_starting_date))&(df['Date']<=str(compare_closing_date))]



#--------総売上----------
total_sales=df1['TotalOrderValue'].sum()
total_sales2 = "{:,}".format(total_sales)

#比較用
comparison_total_sales=df_comparison['TotalOrderValue'].sum()
sales_delta = ((total_sales-comparison_total_sales)/comparison_total_sales)*100

#--------総報酬----------
total_com=df1['Commission'].sum()
total_com2 = "{:,}".format(total_com)


comparison_total_com=df_comparison['Commission'].sum()
commission_delta = ((total_com-comparison_total_com)/comparison_total_com)*100

#--------成果数----------
sales_count = len(df1)
comparison_count=len(df_comparison)
count_delta = ((sales_count-comparison_count)/comparison_count)*100

#--------KIRYOKU総売上----------
kiryoku_sales = df1[(df1['MerchantID']=='bestkenko')|(df1['MerchantID']=='kusuriexpress')|(df1['MerchantID']=='petkusuri')|(df1['MerchantID']=='unidru')]#MerchantIDがKIRYOKUサイトのもののみを抽出
kiryoku_sales=kiryoku_sales['TotalOrderValue'].sum()


#比較用
comparison_kiryoku_sales=df_comparison[(df_comparison['MerchantID']=='bestkenko')|(df_comparison['MerchantID']=='kusuriexpress')|(df_comparison['MerchantID']=='petkusuri')|(df_comparison['MerchantID']=='unidru')]
comparison_kiryoku_sales=comparison_kiryoku_sales['TotalOrderValue'].sum()
kiryoku_sales_delta = ((kiryoku_sales-comparison_kiryoku_sales)/comparison_kiryoku_sales)*100

kiryoku_sales2="{:,}".format(kiryoku_sales)

#--------KIRYOKU総報酬----------
kiryoku_com = df1[(df1['MerchantID']=='bestkenko')|(df1['MerchantID']=='kusuriexpress')|(df1['MerchantID']=='petkusuri')|(df1['MerchantID']=='unidru')]#MerchantIDがKIRYOKUサイトのもののみを抽出
kiryoku_com=kiryoku_com['Commission'].sum()


#比較用
comparison_kiryoku_com=df_comparison[(df_comparison['MerchantID']=='bestkenko')|(df_comparison['MerchantID']=='kusuriexpress')|(df_comparison['MerchantID']=='petkusuri')|(df_comparison['MerchantID']=='unidru')]
comparison_kiryoku_com=comparison_kiryoku_com['Commission'].sum()
kiryoku_com_delta = ((kiryoku_com-comparison_kiryoku_com)/comparison_kiryoku_com)*100

kiryoku_com2="{:,}".format(kiryoku_com)

#--------KIRYOKU成果数----------
kiryoku_sales_count =df1[(df1['MerchantID']=='bestkenko')|(df1['MerchantID']=='kusuriexpress')|(df1['MerchantID']=='petkusuri')|(df1['MerchantID']=='unidru')]
kiryoku_sales_count = len(kiryoku_sales_count)
kiryoku_comparison_count=df_comparison[(df_comparison['MerchantID']=='bestkenko')|(df_comparison['MerchantID']=='kusuriexpress')|(df_comparison['MerchantID']=='petkusuri')|(df_comparison['MerchantID']=='unidru')]
kiryoku_comparison_count=len(kiryoku_comparison_count)
kiryoku_count_delta = ((kiryoku_sales_count-kiryoku_comparison_count)/kiryoku_comparison_count)*100

#--------Merchant総売上----------
merchant_sales = total_sales-kiryoku_sales
merchant_sales2 = "{:,}".format(merchant_sales)
merchant_com = total_com-kiryoku_com
merchant_com2 = "{:,}".format(merchant_com)
merchant_count = sales_count - kiryoku_sales_count
#比較用
comparison_merchant_sales = comparison_total_sales - comparison_kiryoku_sales
comparison_merchant_com = comparison_total_com - comparison_kiryoku_com
comparison_merchant_count = comparison_count - kiryoku_comparison_count

merchant_sales_delta = ((merchant_sales - comparison_merchant_sales)/comparison_merchant_sales)*100
merchant_com_delta = ((merchant_com - comparison_merchant_com)/comparison_merchant_com)*100
merchant_count_delta = ((merchant_count - comparison_merchant_count)/comparison_merchant_count)*100


#--------全体メトリック表示----------
col1, col2, col3 = st.columns(3)
col1.metric("総販売価格", total_sales2, str(round(sales_delta))+'%',help='過去同期間との差%')
col2.metric("総報酬", total_com2, str(round(commission_delta))+'%',help='過去同期間との差%')
col3.metric("成果数",sales_count, str(round(commission_delta))+'%',help='過去同期間との差%')

#--------KIRYOKUメトリック表示----------
###KIRYOKU
col1, col2, col3 = st.columns(3)
col1.metric("KIRYOKU販売価格", kiryoku_sales2, str(round(kiryoku_sales_delta))+'%',help='過去同期間との差%')
col2.metric("KIRYOKU報酬", kiryoku_com2, str(round(kiryoku_com_delta))+'%',help='過去同期間との差%')
col3.metric("KIRYOKU成果数",kiryoku_sales_count, str(round(kiryoku_count_delta))+'%',help='過去同期間との差%')

#--------Merchantメトリック表示----------
####その他広告主
col1, col2, col3 = st.columns(3)
col1.metric("その他広告主販売価格", merchant_sales2, str(round(merchant_sales_delta))+'%',help='過去同期間との差%')
col2.metric("その他広告主報酬", merchant_com2, str(round(merchant_com_delta))+'%',help='過去同期間との差%')
col3.metric("その他広告主成果数",merchant_count, str(round(merchant_count_delta))+'%',help='過去同期間との差%')

#--------広告主売上棒グラフ----------
df_barchart = pd.pivot_table(df1,values='Commission',index='MerchantID',aggfunc=np.sum)
df_barchart = df_barchart.sort_values('Commission',ascending=False)#合計報酬の高い順にソート

st.bar_chart(df_barchart)

#--------広告主ごと売上（日付別）----------
mer_list = df1['MerchantID'].unique()
mer_list = np.insert(mer_list,0,'All')
selected_mer = st.selectbox('広告主ID',mer_list)
if selected_mer == 'All':
    df_merchant_by_date = df1
    df_merchant_by_date['Date']=df1['Date'].dt.strftime('%Y/%m/%d')
    df_merchant_by_date=pd.pivot_table(df_merchant_by_date,values='Commission',index='MerchantID',columns='Date',aggfunc=np.sum,fill_value=0,margins=True,margins_name='TOTAL')
    #df_affiliate_by_date=df_affiliate_by_date.applymap('{:,.0f}'.format)
    df_merchant_by_date = df_merchant_by_date.sort_values('TOTAL',ascending=False)
    st.dataframe(df_merchant_by_date)

else:
    df_merchant_by_date = df1[df1['MerchantID']==selected_mer]
    df_merchant_by_date['Date']=df1['Date'].dt.strftime('%Y/%m/%d')
    by1 = st.radio(' ',('アフィリエイター別','商品別'))
    if by1 == 'アフィリエイター別':
        df_merchant_by_date=pd.pivot_table(df_merchant_by_date,values='Commission',index='Tier1AffiliateID',columns='Date',aggfunc=np.sum,fill_value=0,margins=True,margins_name='TOTAL')
    else:
        df_merchant_by_date=pd.pivot_table(df_merchant_by_date,values='Commission',index='ProductName',columns='Date',aggfunc=np.sum,fill_value=0,margins=True,margins_name='TOTAL')
    #df_affiliate_by_date=df_affiliate_by_date.applymap('{:,.0f}'.format)
    df_merchant_by_date = df_merchant_by_date.sort_values('TOTAL',ascending=False)
    st.dataframe(df_merchant_by_date)





#--------AFごとの売上（日付別）----------
af_list = df1['Tier1AffiliateID'].unique()
af_list = np.insert(af_list,0,'All')
selected_af = st.selectbox('アフィリエイターID',af_list)
if selected_af == 'All':
    df_affiliate_by_date = df1
    #df_merchant_by_date['Date']=df1['Date'].dt.strftime('%Y/%m/%d')
    df_affiliate_by_date=pd.pivot_table(df_affiliate_by_date,values='Commission',index='Tier1AffiliateID',columns='Date',aggfunc=np.sum,fill_value=0,margins=True,margins_name='TOTAL')
    #df_affiliate_by_date=df_affiliate_by_date.applymap('{:,.0f}'.format)
    df_affiliate_by_date = df_affiliate_by_date.sort_values('TOTAL',ascending=False)
    st.dataframe(df_affiliate_by_date)
    st.line_chart(df_affiliate_by_date)
else:
    df_affiliate_by_date = df1[df1['Tier1AffiliateID']==selected_af]
    #df_merchant_by_date['Date']=df1['Date'].dt.strftime('%Y/%m/%d')
    by2 = st.radio(' ',('広告主別','商品別'))
    if by2 == '広告主別':
        df_affiliate_by_date=pd.pivot_table(df_affiliate_by_date,values='Commission',index='MerchantID',columns='Date',aggfunc=np.sum,fill_value=0,margins=True,margins_name='TOTAL')
        st.line_chart(df_affiliate_by_date)
    #df_affiliate_by_date=df_affiliate_by_date.applymap('{:,.0f}'.format)
    else:
        df_affiliate_by_date=pd.pivot_table(df_affiliate_by_date,values='Commission',index='ProductName',columns='Date',aggfunc=np.sum,fill_value=0,margins=True,margins_name='TOTAL')
    df_affiliate_by_date = df_affiliate_by_date.sort_values('TOTAL',ascending=False)
    st.dataframe(df_affiliate_by_date)




#df_affiliate_by_date=pd.pivot_table(df_affiliate_by_date,values='Commission',index='Tier1AffiliateID',columns='Date',aggfunc=np.sum,fill_value=0,margins=True,margins_name='TOTAL')
#df_affiliate_by_date=df_affiliate_by_date.applymap('{:,.0f}'.format)
#df_affiliate_by_date = df_affiliate_by_date.sort_values('TOTAL',ascending=False)
#st.dataframe(df_affiliate_by_date)
#期間とアフィリエイターを指定した折れ線グラフ

#期間と広告主を指定した折れ線グラフ

#伸びてるアフィリエイターと広告主を自動認識（週ベース）

#初成果を上げたアフィリエイター
