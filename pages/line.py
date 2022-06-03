# Bar charts are useful for displaying data that is classified into nominal or ordinal categories.
# A bar chart uses bars to show comparisons between categories of data. A bar chart will always have two axis.
# One axis will generally have numerical values, and the other will describe the types of categories being compared.

import pandas as pd #(version 0.24.2)
from datetime import datetime as dt

import dash         #(version 1.0.0)
from dash.dependencies import Input, Output

from dash import Dash, dcc, html, Input, Output, callback
dash.register_page(__name__)
import plotly       #(version 4.4.1)
import plotly.express as px

df = pd.read_csv("sp_irad_accident.csv")
df['SUBMIT_DATE'] = pd.to_datetime(df['insert_date'])
df.set_index('SUBMIT_DATE', inplace=True)
#-------------------------------------------------------------------------------------
# Drop rows w/ no animals found or calls w/ varied age groups
#df = df[(df['# of Animals']>0) & (df['Age']!='Multiple')]

# Extract month from time call made to Ranger
df['Month'] = pd.to_datetime(df['insert_date'])
df['Month'] = df['Month'].dt.strftime('%m')
df['Month']
df['Crashes']=1

df = df.filter(["crash_type", "Month","Crashes","year",'state','total_dead'], axis=1)
df= df.groupby(['crash_type','Month','year','state','total_dead']).sum().reset_index()
#-------------------------------------------------------------------------------------
layout = html.Div([
 
        #title
        html.Div([
            html.Pre(children= "Line Charts for RBG Accidents",
            style={"text-align": "center", "font-size":"200%", "color":"black"})
                ]),

      
        html.Div(
            children=[
                #Radiobutton 1
                html.Div([
                    html.Label(['X-axis Categories:'],style={"text-align": "center",'font-weight': 'bold'}),
                    dcc.RadioItems(
                        id='xaxis_raditem',
                        options=[
                                {'label': 'Month', 'value': 'Month'},
                                {'label': 'Year', 'value': 'year'}
                        ],
                        value='Month',
                        style={"width": "50%"}
                    )
                ]),

            
                #Radiobutton 2
                html.Div([
                    html.Br(),
                    html.Label(['Y-axis Values:'], style={"text-align": "center",'font-weight': 'bold'}),
                    dcc.RadioItems(
                        id='yaxis_raditem',
                        options=[
                                {'label': '# of people dead', 'value': 'total_dead'},
                                {'label': '# of crashes', 'value': 'Crashes'}
                        ],
                        value='total_dead',
                        style={"width": "50%"}
                    )
                ]),
                #DatePicker
                html.Div([
                html.Br(),
                html.Label(['Choose the Date'],style={"text-align": "center",'font-weight': 'bold'}),
                html.Br(),
                dcc.DatePickerRange(
                id='my-date-picker-range',  # ID to be used for callback
                calendar_orientation='horizontal',  # vertical or horizontal
                day_size=39,  # size of calendar image. Default is 39
                end_date_placeholder_text="Return",  # text that appears when no end date chosen
                with_portal=False,  # if True calendar will open in a full screen overlay portal
                first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                reopen_calendar_on_clear=True,
                is_RTL=False,  # True or False for direction of calendar
                clearable=True,  # whether or not the user can clear the dropdown
                number_of_months_shown=1,  # number of months shown when calendar is open
                min_date_allowed=dt(2021, 2, 22),  # minimum date allowed on the DatePickerRange component
                max_date_allowed=dt(2022, 4, 3),  # maximum date allowed on the DatePickerRange component
                initial_visible_month=dt(2021, 2, 22),  # the month initially presented when the user opens the calendar
                start_date=dt(2021, 2, 22).date(),
                end_date=dt(2022, 4, 3).date(),
                display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
                month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                minimum_nights=2,  # minimum number of days between start and end date

                persistence=True,
                persisted_props=['start_date'],
                persistence_type='session',  # session, local, or memory. Default is 'local'

                updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
                )
            ])
        ]),
    
        html.Div([
            dcc.Graph(id='line_graph')
            ])
])
#-------------------------------------------------------------------------------------
@callback(
    Output(component_id='line_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
    Input(component_id='yaxis_raditem', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')]
)

def update_graph(x_axis, y_axis, start_date, end_date):

    dff = df.loc[start_date:end_date]
    linechart=px.line(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            title=y_axis+': by '+x_axis,
            )

    linechart.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})
    linechart.update_traces(marker_color='black')
    linechart.update_xaxes(type='category')
    linechart.update_xaxes(categoryorder='category ascending')

    return (linechart)

# if __name__ == '__main__':
#     app.run_server(debug=True, port=2000)
