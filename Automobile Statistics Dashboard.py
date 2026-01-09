import dash
#import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

#load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

#initialize the app
app = dash.Dash(__name__)

#set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

#list of years
year_list = [i for i in range(1980, 2024, 1)]

#app layout
app.layout = html.Div([
    #add title to the dashboard
    html.H1("Automobile Sales Data Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    #add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id = 'dropdown-statistics',
            options = dropdown_options,
            value = 'Select Statistics',
            placeholder = 'Select a report type'
        )
    ]),
    html.Div(dcc.Dropdown(
        id = 'select-year',
        options = [{'label': i, 'value': i} for i in year_list],
        value = 'Select-year'
        )),
    html.Div([
        html.Div(id = 'output-container', className = 'chart-grid', style={'display': 'flex'}),])
])

#callback function for input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

#callback function for plotting 
@app.callback(
    Output(component_id = 'output-container', component_property = 'children'),
    [Input(component_id = 'dropdown-statistics', component_property = 'value'),
     Input(component_id = 'select-year', component_property = 'value')]
)

def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        #filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        #create and display graphs for Recession Report Statistics
        #plot 1: Automobile Sales Fluctuations during Recession Periods (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure = px.line(yearly_rec, x = 'Year', y = 'Automobile_Sales', title = 'Automobile Sales Fluctuations during Recession Periods (year wise)')
        )

        #plot 2: Average Number of Vehicles Sold by Vehicle Type during Recession Periods
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure = px.bar(average_sales, x = 'Vehicle_Type', y = 'Automobile_Sales', title = 'Average Number of Vehicles Sold by Vehicle Type during Recession Periods')
        )

        #plot 3: Pie chart for Total Expenditure Share by Vehicle Type during Recession Periods
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure = px.pie(exp_rec, values = 'Advertising_Expenditure', names = 'Vehicle_Type', title = 'Total Expenditure Share by Vehicle Type during Recession Periods')
        )

        #plot 4: Bar chart for the Effect of Unemployment Rate on Automobile Sales and Vehicle Type during Recession Periods
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure = px.bar(unemp_data, x = 'unemployment_rate', y = 'Automobile_Sales', color = 'Vehicle_Type', barmode = 'group', title = 'Effect of Unemployment Rate on Automobile Sales and Vehicle Type during Recession Periods')
        )

        return [
            html.Div(className = 'chart-item', children = [html.Div(children = R_chart1), html.Div(children = R_chart2)], style={'width': '50%', 'display': 'inline-block'}),
            html.Div(className = 'chart-item', children = [html.Div(children = R_chart3), html.Div(children = R_chart4)], style={'width': '50%', 'display': 'inline-block'})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]

        #plot 1: Yearly Automobile Sales Trend
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure = px.line(yas, x = 'Year', y = 'Automobile_Sales', title = 'Yearly Automobile Sales Trend')
        )

        #plot 2: Total Monthly Automobile Sales
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure = px.line(mas, x = 'Month', y = 'Automobile_Sales', title = 'Total Monthly Automobile Sales')
        )

        #plot 3: Bar chart for Average Number of Vehicles sold During the Given Year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure = px.bar(avr_vdata, x = 'Vehicle_Type', y = 'Automobile_Sales', title = 'Average Number of Vehicles sold During the Year {}'.format(input_year))
        )

        #plot 4: Total Advertising Expenditure by Vehicle Type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure = px.pie(exp_data, values = 'Advertising_Expenditure', names = 'Vehicle_Type', title = 'Total Advertising Expenditure by Vehicle Type in the Year {}'.format(input_year))
        )
    
        return [
        html.Div(className = 'chart-item', children = [html.Div(children = Y_chart1), html.Div(children = Y_chart2)], style={'width': '50%', 'display': 'inline-block'}),
        html.Div(className = 'chart-item', children = [html.Div(children = Y_chart3), html.Div(children = Y_chart4)], style={'width': '50%', 'display': 'inline-block'})
        ]

    else:
        return None

#run the app
if __name__ == '__main__':
        app.run(debug=True)