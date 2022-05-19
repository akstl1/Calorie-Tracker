import pokebase as pb
import webbrowser
import dash
from dash import html
from dash import dcc
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import requests
import plotly.express as px
import numpy as np

app = dash.Dash()
# server=app.server

df = pd.read_csv('./calorie_df.csv')

df['Daily_Green'] = df['Breakfast - Green']+df['Lunch - Green']+df['Dinner - Green']+df['Snacks - Green']
df['Daily_Yellow'] = df['Breakfast - Yellow']+df['Lunch - Yellow']+df['Dinner - Yellow']+df['Snacks - Yellow']
df['Daily_Red'] = df['Breakfast - Red']+df['Lunch - Red']+df['Dinner - Red']+df['Snacks - Red']

colors = ['green','gold','red']
fig = px.bar(df, x="Date", y=["Daily_Green", "Daily_Yellow", "Daily_Red"], title="Daily Calorie Density Intake Breakdown")

# fig = go.Figure(data=[go.Bar(
#     x=df['Date'],
#     y=,
#     marker_color=colors # marker color can be a single color value or an iterable
# )])
# fig.update_layout(title_text='Least Used Feature')

app.layout = html.Div([dcc.Graph(figure=fig)

])


if __name__=="__main__":
    app.run_server()
