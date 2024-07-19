import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

#Data frame creation


#sql connection
mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data",
                      password="2107")
cursor=mydb.cursor()

#aggregated_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggregated_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type",
                                                  "Transaction_count","Transaction_amount"))

#aggregated_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggregated_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type",
                                                  "Transaction_count","Transaction_amount"))

#aggregated_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggregated_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands",
                                                  "Transaction_count","Percentage"))

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","District",
                                                  "Transaction_count","Transaction_amount"))


#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","District",
                                                  "Transaction_count","Transaction_amount"))

#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","District",
                                                  "Registered_Users","App_Opens"))

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes",
                                                  "Transaction_count","Transaction_amount"))

#top_transctio_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes",
                                                  "Transaction_count","Transaction_amount"))


#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes",
                                                  "RegisteredUsers"))




def Transaction_amount_count_Y(df, year):
    TACY=df[df["Years"]==year]
    TACY.reset_index(drop=True,inplace=True)

    TACY_GROUP=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACY_GROUP.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(TACY_GROUP,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                     color_discrete_sequence=px.colors.sequential.Sunset_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

       fig_count=px.bar(TACY_GROUP,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                   color_discrete_sequence=px.colors.sequential.Blackbody,height=650,width=600)
       st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        URL="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(URL)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(TACY_GROUP, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                  color="Transaction_amount",color_continuous_scale="Rainbow",
                                  range_color=(TACY_GROUP["Transaction_amount"].min(),TACY_GROUP["Transaction_amount"].max()),
                                  hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",height=650,width=600)
    
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(TACY_GROUP, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                  color="Transaction_count",color_continuous_scale="Rainbow",
                                  range_color=(TACY_GROUP["Transaction_count"].min(),TACY_GROUP["Transaction_count"].max()),
                                  hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",height=650,width=600)
    
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return TACY

def Transaction_amount_count_Y_Q(df, quarter):
    TACY=df[df["Quarter"]==quarter]
    TACY.reset_index(drop=True,inplace=True)

    TACY_GROUP=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACY_GROUP.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(TACY_GROUP,x="States",y="Transaction_amount",title=f"{TACY['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                         color_discrete_sequence=px.colors.sequential.Sunset_r,height= 650,width=600)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count=px.bar(TACY_GROUP,x="States",y="Transaction_count",title=f"{TACY['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                         color_discrete_sequence=px.colors.sequential.Blackbody,height= 650,width=600)
        st.plotly_chart(fig_count)
    col1,col2=st.columns(2)
    with col1:

       URL="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
       response=requests.get(URL)
       data1=json.loads(response.content)
       states_name=[]
       for feature in data1["features"]:
          states_name.append(feature["properties"]["ST_NM"])

       states_name.sort()

       fig_india_1=px.choropleth(TACY_GROUP, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                 color="Transaction_amount",color_continuous_scale="Rainbow",
                                 range_color=(TACY_GROUP["Transaction_amount"].min(),TACY_GROUP["Transaction_amount"].max()),
                                 hover_name="States",title=f"{TACY['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",height=650,width=600)
    
       fig_india_1.update_geos(visible=False)
       st.plotly_chart(fig_india_1)
    with col2:

       fig_india_2=px.choropleth(TACY_GROUP, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                 color="Transaction_count",color_continuous_scale="Rainbow",
                                 range_color=(TACY_GROUP["Transaction_count"].min(),TACY_GROUP["Transaction_count"].max()),
                                 hover_name="States",title=f"{TACY['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",height=650,width=600)
    
       fig_india_2.update_geos(visible=False)
       st.plotly_chart(fig_india_2)

       return TACY

    
def Aggre_Tran_Transaction_Type(df,state):

   TACY=df[df["States"]==state]
   TACY.reset_index(drop=True,inplace=True)

   TACY_GROUP=TACY.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
   TACY_GROUP.reset_index(inplace=True)
   
   col1,col2=st.columns(2)
   with col1:
     fig_pie_1=px.pie(data_frame=TACY_GROUP,names="Transaction_type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.8)
     st.plotly_chart(fig_pie_1)

   with col2:
      fig_pie_2=px.pie(data_frame=TACY_GROUP,names="Transaction_type",values="Transaction_count",
                       width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.8)
      st.plotly_chart(fig_pie_2)

#Aggregated_user_analysis_1
def Aggregated_user_plot_1(df,year):
    AGUY=df[df["Years"]==year]
    AGUY.reset_index(drop=True,inplace=True)

    AGUY_GROUP=pd.DataFrame(AGUY.groupby("Brands")["Transaction_count",].sum())
    AGUY_GROUP.reset_index(inplace=True)

    fig_bar_1=px.bar(AGUY_GROUP,x="Brands",y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",
                      width=1000,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return AGUY

#Aggregated_user_analysis_2
def Aggre_user_plot_2(df,quarter):
   AGUYQ=df[df["Quarter"]==quarter]
   AGUYQ.reset_index(drop=True,inplace=True)


   AGUYQG=pd.DataFrame(AGUYQ.groupby("Brands")["Transaction_count"].sum())
   AGUYQG.reset_index(inplace=True)

   fig_bar_1=px.bar(AGUYQG,x="Brands",y="Transaction_count",title=f"{quarter} QUARTER,BRANDS AND TRANSACTION COUNT",
                       width=1000,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
   st.plotly_chart(fig_bar_1)

   return AGUYQ

#Aggre_user_analysis_3
def Aggre_user_plot_3(df,state):
   AUYQS=df[df["States"]==state]
   AUYQS.reset_index(drop=True,inplace=True)

   fig_line_1=px.line(AUYQS,x="Brands",y="Transaction_count",hover_data="Percentage",
                      title=f"{state.upper()} BRANDS, TRANSACTION COUNT,PERCENTAGE",width=1000,markers=True)
   st.plotly_chart(fig_line_1)

#Map_Insurance_District
def Map_insur_District(df,state):

   TACY=df[df["States"]==state]
   TACY.reset_index(drop=True,inplace=True)

   TACY_GROUP=TACY.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
   TACY_GROUP.reset_index(inplace=True)

   col1,col2=st.columns(2)
   with col1:
       fig_bar_1=px.bar(TACY_GROUP,x="Transaction_amount",y="District",orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
       st.plotly_chart(fig_bar_1)

   with col2:
       fig_bar_2=px.bar(TACY_GROUP,x="Transaction_count",y="District",orientation="h",height=600,
                         title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
       st.plotly_chart(fig_bar_2)

#Map_User
def Map_user_plot_1(df,year):
    MUY=df[df["Years"]==year]
    MUY.reset_index(drop=True,inplace=True)

    MUY_GROUP=MUY.groupby("States")[["Registered_Users","App_Opens"]].sum()
    MUY_GROUP.reset_index(inplace=True)

    fig_bar_1=px.line(MUY_GROUP,x="States",y=["Registered_Users","App_Opens"],title=f"{year} REGISTEREDUSERS APPOPENS",
                      width=1000,height=800,markers=True)
    st.plotly_chart(fig_bar_1)

    return MUY

#Map_User2
def Map_user_plot_2(df,quarter):
    MUYQ=df[df["Quarter"]==quarter]
    MUYQ.reset_index(drop=True,inplace=True)

    MUYQ_GROUP=MUYQ.groupby("States")[["Registered_Users","App_Opens"]].sum()
    MUYQ_GROUP.reset_index(inplace=True)

    fig_bar_1=px.line(MUYQ_GROUP,x="States",y=["Registered_Users","App_Opens"],title=f"{df['Years'].min()} {quarter} QUARTER REGISTEREDUSERS APPOPENS",
                      width=1000,height=800,markers=True,color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bar_1)

    return MUYQ

#map_user_plot_3
def map_user_plot_3(df,states):
    MUYQS=df[df["States"]==states]
    MUYQS.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(MUYQS,x="Registered_Users",y="District",orientation="h",title=f"{states.upper()} REGISTERED USER",
                                  height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2=px.bar(MUYQS,x="App_Opens",y="District",orientation="h",title=f"{states.upper()} APP OPENS",
                                 height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_2)

#Top_Insurance_Plot_1
def Top_insurance_plot_1(df,state):

   TIY=df[df["States"]==state]
   TIY.reset_index(drop=True,inplace=True)

   TIY_GROUP=TIY.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum()
   TIY_GROUP.reset_index(inplace=True)

   col1,col2=st.columns(2)
   with col1:
       fig_bar_1=px.bar(TIY,x="Quarter",y="Transaction_amount",hover_data="Pincodes",
                         title=f"{state.upper()} PINCODES AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
       st.plotly_chart(fig_bar_1)

   with col2:
       fig_bar_2=px.bar(TIY,x="Quarter",y="Transaction_count",hover_data="Pincodes",
                        title=f"{state.upper()} PINCODES AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.GnBu_r)
       st.plotly_chart(fig_bar_2)

#top_user_plot_1
def top_user_plot_1(df,year):
    TUY=df[df["Years"]==year]
    TUY.reset_index(drop=True,inplace=True)

    TUY_GROUP=pd.DataFrame(TUY.groupby(["States","Quarter"])["RegisteredUsers",].sum())
    TUY_GROUP.reset_index(inplace=True)

    fig_top_plot_1=px.bar(TUY_GROUP,x="States",y="RegisteredUsers",color="Quarter",width=1000,height=800,
                          color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",
                          title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return TUY

#Top_user_plot_2
def top_user_plot_2(df,state):
    TUYS=df[df["States"]==state]
    TUYS.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(TUYS,x="Quarter",y="RegisteredUsers",title="REGISTEREDUSERS,PINCODES,QUARTER",width=1000,
                          height=800,color="RegisteredUsers",hover_data="Pincodes",color_continuous_scale=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_top_plot_2)

    #sql connection
def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                          user="postgres",
                          port="5432",
                          database="phonepe_data",
                          password="2107")
    cursor=mydb.cursor()

    #plot_1
    query1=f'''select states, sum(transaction_amount) AS transaction_amount
              from {table_name}
              group by states
              order by transaction_amount desc
              limit 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states","transaction_amount"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(df_1,x="states",y="transaction_amount",title="TOP 10 OF TRANSACTION AMOUNT",hover_name="states",
                      color_discrete_sequence=px.colors.sequential.Sunset_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2=f'''select states, sum(transaction_amount) AS transaction_amount
              from {table_name}
              group by states
              order by transaction_amount
              limit 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states","transaction_amount"))

    with col2:

       fig_amount_2=px.bar(df_2,x="states",y="transaction_amount",title="LAST 10 OF TRANSACTION AMOUNT",hover_name="states",
                  color_discrete_sequence=px.colors.sequential.Sunset,height=650,width=600)
       st.plotly_chart(fig_amount_2)

    #plot_3
    query3=f'''select states, AVG(transaction_amount) AS transaction_amount
               from {table_name}
               group by states
               order by transaction_amount;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states","transaction_amount"))

    fig_amount_3=px.bar(df_3,x="states",y="transaction_amount",title="AVERAGE OF TRANSACTION AMOUNT",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=800,width=1000)
    st.plotly_chart(fig_amount_3)


    #sql connection
def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                          user="postgres",
                          port="5432",
                          database="phonepe_data",
                          password="2107")
    cursor=mydb.cursor()

    #plot_1
    query1=f'''select states, sum(transaction_count) AS transaction_count
              from {table_name}
              group by states
              order by transaction_count desc
              limit 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states","transaction_count"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="states",y="transaction_count",title="TOP 10 OF TRANSACTION COUNT",hover_name="states",
                          color_discrete_sequence=px.colors.sequential.Sunset_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2=f'''select states, sum(transaction_count) AS transaction_count
              from {table_name}
              group by states
              order by transaction_count
              limit 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states","transaction_count"))

    with col2:
        fig_amount_2=px.bar(df_2,x="states",y="transaction_count",title="LAST 10 OF TRANSACTION COUNT",hover_name="states",
                  color_discrete_sequence=px.colors.sequential.Sunset,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3=f'''select states, AVG(transaction_count) AS transaction_count
               from {table_name}
               group by states
               order by transaction_count;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states","transaction_count"))

    fig_amount_3=px.bar(df_3,x="states",y="transaction_count",title="AVERAGE OF TRANSACTION COUNT",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_user(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                          user="postgres",
                          port="5432",
                          database="phonepe_data",
                          password="2107")
    cursor=mydb.cursor()

    #plot_1
    query1=f'''select districts, sum(registered_users) as registered_users
              from {table_name}
              where states='{state}'
              group by districts
              order by registered_users desc
              limit 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("districts","registered_users"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="districts",y="registered_users",title="TOP 10 REGISTERED USERS",hover_name="districts",
                          color_discrete_sequence=px.colors.sequential.Sunset_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2=f'''select districts, sum(registered_users) as registered_users
              from {table_name}
              where states='{state}'
              group by districts
              order by registered_users
              limit 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("districts","registered_users"))

    with col2:
        fig_amount_2=px.bar(df_2,x="districts",y="registered_users",title="LAST 10 REGISTERED USERS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Sunset,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3=f'''select districts, avg(registered_users) as registered_users
              from {table_name}
              where states='{state}'
              group by districts
              order by registered_users;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("districts","registered_users"))

    fig_amount_3=px.bar(df_3,x="districts",y="registered_users",title="AVG OF REGISTERED USERS",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_appopens(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                          user="postgres",
                          port="5432",
                          database="phonepe_data",
                          password="2107")
    cursor=mydb.cursor()

    #plot_1
    query1=f'''select districts, sum(app_opens) as app_opens
              from {table_name}
              where states='{state}'
              group by districts
              order by app_opens desc
              limit 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("districts","app_opens"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="districts",y="app_opens",title="TOP 10 APPOPENS",hover_name="districts",
                           color_discrete_sequence=px.colors.sequential.Sunset_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2=f'''select districts, sum(app_opens) as app_opens
              from {table_name}
              where states='{state}'
              group by districts
              order by app_opens
              limit 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("districts","app_opens"))

    with col2:
        fig_amount_2=px.bar(df_2,x="districts",y="app_opens",title="LAST 10 APPOPENS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Sunset,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3=f'''select districts, avg(app_opens) as app_opens
              from {table_name}
              where states='{state}'
              group by districts
              order by app_opens;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("districts","app_opens"))

    fig_amount_3=px.bar(df_3,x="districts",y="app_opens",title="AVG OF APPOPENS",hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_users(table_name):
    mydb=psycopg2.connect(host="localhost",
                          user="postgres",
                          port="5432",
                          database="phonepe_data",
                          password="2107")
    cursor=mydb.cursor()

    #plot_1
    query1=f'''select states, sum(registeredusers) as registeredusers
              from {table_name}
              group by states
              order by registeredusers desc
              limit 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states","registeredusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="states",y="registeredusers",title="TOP 10 REGISTERED USERS",hover_name="states",
                           color_discrete_sequence=px.colors.sequential.Sunset_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2=f'''select states, sum(registeredusers) as registeredusers
              from {table_name}
              group by states
              order by registeredusers
              limit 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states","registeredusers"))

    with col2:
        fig_amount_2=px.bar(df_2,x="states",y="registeredusers",title="LAST 10 REGISTERED USERS",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Sunset,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3=f'''select states, avg(registeredusers) as registeredusers
              from {table_name}
              group by states
              order by registeredusers;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states","registeredusers"))

    fig_amount_3=px.bar(df_3,x="states",y="registeredusers",title="AVG OF REGISTERED USERS",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=800,width=1000)
    st.plotly_chart(fig_amount_3)





# streamlit part
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")


with st.sidebar:
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    col1,col2=st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe is an indian digital payments and financial technology company")
        st.write("***FEATURES***")
        st.write("***Credit & Debit Card linking***")
        st.write("***Bank Balance Check***")
        st.write("***Money Storage***")
        st.write("***PIN Authorization***")
        st.download_button("DOWNLOAD THE APP NOW","https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\smani\manikandanproject\photo\download.png"),width=600)
    
    col3,col4=st.columns(2)
    with col3:
        st.image(Image.open(r"C:\Users\smani\manikandanproject\photo1.jpg"))

    with col4:
        st.write("***Easy 1transactions***")
        st.write("***One App For All Your Payments***")
        st.write("***Your Bank Acount Is All You Need***")
        st.write("***Multiple Payment Modes***")
        st.write("***Phonepe Merchants***")
        st.write("***Multiple Ways To Pay***")
        st.write("***1.Direct Transfer & More***")
        st.write("***2.QR Code***")
        st.write("***Earn Great Rewards***")
    
    col5,col6=st.columns(2)
    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("***No Wallet Top-up Required***")
        st.write("***Pay Directly From Any Bank A/C***")
        st.write("***Instantly & Free***")

    with col6:
        st.image(Image.open(r"C:\Users\smani\manikandanproject\photo2.jpg"))



elif select=="DATA EXPLORATION":
     tab1,tab2,tab3=st.tabs(["Aggreated Analysis","Map Analysis","Top Analysis"])

     with tab1:
         method=st.radio("Select The Method",["Aggregated Insurance","Aggregated Transaction","Aggregated User"])

         if method=="Aggregated Insurance":
             
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year",Aggregated_insurance["Years"].min(),Aggregated_insurance["Years"].max(),Aggregated_insurance["Years"].min())
             tac_Y=Transaction_amount_count_Y(Aggregated_insurance, years)

             col1,col2=st.columns(2)
             with col1:
                 
                 quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
             Transaction_amount_count_Y_Q(tac_Y, quarters)    
               

         elif method=="Aggregated Transaction":
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year",Aggregated_transaction["Years"].min(),Aggregated_transaction["Years"].max(),Aggregated_transaction["Years"].min())
             Agg_tran_tac_Y=Transaction_amount_count_Y(Aggregated_transaction, years)

             col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State",Agg_tran_tac_Y["States"].unique())

             Aggre_Tran_Transaction_Type(Agg_tran_tac_Y,states)

             col1,col2=st.columns(2)
             with col1:
                 
                 quarters=st.slider("Select The Quarter",Agg_tran_tac_Y["Quarter"].min(),Agg_tran_tac_Y["Quarter"].max(),Agg_tran_tac_Y["Quarter"].min())
             Aggre_Tran_Tac_Y_Q=Transaction_amount_count_Y_Q(Agg_tran_tac_Y, quarters)

             col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State_Ty",Aggre_Tran_Tac_Y_Q["States"].unique())

             Aggre_Tran_Transaction_Type(Aggre_Tran_Tac_Y_Q,states)
    
               
             
         elif method=="Aggregated User":
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year",Aggregated_user["Years"].min(),Aggregated_user["Years"].max(),Aggregated_user["Years"].min())
             Aggre_user_Y=Aggregated_user_plot_1(Aggregated_user,years)

             col1,col2=st.columns(2)
             with col1:
                 
                 quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
             Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y, quarters)

             col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State",Aggre_user_Y_Q["States"].unique())

             Aggre_user_plot_3(Aggre_user_Y_Q,states)
    

             
         

     with tab2:
         method2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])
         if method2=="Map Insurance":
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year_Y",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
               map_insur_tac_Y=Transaction_amount_count_Y(Map_insurance, years)

               col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State",map_insur_tac_Y["States"].unique())

             Map_insur_District(map_insur_tac_Y,states)

             col1,col2=st.columns(2)
             with col1:
                 
                 quarters=st.slider("Select The Quarter_Q",map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
             map_insur_tac_Y_Q=Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)

             col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State_Ty",map_insur_tac_Y_Q["States"].unique())

             Map_insur_District(map_insur_tac_Y_Q,states)
    

             

         elif method2=="Map Transaction":
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year_Y",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
               map_tran_tac_Y=Transaction_amount_count_Y(Map_transaction, years)

               col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State",map_tran_tac_Y["States"].unique())

             Map_insur_District(map_tran_tac_Y,states)

             col1,col2=st.columns(2)
             with col1:
                 
                 quarters=st.slider("Select The Quarter_Q",map_tran_tac_Y["Quarter"].min(),map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
             map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

             col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State_Ty",map_tran_tac_Y_Q["States"].unique())

             Map_insur_District(map_tran_tac_Y_Q,states)
             
         elif method2=="Map User":
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
               map_user_Y=Map_user_plot_1(Map_user, years)

               col1,col2=st.columns(2)
             with col1:
                 
                 quarters=st.slider("Select The Quarter_Q",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
             map_user_Y_Q=Map_user_plot_2(map_user_Y, quarters)

             col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State_Y_Q",map_user_Y_Q["States"].unique())

             map_user_plot_3(map_user_Y_Q,states)


     with tab3:
         method3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

         if method3=="Top Insurance":
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year_TY",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
               Top_insur_tac_Y=Transaction_amount_count_Y(Top_insurance, years)

               col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State_TI",Top_insur_tac_Y["States"].unique())

             Top_insurance_plot_1(Top_insur_tac_Y,states)

             col1,col2=st.columns(2)
             with col1:
                 
                 quarters=st.slider("Select The Quarter_YQ",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min())
             Top_insur_tac_Y_Q=Transaction_amount_count_Y_Q(Top_insur_tac_Y, quarters)

             

         elif method3=="Top Transaction":
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year_TY",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
               Top_tran_tac_Y=Transaction_amount_count_Y(Top_transaction, years)

               col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State_TI",Top_tran_tac_Y["States"].unique())

             Top_insurance_plot_1(Top_tran_tac_Y,states)

             col1,col2=st.columns(2)
             with col1:
                 
                 quarters=st.slider("Select The Quarter_YQ",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
             Top_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Top_tran_tac_Y, quarters)

         elif method3=="Top User":
             col1,col2=st.columns(2)
             with col1:
             
               years=st.slider("Select The Year_TU",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
               Top_user_Y=top_user_plot_1(Top_user, years)

             col1,col2=st.columns(2)
             with col1:
                 states=st.selectbox("Select The State_TU",Top_user_Y["States"].unique())
             top_user_plot_2(Top_user_Y,states)
             
    
elif select=="TOP CHARTS":
     question=st.selectbox("Select The Questions",["1. Transaction Amount and Count of Aggregated Insurance",
                                                   "2. Transaction Amount and Count of Map Insurance",
                                                   "3. Transaction Amount and Count of Top Insurance",
                                                   "4. Transaction Amount and Count of Aggregated Transaction",
                                                   "5. Transaction Amount and Count of Map Transaction",
                                                   "6. Transaction Amount and Count of Top Transaction",
                                                   "7. Transaction Count of Aggregated User",
                                                   "8. Registered Users of Map USer",
                                                   "9. App Opens of Map User",
                                                   "10. Registered User of Top User"
                                                   ])
     if question=="1. Transaction Amount and Count of Aggregated Insurance":
         
         st.subheader("TRANSACTION AMOUNT")
         top_chart_transaction_amount("aggregated_insurance")
         st.subheader("TRANSACTION COUNT")   
         top_chart_transaction_count("aggregated_insurance")
         
     elif question=="2. Transaction Amount and Count of Map Insurance":
         
         st.subheader("TRANSACTION AMOUNT")
         top_chart_transaction_amount("map_insurance")
         st.subheader("TRANSACTION COUNT")   
         top_chart_transaction_count("map_insurance")

     elif question=="3. Transaction Amount and Count of Top Insurance":
         
         st.subheader("TRANSACTION AMOUNT")
         top_chart_transaction_amount("top_insurance")
         st.subheader("TRANSACTION COUNT")   
         top_chart_transaction_count("top_insurance")

     elif question=="4. Transaction Amount and Count of Aggregated Transaction":
         
         st.subheader("TRANSACTION AMOUNT")
         top_chart_transaction_amount("aggregated_transaction")
         st.subheader("TRANSACTION COUNT")   
         top_chart_transaction_count("aggregated_transaction")

     elif question=="5. Transaction Amount and Count of Map Transaction":
         
         st.subheader("TRANSACTION AMOUNT")
         top_chart_transaction_amount("map_transaction")
         st.subheader("TRANSACTION COUNT")   
         top_chart_transaction_count("map_transaction")

     elif question=="6. Transaction Amount and Count of Top Transaction":
         
         st.subheader("TRANSACTION AMOUNT")
         top_chart_transaction_amount("top_transaction")
         st.subheader("TRANSACTION COUNT")   
         top_chart_transaction_count("top_transaction")

     elif question=="7. Transaction Count of Aggregated User":
         
         st.subheader("TRANSACTION COUNT")   
         top_chart_transaction_count("aggregated_user")

     elif question=="8. Registered Users of Map USer":
         
         states=st.selectbox("Select the state",Map_user["States"].unique())
         st.subheader("REGISTERED USERS")   
         top_chart_registered_user("map_user",states)

     elif question=="9. App Opens of Map User":
         
         states=st.selectbox("Select the state",Map_user["States"].unique())
         st.subheader("app_opens")   
         top_chart_appopens("map_user",states)

     elif question=="10. Registered User of Top User":
        
         st.subheader("REGISTERED_USERS")   
         top_chart_registered_users("top_user")


     
         
         

         

