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
# server = Flask(__name__)
server=app.server
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

df = pd.read_sql_table('nutrition_table', con=db.engine).fillna(0)
df.Date = df.Date.apply(lambda x:dt.datetime.strptime(x,'%Y-%m-%d').date())
for col in df.columns:
    if col=="Weight":
        df[col] = df[col].astype('float')
    elif col!="Date":
        df[col] = df[col].astype('int')

# ------------------------------------------------------------------------------------------------

### calorie plot

df['Daily_Green'] = df.Breakfast_Green+df.Lunch_Green+df.Dinner_Green+df.Snacks_Green
df['Daily_Yellow'] = df.Breakfast_Yellow+df.Lunch_Yellow+df.Dinner_Yellow+df.Snacks_Yellow
df['Daily_Red'] = df.Breakfast_Red+df.Lunch_Red+df.Dinner_Red+df.Snacks_Red

cal_fig = go.Figure()
cal_fig.add_trace(go.Bar(
    y=df.Daily_Green,
    x=df.Date,
    name='Green',
    text=df.Daily_Green,
    marker=dict(
        color='rgb(0,255,0)'
    )
))
cal_fig.add_trace(go.Bar(
    y=df.Daily_Yellow,
    x=df.Date,
    name='Yellow',
    text=df.Daily_Yellow,
    marker=dict(
        color='rgb(242,242,19)'
    )
))
cal_fig.add_trace(go.Bar(
    y=df.Daily_Red,
    x=df.Date,
    name='Red',
    text=df.Daily_Red,
    marker=dict(
        color='rgb(246, 78, 139)'
    )
))
cal_fig.update_layout(barmode='stack')
cal_fig.update_layout(title_text='Daily Calorie and Calorie Density Breakdown', title_x=0.5)


### weight plot

weight_fig = px.line(df, x="Date", y="Weight", title='Weight Over Time',markers=True)
weight_fig.add_hline(y=155,line=dict(color='royalblue', width=4, dash='dot'))
weight_fig.update_layout(yaxis_range=[150,180])
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

exercise_fig = px.line(df, x="Date", y="Steps",markers=True)
exercise_fig.update_layout(yaxis_range=[0,1500])
exercise_fig.update_layout(title_text="Steps", title_x=0.5)

### calorie breakdown chart

breakfast_total = sum(df.Breakfast_Green+df.Breakfast_Yellow+df.Breakfast_Red)
if breakfast_total:
    breakfast_green_pct = 100*sum(df.Breakfast_Green)/breakfast_total
    breakfast_yellow_pct = 100*sum(df.Breakfast_Yellow)/breakfast_total
    breakfast_red_pct = 100*sum(df.Breakfast_Red)/breakfast_total
else:
    breakfast_green_pct,breakfast_yellow_pct,breakfast_red_pct =0,0,0

lunch_total = sum(df.Lunch_Green+df.Lunch_Yellow+df.Lunch_Red)
if lunch_total:
    lunch_green_pct = 100*sum(df.Lunch_Green)/lunch_total
    lunch_yellow_pct = 100*sum(df.Lunch_Yellow)/lunch_total
    lunch_red_pct = 100*sum(df.Lunch_Red)/lunch_total
else:
    lunch_green_pct,lunch_yellow_pct,lunch_red_pct=0,0,0

dinner_total = sum(df.Dinner_Green+df.Dinner_Yellow+df.Dinner_Red)
if dinner_total:
    dinner_green_pct = 100*sum(df.Dinner_Green)/dinner_total
    dinner_yellow_pct = 100*sum(df.Dinner_Yellow)/dinner_total
    dinner_red_pct = 100* sum(df.Dinner_Red)/dinner_total
else:
    dinner_green_pct,dinner_yellow_pct,dinner_red_pct=0,0,0

snack_total = sum(df.Snacks_Green+df.Snacks_Yellow+df.Snacks_Red)
if snack_total:
    snacks_green_pct = 100*sum(df.Snacks_Green)/snack_total
    snacks_yellow_pct = 100*sum(df.Snacks_Yellow)/snack_total
    snacks_red_pct = 100*sum(df.Snacks_Red)/snack_total
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
min_date = min(df.Date)
max_date = dt.datetime.today().date()
test_date = (dt.datetime.today()-timedelta(days=7)).date()

# default dates will be one week from today to start, and today to finish
start_date = max((dt.datetime.today()-timedelta(days=7)).date(),min_date)
end_date = dt.datetime.strptime(dt.datetime.today().strftime("%m/%d/%Y"),'%m/%d/%Y').date()

### App layout

app.layout = html.Div([
        # create a div to store each graph
        html.Div([html.H1('Physical Health Dashboard')],style={'text-align':'center'}),
        html.Div([
        dcc.DatePickerRange(id='my-date-range-picker',
    start_date=start_date,
    end_date=end_date,
    calendar_orientation='vertical',
    min_date_allowed = min_date,
    max_date_allowed = max_date
)
        ], style={'text-align':'center'}),
        html.Div([dcc.Graph(id='weight-graph',figure=weight_fig)]),
        html.Div([dcc.Graph(id='cal-graph',figure=cal_fig)]),
        html.Div([dcc.Graph(id='exercise-graph',figure=exercise_fig)]),
        html.Div([dcc.Graph(id='pct-graph',figure=pct_fig)]),
        html.Div([
            dcc.Input(
                id='adding-rows-name',
                placeholder='Enter a column name...',
                value='',
                style={'padding': 10}
            ),
            html.Button('Add Column', id='adding-columns-button', n_clicks=0)
        ], style={'height': 50}),
        dcc.Interval(id='interval_pg', interval=86400000*7, n_intervals=0),  # activated once/week or when page refreshed
        html.Div(id='postgres_datatable'),
        html.Button('Add Row', id='editing-rows-button', n_clicks=0),
        html.Button('Save to PostgreSQL', id='save_to_postgres', n_clicks=0),

        # Create notification when saving to excel
        html.Div(id='placeholder', children=[]),
        dcc.Store(id="store", data=0),
        dcc.Interval(id='interval', interval=86400000*7),
        html.Div([html.H1('-')], style={'opacity':'0'})
])


## -------------------------------------------------------------------------------------------------
@app.callback(Output('postgres_datatable', 'children'),
              [Input('interval_pg', 'n_intervals')],
              [Input(component_id='my-date-range-picker',component_property='start_date')],
               [Input(component_id='my-date-range-picker',component_property='end_date')])
def populate_datatable(n_intervals,start_date,end_date):
    start_date = dt.datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end_date,'%Y-%m-%d').date()
    df = pd.read_sql_table('nutrition_table', con=db.engine)
    df.Date = df.Date.apply(lambda x:dt.datetime.strptime(x,'%Y-%m-%d').date())
    df = df[(df.Date>=start_date) & (df.Date<=end_date)]
    return [
        dash_table.DataTable(
            id='our-table',
            columns=[{
                         'name': str(x),
                         'id': str(x),
                         'deletable': False,
                     } if x == 'Date'
                     else {
                'name': str(x),
                'id': str(x),
                'deletable': True,
            }
                     for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'}
            # style_cell_conditional=[
            #     {
            #         'if': {'column_id': c},
            #         'textAlign': 'right'
            #     } for c in ['Date']
            # ]

        ),
    ]

@app.callback(
    Output('our-table', 'columns'),
    [Input('adding-columns-button', 'n_clicks')],
    [State('adding-rows-name', 'value'),
     State('our-table', 'columns')],
    prevent_initial_call=True)
def add_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'name': value, 'id': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns


@app.callback(
    Output('our-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('our-table', 'data'),
     State('our-table', 'columns')],
    prevent_initial_call=True)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(
    [Output('placeholder', 'children'),
     Output("store", "data")],
    [Input('save_to_postgres', 'n_clicks'),
     Input("interval", "n_intervals")
     ],
    [State('our-table', 'data'),
     State('store', 'data')],
    prevent_initial_call=True)
def df_to_csv(n_clicks, n_intervals, dataset, s):
    output = html.Plaintext("The data has been saved to your PostgreSQL database.",
                            style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
    no_output = html.Plaintext("", style={'margin': "0px"})

    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if input_triggered == "save_to_postgres":
        s = 6
        pg = pd.DataFrame(dataset)
        pg.to_sql("nutrition_table", con=db.engine, if_exists='replace', index=False)
        return output, s
    elif input_triggered == 'interval' and s > 0:
        s = s - 1
        if s > 0:
            return output, s
        else:
            return no_output, s
    elif s == 0:
        return no_output, s



@app.callback(Output(component_id='cal-graph', component_property='figure'),
              Output(component_id='weight-graph', component_property='figure'),
              Output(component_id='exercise-graph', component_property='figure'),
              Output(component_id='pct-graph', component_property='figure'),
              [Input(component_id='my-date-range-picker',component_property='start_date')],
               [Input(component_id='my-date-range-picker',component_property='end_date')])
def update_cal_graph(start_date,end_date):

    start_date = dt.datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end_date,'%Y-%m-%d').date()

    # df = pd.read_excel('./data_df.xlsx', 'df',converters = {'Date':dt.datetime.date}).fillna(0)

    df = pd.read_sql_table('nutrition_table', con=db.engine).fillna(0)
    df.Date = df.Date.apply(lambda x:dt.datetime.strptime(x,'%Y-%m-%d').date())
    for col in df.columns:
        if col=="Weight":
            df[col] = df[col].astype('float')
        elif col!="Date":
            df[col] = df[col].astype('int')
    # print('start',start_date,type(start_date),'end',end_date,type(end_date),'dates',df.Date[0],type(df.Date[0]))
    df = df[(df.Date>=start_date) & (df.Date<=end_date)]
    df['Daily_Green'] = df.Breakfast_Green+df.Lunch_Green+df.Dinner_Green+df.Snacks_Green
    df['Daily_Yellow'] = df.Breakfast_Yellow+df.Lunch_Yellow+df.Dinner_Yellow+df.Snacks_Yellow
    df['Daily_Red'] = df.Breakfast_Red+df.Lunch_Red+df.Dinner_Red+df.Snacks_Red

    cal_fig = go.Figure()
    cal_fig.add_trace(go.Bar(
        y=df.Daily_Green,
        x=df.Date,
        name='Green',
        text=df.Daily_Green,
        marker=dict(
            color='rgb(0,255,0)'
        )
    ))
    cal_fig.add_trace(go.Bar(
        y=df.Daily_Yellow,
        x=df.Date,
        name='Yellow',
        text=df.Daily_Yellow,
        marker=dict(
            color='rgb(242,242,19)'
        )
    ))
    cal_fig.add_trace(go.Bar(
        y=df.Daily_Red,
        x=df.Date,
        name='Red',
        text=df.Daily_Red,
        marker=dict(
            color='rgb(246, 78, 139)'
        )
    ))
    cal_fig.update_layout(barmode='stack')
    cal_fig.update_layout(title_text='Daily Calorie and Calorie Density Breakdown', title_x=0.5)
    cal_fig.update_xaxes(fixedrange=True,tickformat="%m/%d/%Y")
    # cal_fig.update_xaxes(dtick=86400000)
    cal_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))



    ### weight plot

    weight_fig = px.line(df, x="Date", y="Weight", title='Weight Over Time',markers=True)
    weight_fig.add_hline(y=155,line=dict(color='royalblue', width=4, dash='dot'))
    weight_fig.update_layout(yaxis_range=[150,180])
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
    # weight_fig.update_xaxes(dtick=86400000)
    weight_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))

    ### exercise plot

    exercise_fig = px.line(df, x="Date", y="Steps",markers=True)
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
    # exercise_fig.update_xaxes(dtick=86400000)
    exercise_fig.update_layout(xaxis=dict(tickformat="%m/%d/%Y"))

    ### calorie breakdown chart

    breakfast_total = sum(df.Breakfast_Green+df.Breakfast_Yellow+df.Breakfast_Red)
    if breakfast_total:
        breakfast_green_pct = 100*sum(df.Breakfast_Green)/breakfast_total
        breakfast_yellow_pct = 100*sum(df.Breakfast_Yellow)/breakfast_total
        breakfast_red_pct = 100*sum(df.Breakfast_Red)/breakfast_total
    else:
        breakfast_green_pct,breakfast_yellow_pct,breakfast_red_pct =0,0,0

    lunch_total = sum(df.Lunch_Green+df.Lunch_Yellow+df.Lunch_Red)
    if lunch_total:
        lunch_green_pct = 100*sum(df.Lunch_Green)/lunch_total
        lunch_yellow_pct = 100*sum(df.Lunch_Yellow)/lunch_total
        lunch_red_pct = 100*sum(df.Lunch_Red)/lunch_total
    else:
        lunch_green_pct,lunch_yellow_pct,lunch_red_pct=0,0,0

    dinner_total = sum(df.Dinner_Green+df.Dinner_Yellow+df.Dinner_Red)
    if dinner_total:
        dinner_green_pct = 100*sum(df.Dinner_Green)/dinner_total
        dinner_yellow_pct = 100*sum(df.Dinner_Yellow)/dinner_total
        dinner_red_pct = 100* sum(df.Dinner_Red)/dinner_total
    else:
        dinner_green_pct,dinner_yellow_pct,dinner_red_pct=0,0,0

    snack_total = sum(df.Snacks_Green+df.Snacks_Yellow+df.Snacks_Red)
    if snack_total:
        snacks_green_pct = 100*sum(df.Snacks_Green)/snack_total
        snacks_yellow_pct = 100*sum(df.Snacks_Yellow)/snack_total
        snacks_red_pct = 100*sum(df.Snacks_Red)/snack_total
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
