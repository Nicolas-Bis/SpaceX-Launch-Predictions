# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Get unique launch sites from the DataFrame
launch_sites = spacex_df['Launch Site'].unique()

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),
    
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i} Kg' for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),
    
    html.Br(),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback function to update the pie chart based on selected dropdown value
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Group data by Launch Site and calculate the total success count for each site
        grouped_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        # Create a pie chart showing the total success counts for each launch site
        fig = px.pie(grouped_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By All Sites')
        return fig
    else:
        # Filter the data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Create a pie chart for the filtered site showing success vs. failure
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# TASK 4: Callback function to update the scatter plot based on selected site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(entered_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        # Create a scatter plot for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        # Filter the data for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Create a scatter plot for the filtered site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
