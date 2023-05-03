# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 08:18:58 2023

@author: CH
"""

import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output

spacex_df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
spacex_df




app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Launch Site Dashboard'),




   dcc.Graph(id='site-pie-chart'),
    
    
    html.Div(children='''
        Select a launch site:
    '''),
    
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A 3', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        searchable=True
    ),
    
    
    

    dcc.Graph(id='payload-scatter-chart'),

    
    
    
    
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 1000)},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),
    
   
    
])
             
# Define callback function to update pie chart
@app.callback(
    Output('site-pie-chart', 'figure'),
    [dash.dependencies.Input('site-dropdown', 'value'),
     dash.dependencies.Input('payload-slider', 'value')])
# Function decorator to specify function input and output

def get_pie_chart(site_dropdown, payload_range):
    if site_dropdown == 'ALL':
        data = spacex_df.groupby(['Launch Site', 'class']).size().reset_index(name='Counts')
        fig = px.pie(data, values='Counts', names='Launch Site', color='Launch Site', 
                     title='Total Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        data = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='Counts')
        fig = px.pie(data, values='Counts', names='class', color='class', 
                     title='Success Rate of {}'.format(site_dropdown))
    return fig

@app.callback(dash.dependencies.Output('payload-scatter-chart', 'figure'),
              [dash.dependencies.Input('site-dropdown', 'value'),
               dash.dependencies.Input('payload-slider', 'value')])
         
     
       
def update_scatter_chart(site_dropdown, payload_range):
   filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                           (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
   if site_dropdown != 'ALL':
       filtered_df = filtered_df[filtered_df['Launch Site'] == site_dropdown]
   fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version')
   return fig    
        
     
        
     
        
     
        
     
        
     
        
     
        
     
# def update_pie_chart(site):
#     if site == 'ALL':
#         df = spacex_df.groupby(['Launch Site']).size().reset_index(name='class count')
#         fig = px.pie(df, values='class count', names='Launch Site', title='Total Launches by Site')
#     else:
#         df = spacex_df[spacex_df['Launch Site'] == site].groupby(['Class']).size().reset_index(name='class count')
#         fig = px.pie(df, values='class count', names='Class', title='Total Launches by Class for {}'.format(site))
#     return fig   
           
             

# Run App
if __name__ == '__main__':
    app.run_server()
    # try:
    #     app.run_server(debug=True)
    # except Exception as e:
    #     print("Error: {}".format(str(e)))
