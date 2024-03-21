#import streamlit as st

#st.title("Manage")

# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import plotly.express as px #pip install plotly_express 
import pandas as pd  #pip install pandas
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Client Review Dashboards", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Dashboards")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

#fl = st.file_uploader(":file_folder: Upload a data file", type=(["csv", "xlsx", "xls"]))

#if fl is not None:
#    filename = fl.name
#    st.write(filename)
    #df = pd.read_excel(filename)
    
df = pd.read_excel(io='FamilyOfficeEntityDataSampleV1.1.xlsx',
                engine='openpyxl',
                       sheet_name='Client Profile' )
    
    #print(df)

col1, col2 = st.columns((2))
df["Date of Birth"] = pd.to_datetime(df["Date of Birth"])
startDate = pd.to_datetime(df["Date of Birth"]).min()
endDate = pd.to_datetime(df["Date of Birth"]).max()

with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
      
with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date of Birth"] >= date1) & (df["Date of Birth"] <= date2)]

st.sidebar.header("Choose your filter: ")

#create for Status
status = st.sidebar.multiselect("Pick the Status", df["Status"].unique())
if not status:
       df2 = df.copy()
else:
      df2 = df[df["Status"].isin(status)]

profession = st.sidebar.multiselect("Pick the Profession", df2["Profession"].unique())
if not profession:
       df3 = df2.copy()
else:
      df3 = df2[df2["Profession"].isin(profession)]

if not status and not profession:
       filtered_df = df
elif  status and profession:
       filtered_df = df3
elif  status and not profession:
       filtered_df = df2
elif  not status and profession:
       filtered_df = df3

status_df =  filtered_df.groupby(by = ["Status"], as_index = False)["Net Worth"].sum()

with col1:
       st.subheader("Status wise Net Worth review")
       fig = px.bar(status_df, x = "Status", y = "Net Worth", 
                    template="seaborn")
       st.plotly_chart(fig, use_container_width=True, height = 200)

profession_df =  filtered_df.groupby(by = ["Profession"], as_index = False)["Net Worth"].sum()
with col2:
       st.subheader("Profession wise Net Worth review")
       fig = px.pie(profession_df, values = "Net Worth", names = "Profession", hole=0.5) 
       fig.update_traces(text = filtered_df["Profession"], textposition = "outside")  
       st.plotly_chart(fig, use_container_width=True) 