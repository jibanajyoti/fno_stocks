import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = pd.read_csv('datasets/MW-SECURITIES-IN-F&O-21-Aug-2023.csv')

# Load the CSV file into a DataFrame
file_path = 'datasets/MW-SECURITIES-IN-F&O-21-Aug-2023.csv'
stock_data = pd.read_csv(file_path)

# Clean up the column names
stock_data.columns = stock_data.columns.str.strip()  # Remove leading/trailing spaces

# Data preprocessing
stock_data['VALUE'] = stock_data['VALUE'].str.replace(',', '').astype(float)

# Replace '-' characters with NaN in %CHNG column
stock_data['%CHNG'] = stock_data['%CHNG'].replace('-', pd.NA)

stock_data['%CHNG'] = pd.to_numeric(stock_data['%CHNG'])

fig = px.treemap(
            stock_data,
            path=['SYMBOL'],
            values='VALUE',
            color='%CHNG',  
            color_continuous_scale='RdYlGn',  
            hover_data=['%CHNG'], 
            title='F&O Stocks Treemap by value and %chng')

app.layout = html.Div([

    dcc.Graph(
        id='treemap',
        figure=fig
        
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)