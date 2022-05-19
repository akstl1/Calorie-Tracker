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

cal_fig = go.Figure()
cal_fig.add_trace(go.Bar(
    y=calorie_df.Daily_Green,
    x=calorie_df.Date,
    name='Green',
    text=calorie_df['Daily_Green'],
    marker=dict(
        color='rgb(0,255,0)'
    )
))
cal_fig.add_trace(go.Bar(
    y=calorie_df.Daily_Yellow,
    x=calorie_df.Date,
    name='Yellow',
    text=calorie_df['Daily_Yellow'],
    marker=dict(
        color='rgb(242,242,19)'
        # line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
cal_fig.add_trace(go.Bar(
    y=calorie_df.Daily_Red,
    x=calorie_df.Date,
    name='Red',
    text=calorie_df['Daily_Red'],
    marker=dict(
        color='rgb(246, 78, 139)'
        # line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
cal_fig.update_layout(barmode='stack')
cal_fig.update_layout(title_text='Daily Calorie and Calorie Density Breakdown', title_x=0.5)

### weight plot

weight_df = pd.read_csv('./weight_df.csv')
weight_fig = px.line(weight_df, x="Date", y="Weight (lb)", title='Weight Over Time',markers=True)
weight_fig.add_hline(y=155,line=dict(color='royalblue', width=4, dash='dot'))
weight_fig.update_layout(yaxis_range=[150,170])
weight_fig.update_layout(title_text="Weight Over Time", title_x=0.5)

annotation = {
    'xref': 'paper',
    'yref': 'paper',
    'x': 0.05,
    'y': 0.27,
    'text': 'Goal weight: 155 lb',
    'showarrow': False,
    'arrowhead': 0,
}

weight_fig.update_layout({'annotations': [annotation]})


### exercise plot

exercise_df = pd.read_csv('./exercise_df.csv')
exercise_fig = px.line(exercise_df, x="Date", y="Calories Burned",markers=True)
exercise_fig.update_layout(yaxis_range=[0,1500])
exercise_fig.update_layout(title_text="Calories Burned From Exercise", title_x=0.5)

### calorie breakdown chart

breakfast_total = sum(calorie_df['Breakfast - Green']+calorie_df['Breakfast - Yellow']+calorie_df['Breakfast - Red'])
breakfast_green_pct = 100*sum(calorie_df['Breakfast - Green'])/breakfast_total
breakfast_yellow_pct = 100*sum(calorie_df['Breakfast - Yellow'])/breakfast_total
breakfast_red_pct = 100*sum(calorie_df['Breakfast - Red'])/breakfast_total

lunch_total = sum(calorie_df['Lunch - Green']+calorie_df['Lunch - Yellow']+calorie_df['Lunch - Red'])
lunch_green_pct = 100*sum(calorie_df['Lunch - Green'])/lunch_total
lunch_yellow_pct = 100*sum(calorie_df['Lunch - Yellow'])/lunch_total
lunch_red_pct = 100*sum(calorie_df['Lunch - Red'])/lunch_total

dinner_total = sum(calorie_df['Dinner - Green']+calorie_df['Dinner - Yellow']+calorie_df['Dinner - Red'])
dinner_green_pct = 100*sum(calorie_df['Dinner - Green'])/dinner_total
dinner_yellow_pct = 100*sum(calorie_df['Dinner - Yellow'])/dinner_total
dinner_red_pct = 100* sum(calorie_df['Dinner - Red'])/dinner_total

snack_total = sum(calorie_df['Snacks - Green']+calorie_df['Snacks - Yellow']+calorie_df['Snacks - Red'])
snacks_green_pct = 100*sum(calorie_df['Snacks - Green'])/snack_total
snacks_yellow_pct = 100*sum(calorie_df['Snacks - Yellow'])/snack_total
snacks_red_pct = 100*sum(calorie_df['Snacks - Red'])/snack_total

d2= {'Green': [breakfast_green_pct,lunch_green_pct,dinner_green_pct,snacks_green_pct],
     'Yellow': [breakfast_yellow_pct,lunch_yellow_pct,dinner_yellow_pct,snacks_yellow_pct],
     'Red':[breakfast_red_pct,lunch_red_pct,dinner_red_pct, snacks_red_pct]

                  }

d = pd.DataFrame(data=d2, index=['Breakfast','Lunch','Dinner','Snacks']).round(2)
pct_fig = go.Figure()
pct_fig.add_trace(go.Bar(
    y=d.index,
    x=d['Green'],
    name='Green',
    orientation='h',
    text=d['Green'],
    marker=dict(
        color='rgb(0,255,0)'
    )
))
pct_fig.add_trace(go.Bar(
    y=d.index,
    x=d['Yellow'],
    name='Yellow',
    orientation='h',
    text=d['Yellow'],
    marker=dict(
        color='rgb(242,242,19)'
        # line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
pct_fig.add_trace(go.Bar(
    y=d.index,
    x=d['Red'],
    name='Red',
    orientation='h',
    text=d['Red'],
    marker=dict(
        color='rgb(246, 78, 139)'
        # line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
pct_fig.update_layout(barmode='stack')
pct_fig.update_layout(title_text="Calorie Density Breakdown by Meal (%)", title_x=0.5)

### App layout

app.layout = html.Div([
        # create a div to store each graph
        html.Div([dcc.Graph(figure=cal_fig)]),
        html.Div([dcc.Graph(figure=weight_fig)]),
        html.Div([dcc.Graph(figure=exercise_fig)]),
        html.Div([dcc.Graph(figure=pct_fig)])

])

# run app
if __name__=="__main__":
    app.run_server()
