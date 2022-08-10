import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff

import cufflinks as cf

import warnings
warnings.filterwarnings("ignore")

####### Load Dataset #####################

df = pd.read_csv("./dataset.csv")

st.set_page_config(layout="wide")

st.markdown("## House PRice Dataset Analysis")   ## Main Title

################# Scatter Chart Logic #################

st.sidebar.markdown("### Scatter Chart: Explore Relationship Between Ingredients :")

columns = df.select_dtypes(exclude=['object']).columns.tolist()

x_axis = st.sidebar.selectbox("X-Axis", columns)
y_axis = st.sidebar.selectbox("Y-Axis", columns, index=1)

fig=plt.figure(figsize=(12,6))

if x_axis and y_axis:
    scatter_fig = df.iplot(kind="scatter", x=x_axis, y=y_axis,
                    mode="markers",
                    categories="BldgType",
                    asFigure=True, opacity=1.0,
                    xTitle=x_axis,
                    yTitle=y_axis,
                    title=f'Scatter Plot of {x_axis.capitalize()} vs {y_axis.capitalize()}')


########## Bar Chart Logic ##################

st.sidebar.markdown("### Bar Chart: Average Ingredients Per Wine Type : ")

avg_wine_df = df.groupby(by=["BldgType"]).mean()

bar_axis = st.sidebar.multiselect(label="Bar Chart Ingredient", options=avg_wine_df.columns.tolist(), default=["PoolArea", "LotArea"])

if bar_axis:
    bar_fig = avg_wine_df[bar_axis].iplot(kind="bar",
                        barmode="stack",
                        xTitle="Wine Type",
                        title="Distribution of Average Ingredients Per Wine Type",
                        asFigure=True,
                        opacity=1.0,
                        );
else:
    bar_fig = avg_wine_df[["LotArea"]].iplot(kind="bar",
                        barmode="stack",
                        xTitle="Wine Type",
                        title="Distribution of Average Alcohol Per Wine Type",
                        asFigure=True,
                        opacity=1.0,
                        );

################# Histogram Logic ########################

st.sidebar.markdown("### Histogram: Explore Distribution of Ingredients : ")

hist_axis = st.sidebar.multiselect(label="Histogram Ingredient", options=columns, default=["LotArea"])
bins = st.sidebar.radio(label="Bins :", options=[10,20,30,40,50], index=1)

if hist_axis:
    hist_fig = df.iplot(kind="hist",
                             keys=hist_axis,
                             bins=bins,
                             title="Distribution of columns",
                             asFigure=True,
                             opacity=1.0
                            );
else:
    hist_fig = df.iplot(kind="hist",
                             keys=["LotArea"],
                             bins=bins,
                             title="Distribution of Alcohol",
                             asFigure=True,
                             opacity=1.0
                            );

#################### Pie Chart Logic ##################################

wine_cnt = df.groupby(by=["BldgType"]).count()[['LotArea']].reset_index()

pie_fig = wine_cnt.iplot(kind="pie", labels="BldgType", values="LotArea",
                         title="Wine Samples Distribution Per WineType",
                         hole=0.4,
                         asFigure=True)


##################### Layout Application ##################

container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        scatter_fig
    with col2:
        bar_fig


container2 = st.container()
col3, col4 = st.columns(2)

with container2:
    with col3:
        hist_fig
    with col4:
        pie_fig
