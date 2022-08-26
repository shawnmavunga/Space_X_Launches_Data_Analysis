# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

data = spacex_df[['Launch Site','class']]


# Create a dash application
app = dash.Dash(__name__)
#
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id = 'site-dropdown',
                                            options = [
                                                {'label': 'All Sites', 'value': 'All Sites'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                ],
                                            value='ALL',
                                            placeholder="Launch Sites",
                                            searchable=True    
                                      
                                            ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                        
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                 dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                marks={0:'0 Kg', 10000:'10000 Kg'},
                                                value = [0, 5000]                                             
                                                ),
                                html.Div(id='slider-output-container'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'All Sites':
        fig = px.pie(data, values='class',  
        names='Launch Site', 
        title='The Total Launches by Site')
        return fig
    else:
        df1 = data.groupby(['Launch Site']).value_counts().reset_index(name='count_class')
        df2 = df1[df1['Launch Site'] == entered_site]
        fig = px.pie(df2, values='count_class',
            names='class', 
            title='The Total Launches for the site '+entered_site)   
        return fig   

    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
            )
def get_scatter_chart(site_dropdown, payload_slider):
    data = spacex_df  
    if site_dropdown == 'All Sites':
        fig1 = px.scatter(data[(data['Payload Mass (kg)'] > min(payload_slider)) & (data['Payload Mass (kg)'] < max(payload_slider))], 
                        x="Payload Mass (kg)", y="class", 
                        color="Booster Version",
                        )
        return fig1
    else:
        fig1 = px.scatter(data[(data['Payload Mass (kg)'] > min(payload_slider)) & (data['Payload Mass (kg)'] < max(payload_slider)) & (data['Launch Site'] == site_dropdown)], 
                        x="Payload Mass (kg)", y="class", 
                        color="Booster Version",
                        )
        return fig1  


# Run the app
if __name__ == '__main__':
    app.run_server()