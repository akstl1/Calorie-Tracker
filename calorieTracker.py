import dash
from dash import html, dcc, dash_table
from dash import dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import datetime as dt
from datetime import timedelta

import os
from dotenv import load_dotenv


from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# load env variables
load_dotenv()

# start up app, server
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# for your live Heroku PostgreSQL database
app.server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("URI")

db = SQLAlchemy(app.server)

# enter new row schema for db
class Entry(db.Model):
    __tablename__ = 'nutrition_table'

    Date = db.Column(db.Date, nullable=False, primary_key=True)
    Breakfast_Green = db.Column(db.Integer, nullable=False)
    Breakfast_Yellow = db.Column(db.Integer, nullable=False)
    Breakfast_Red = db.Column(db.Integer, nullable=False)
    Lunch_Green = db.Column(db.Integer, nullable=False)
    Lunch_Yellow = db.Column(db.Integer, nullable=False)
    Lunch_Red = db.Column(db.Integer, nullable=False)
    Dinner_Green = db.Column(db.Integer, nullable=False)
    Dinner_Yellow = db.Column(db.Integer, nullable=False)
    Dinner_Red = db.Column(db.Integer, nullable=False)
    Snacks_Green = db.Column(db.Integer, nullable=False)
    Snacks_Yellow = db.Column(db.Integer, nullable=False)
    Snacks_Red = db.Column(db.Integer, nullable=False)
    Weight = db.Column(db.Numeric, nullable=False)
    Steps = db.Column(db.Integer, nullable=False)

    def __init__(self, date, breakfast_green, breakfast_yellow, breakfast_red, lunch_green, lunch_yellow, lunch_red, dinner_green, dinner_yellow, dinner_red, snacks_green, snacks_yellow, snacks_red, weight, steps):
        self.Date = date
        self.Breakfast_Green = breakfast_green
        self.Breakfast_Yellow = breakfast_yellow
        self.Breakfast_Red = breakfast_red
        self.Lunch_Green = lunch_green
        self.Lunch_Yellow = lunch_yellow
        self.Lunch_Red = lunch_red
        self.Dinner_Green = dinner_green
        self.Dinner_Yellow = dinner_yellow
        self.Dinner_Red = dinner_red
        self.Snacks_Green = snacks_green
        self.Snacks_Yellow = snacks_yellow
        self.Snacks_Red = snacks_red
        self.Weight = weight
        self.Steps = steps

df = pd.read_sql_table('nutrition_table', con=db.engine)
print(df)
# ------------------------------------------------------------------------------------------------

### calorie plot
calorie_df = pd.read_excel('./data_df.xlsx', 'calorie_df',converters = {'Date':dt.datetime.date}).fillna(0)

calorie_df['Daily_Green'] = calorie_df.Breakfast_Green+calorie_df.Lunch_Green+calorie_df.Dinner_Green+calorie_df.Snacks_Green
calorie_df['Daily_Yellow'] = calorie_df.Breakfast_Yellow+calorie_df.Lunch_Yellow+calorie_df.Dinner_Yellow+calorie_df.Snacks_Yellow
calorie_df['Daily_Red'] = calorie_df.Breakfast_Red+calorie_df.Lunch_Red+calorie_df.Dinner_Red+calorie_df.Snacks_Red
# calorie_df.Date = calorie_df.Date.apply(lambda x:dt.datetime.strptime(x,'%m/%d/%Y').date())

cal_fig = go.Figure()
cal_fig.add_trace(go.Bar(
    y=calorie_df.Daily_Green,
    x=calorie_df.Date,
    name='Green',
    text=calorie_df.Daily_Green,
    marker=dict(
        color='rgb(0,255,0)'
    )
))
cal_fig.add_trace(go.Bar(
    y=calorie_df.Daily_Yellow,
    x=calorie_df.Date,
    name='Yellow',
    text=calorie_df.Daily_Yellow,
    marker=dict(
        color='rgb(242,242,19)'
    )
))
cal_fig.add_trace(go.Bar(
    y=calorie_df.Daily_Red,
    x=calorie_df.Date,
    name='Red',
    text=calorie_df.Daily_Red,
    marker=dict(
        color='rgb(246, 78, 139)'
    )
))
cal_fig.update_layout(barmode='stack')
cal_fig.update_layout(title_text='Daily Calorie and Calorie Density Breakdown', title_x=0.5)


### weight plot

weight_df = pd.read_excel('./data_df.xlsx', 'weight_df',converters = {'Date':dt.datetime.date})
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

exercise_df = pd.read_excel('./data_df.xlsx', 'exercise_df',converters = {'Date':dt.datetime.date})

exercise_fig = px.line(exercise_df, x="Date", y="Steps",markers=True)
exercise_fig.update_layout(yaxis_range=[0,1500])
exercise_fig.update_layout(title_text="Steps", title_x=0.5)

### calorie breakdown chart

breakfast_total = sum(calorie_df.Breakfast_Green+calorie_df.Breakfast_Yellow+calorie_df.Breakfast_Red)
if breakfast_total:
    breakfast_green_pct = 100*sum(calorie_df.Breakfast_Green)/breakfast_total
    breakfast_yellow_pct = 100*sum(calorie_df.Breakfast_Yellow)/breakfast_total
    breakfast_red_pct = 100*sum(calorie_df.Breakfast_Red)/breakfast_total
else:
    breakfast_green_pct,breakfast_yellow_pct,breakfast_red_pct =0,0,0

lunch_total = sum(calorie_df.Lunch_Green+calorie_df.Lunch_Yellow+calorie_df.Lunch_Red)
if lunch_total:
    lunch_green_pct = 100*sum(calorie_df.Lunch_Green)/lunch_total
    lunch_yellow_pct = 100*sum(calorie_df.Lunch_Yellow)/lunch_total
    lunch_red_pct = 100*sum(calorie_df.Lunch_Red)/lunch_total
else:
    lunch_green_pct,lunch_yellow_pct,lunch_red_pct=0,0,0

dinner_total = sum(calorie_df.Dinner_Green+calorie_df.Dinner_Yellow+calorie_df.Dinner_Red)
if dinner_total:
    dinner_green_pct = 100*sum(calorie_df.Dinner_Green)/dinner_total
    dinner_yellow_pct = 100*sum(calorie_df.Dinner_Yellow)/dinner_total
    dinner_red_pct = 100* sum(calorie_df.Dinner_Red)/dinner_total
else:
    dinner_green_pct,dinner_yellow_pct,dinner_red_pct=0,0,0

snack_total = sum(calorie_df.Snacks_Green+calorie_df.Snacks_Yellow+calorie_df.Snacks_Red)
if snack_total:
    snacks_green_pct = 100*sum(calorie_df.Snacks_Green)/snack_total
    snacks_yellow_pct = 100*sum(calorie_df.Snacks_Yellow)/snack_total
    snacks_red_pct = 100*sum(calorie_df.Snacks_Red)/snack_total
else:
    snacks_green_pct,snacks_yellow_pct,snacks_red_pct=0,0,0

d2= {'Green': [breakfast_green_pct,lunch_green_pct,dinner_green_pct,snacks_green_pct],
     'Yellow': [breakfast_yellow_pct,lunch_yellow_pct,dinner_yellow_pct,snacks_yellow_pct],
     'Red':[breakfast_red_pct,lunch_red_pct,dinner_red_pct, snacks_red_pct]

                  }

d = pd.DataFrame(data=d2, index=['Breakfast','Lunch','Dinner','Snacks']).round(2)
pct_fig = go.Figure()
pct_fig.add_trace(go.Bar(
    y=d.index,
    x=d.Green,
    name='Green',
    orientation='h',
    text=d.Green,
    marker=dict(
        color='rgb(0,255,0)'
    )
))
pct_fig.add_trace(go.Bar(
    y=d.index,
    x=d.Yellow,
    name='Yellow',
    orientation='h',
    text=d.Yellow,
    marker=dict(
        color='rgb(242,242,19)'
    )
))
pct_fig.add_trace(go.Bar(
    y=d.index,
    x=d.Red,
    name='Red',
    orientation='h',
    text=d.Red,
    marker=dict(
        color='rgb(246, 78, 139)'
    )
))
pct_fig.update_layout(barmode='stack')
pct_fig.update_layout(title_text="Calorie Density Breakdown by Meal (%)", title_x=0.5)

### Getting min, max, and default start, end dates for date picker

# min will be the minimum date in calorie df, max will be today's date
min_date = min(calorie_df.Date)
max_date = dt.datetime.today().date()
test_date = (dt.datetime.today()-timedelta(days=7)).date()

# default dates will be one week from today to start, and today to finish
start_date = max((dt.datetime.today()-timedelta(days=7)).date(),min_date)
end_date = dt.datetime.strptime(dt.datetime.today().strftime("%m/%d/%Y"),'%m/%d/%Y').date()

### App layout

app.layout = html.Div([
        # create a div to store each graph
        html.Div([
        dcc.DatePickerRange(id='my-date-range-picker',
    start_date=start_date,
    end_date=end_date,
    calendar_orientation='vertical',
    min_date_allowed = min_date,
    max_date_allowed = max_date
)
        ], style={'text-align':'center'}),
        html.Div([dcc.Graph(id='cal-graph',figure=cal_fig)]),
        html.Div([dcc.Graph(id='weight-graph',figure=weight_fig)]),
        html.Div([dcc.Graph(id='exercise-graph',figure=exercise_fig)]),
        html.Div([dcc.Graph(id='pct-graph',figure=pct_fig)])

])

@app.callback(Output(component_id='cal-graph', component_property='figure'),
              Output(component_id='weight-graph', component_property='figure'),
              Output(component_id='exercise-graph', component_property='figure'),
              Output(component_id='pct-graph', component_property='figure'),
              [Input(component_id='my-date-range-picker',component_property='start_date')],
               [Input(component_id='my-date-range-picker',component_property='end_date')])

def update_cal_graph(start_date,end_date):

    start_date = dt.datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end_date,'%Y-%m-%d').date()
    calorie_df = pd.read_excel('./data_df.xlsx', 'calorie_df',converters = {'Date':dt.datetime.date}).fillna(0)
    calorie_df = calorie_df[(calorie_df.Date>=start_date) & (calorie_df.Date<=end_date)]

    calorie_df['Daily_Green'] = calorie_df.Breakfast_Green+calorie_df.Lunch_Green+calorie_df.Dinner_Green+calorie_df.Snacks_Green
    calorie_df['Daily_Yellow'] = calorie_df.Breakfast_Yellow+calorie_df.Lunch_Yellow+calorie_df.Dinner_Yellow+calorie_df.Snacks_Yellow
    calorie_df['Daily_Red'] = calorie_df.Breakfast_Red+calorie_df.Lunch_Red+calorie_df.Dinner_Red+calorie_df.Snacks_Red

    cal_fig = go.Figure()
    cal_fig.add_trace(go.Bar(
        y=calorie_df.Daily_Green,
        x=calorie_df.Date,
        name='Green',
        text=calorie_df.Daily_Green,
        marker=dict(
            color='rgb(0,255,0)'
        )
    ))
    cal_fig.add_trace(go.Bar(
        y=calorie_df.Daily_Yellow,
        x=calorie_df.Date,
        name='Yellow',
        text=calorie_df.Daily_Yellow,
        marker=dict(
            color='rgb(242,242,19)'
        )
    ))
    cal_fig.add_trace(go.Bar(
        y=calorie_df.Daily_Red,
        x=calorie_df.Date,
        name='Red',
        text=calorie_df.Daily_Red,
        marker=dict(
            color='rgb(246, 78, 139)'
        )
    ))
    cal_fig.update_layout(barmode='stack')
    cal_fig.update_layout(title_text='Daily Calorie and Calorie Density Breakdown', title_x=0.5)
    cal_fig.update_xaxes(fixedrange=True,tickformat="%m/%d/%Y")
    cal_fig.update_xaxes(dtick=86400000)
    cal_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))



    ### weight plot

    weight_df = pd.read_excel('./data_df.xlsx', 'weight_df',converters = {'Date':dt.datetime.date})
    weight_df = weight_df[(weight_df.Date>=start_date) & (weight_df.Date<=end_date)]
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
    weight_fig.update_xaxes(dtick=86400000)
    weight_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))

    ### exercise plot

    exercise_df = pd.read_excel('./data_df.xlsx','exercise_df', converters = {'Date':dt.datetime.date})
    exercise_df = exercise_df[(exercise_df.Date>=start_date) & (exercise_df.Date<=end_date)]

    exercise_fig = px.line(exercise_df, x="Date", y="Steps",markers=True)
    exercise_fig.update_layout(yaxis_range=[0,25000])
    exercise_fig.update_layout(title_text="Steps", title_x=0.5)
    exercise_fig.add_hline(y=10000,line=dict(color='royalblue', width=4, dash='dot'))
    annotation = {
        'xref': 'paper',
        'yref': 'paper',
        'x': 0.05,
        'y': 0.45,
        'text': 'Goal steps: 10,000',
        'showarrow': False,
        'arrowhead': 0,
    }

    exercise_fig.update_layout({'annotations': [annotation]})
    exercise_fig.update_xaxes(dtick=86400000)
    exercise_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))

    ### calorie breakdown chart

    breakfast_total = sum(calorie_df.Breakfast_Green+calorie_df.Breakfast_Yellow+calorie_df.Breakfast_Red)
    if breakfast_total:
        breakfast_green_pct = 100*sum(calorie_df.Breakfast_Green)/breakfast_total
        breakfast_yellow_pct = 100*sum(calorie_df.Breakfast_Yellow)/breakfast_total
        breakfast_red_pct = 100*sum(calorie_df.Breakfast_Red)/breakfast_total
    else:
        breakfast_green_pct,breakfast_yellow_pct,breakfast_red_pct =0,0,0

    lunch_total = sum(calorie_df.Lunch_Green+calorie_df.Lunch_Yellow+calorie_df.Lunch_Red)
    if lunch_total:
        lunch_green_pct = 100*sum(calorie_df.Lunch_Green)/lunch_total
        lunch_yellow_pct = 100*sum(calorie_df.Lunch_Yellow)/lunch_total
        lunch_red_pct = 100*sum(calorie_df.Lunch_Red)/lunch_total
    else:
        lunch_green_pct,lunch_yellow_pct,lunch_red_pct=0,0,0

    dinner_total = sum(calorie_df.Dinner_Green+calorie_df.Dinner_Yellow+calorie_df.Dinner_Red)
    if dinner_total:
        dinner_green_pct = 100*sum(calorie_df.Dinner_Green)/dinner_total
        dinner_yellow_pct = 100*sum(calorie_df.Dinner_Yellow)/dinner_total
        dinner_red_pct = 100* sum(calorie_df.Dinner_Red)/dinner_total
    else:
        dinner_green_pct,dinner_yellow_pct,dinner_red_pct=0,0,0

    snack_total = sum(calorie_df.Snacks_Green+calorie_df.Snacks_Yellow+calorie_df.Snacks_Red)
    if snack_total:
        snacks_green_pct = 100*sum(calorie_df.Snacks_Green)/snack_total
        snacks_yellow_pct = 100*sum(calorie_df.Snacks_Yellow)/snack_total
        snacks_red_pct = 100*sum(calorie_df.Snacks_Red)/snack_total
    else:
        snacks_green_pct,snacks_yellow_pct,snacks_red_pct=0,0,0

    d2= {'Green': [breakfast_green_pct,lunch_green_pct,dinner_green_pct,snacks_green_pct],
         'Yellow': [breakfast_yellow_pct,lunch_yellow_pct,dinner_yellow_pct,snacks_yellow_pct],
         'Red':[breakfast_red_pct,lunch_red_pct,dinner_red_pct, snacks_red_pct]

                      }

    d = pd.DataFrame(data=d2, index=['Breakfast','Lunch','Dinner','Snacks']).round(2)
    pct_fig = go.Figure()
    pct_fig.add_trace(go.Bar(
        y=d.index,
        x=d.Green,
        name='Green',
        orientation='h',
        text=d.Green,
        marker=dict(
            color='rgb(0,255,0)'
        )
    ))
    pct_fig.add_trace(go.Bar(
        y=d.index,
        x=d.Yellow,
        name='Yellow',
        orientation='h',
        text=d.Yellow,
        marker=dict(
            color='rgb(242,242,19)'
        )
    ))
    pct_fig.add_trace(go.Bar(
        y=d.index,
        x=d.Red,
        name='Red',
        orientation='h',
        text=d.Red,
        marker=dict(
            color='rgb(246, 78, 139)'
        )
    ))
    pct_fig.update_layout(barmode='stack')
    pct_fig.update_layout(title_text="Calorie Density Breakdown by Meal (%)", title_x=0.5)

    return cal_fig,weight_fig,exercise_fig,pct_fig


# run app
if __name__=="__main__":
    app.run_server()
