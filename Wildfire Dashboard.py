import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from dash import no_update
import datetime as dt

#Create app
app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

#Read the wildfire data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year

#Layout of the dashboard
#Add the title to the dashboard
app.layout = html.Div(children=[html.H1(children='Wildfire Analysis Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),
                                        #Add the radio items and a dropdown right below the first inner division
                                #Outer division starts here        
                                html.Div([ #First inner division for adding dropdown helper text for selectred drive wheels
                                    html.Div([html.H2('Select Region:', style={'margin-right': '2em'}),
                                              #radio items to select the region
                                                    dcc.RadioItems([{"label":"New South Wales","value": "NSW"},
                                    {"label":"Northern Territory","value": "NT"},
                                    {"label":"Queensland","value": "QL"},
                                    {"label":"South Australia","value": "SA"},
                                    {"label":"Tasmania","value": "TA"},
                                    {"label":"Victoria","value": "VI"},
                                    {"label":"Western Australia","value": "WA"}],"NSW", id='region',inline=True)]),
                                    #dropdown to select the year
                                    html.Div([html.H2('Select Year:', style={'margin-right': '2em'}),
                                              dcc.Dropdown(df.Year.unique().tolist(), #years available in the dataset
                                                           value=2005, id='year')], style={'width': '40%', 'padding-left': '2em'}), 
                                                           #add two empty divisions to the outer division to hold the graphs
                                                           #second inner division for adding 2 inner divisions for 2 output graphs
                                                           html.Div([html.Div([], id='plot1'),
                                                                     html.Div([], id='plot2')], style={'display': 'flex'}),
                                #outer division ends here
                                ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
])
#layout ends here
                                                        
#Output and input components inside the app.callback decorator 
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
               [Input(component_id='region', component_property='value'),
                Input(component_id='year', component_property='value')])

#add callback function
def reg_year_display(input_region, input_year):
    #dataframe operations to filter the data based on the input region and year
    region_data = df[df['Region'] == input_region]
    year_data = region_data[region_data['Year'] == input_year]

    #month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    year_data['Month'] = pd.Categorical(year_data['Month'], categories=month_order, ordered=True)

    #plot 1: Monthly Average Estimated Fire Area
    est_data = year_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month', title='{}: Monthly Average Estimated Fire Area in year {}'.format(input_region, input_year))
    
    #plot 2: Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = year_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count', title='{}: Monthly Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region, input_year))
    
    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

if __name__ == '__main__':
        app.run(debug=True)