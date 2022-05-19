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

### calorie plot
calorie_df = pd.read_csv('./calorie_df.csv').fillna(0)

calorie_df['Daily_Green'] = calorie_df['Breakfast - Green']+calorie_df['Lunch - Green']+calorie_df['Dinner - Green']+calorie_df['Snacks - Green']
calorie_df['Daily_Yellow'] = calorie_df['Breakfast - Yellow']+calorie_df['Lunch - Yellow']+calorie_df['Dinner - Yellow']+calorie_df['Snacks - Yellow']
calorie_df['Daily_Red'] = calorie_df['Breakfast - Red']+calorie_df['Lunch - Red']+calorie_df['Dinner - Red']+calorie_df['Snacks - Red']

colors = ['green','gold','red']
fig = px.bar(calorie_df, x="Date", y=["Daily_Green", "Daily_Yellow", "Daily_Red"], title="Daily Calorie Density Intake Breakdown")

### weight plot

weight_df = pd.read_csv('./weight_df.csv')
fig2 = px.line(weight_df, x="Date", y="Weight (lb)", title='Weight Over Time',markers=True)
fig2.add_hline(y=155,line=dict(color='royalblue', width=4, dash='dot'))
fig2.update_layout(yaxis_range=[150,170])

### exercise plot

exercise_df = pd.read_csv('./exercise_df.csv')
fig3 = px.line(exercise_df, x="Date", y="Calories Burned", title='Calories Burned From Exercise',markers=True)
fig3.update_layout(yaxis_range=[0,1500])


# fig = go.Figure(data=[go.Bar(
#     x=calorie_df['Date'],
#     y=,
#     marker_color=colors # marker color can be a single color value or an iterable
# )])
# fig.update_layout(title_text='Least Used Feature')

app.layout = html.Div([
        html.Div([dcc.Graph(figure=fig)]),
        html.Div([dcc.Graph(figure=fig2)]),
        html.Div([dcc.Graph(figure=fig3)])

])


if __name__=="__main__":
    app.run_server()
