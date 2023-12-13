
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

url = 'https://raw.githubusercontent.com/meharaz2020/ex/master/CM.xlsx'

# Read Excel file from the URL
df = pd.read_excel(url)
# Calculating grouped data for the pie charts
grouped_df = df.groupby('Payment Status')['SEX'].value_counts().reset_index(name='Count')
amount_per_package = df.groupby('Package Name')['Price'].sum().reset_index()

# Initializing the Dash app
app = dash.Dash(__name__)
server = app.server
# Creating layout for the dashboard
app.layout = html.Div([
    html.H1("Dashboard For Candidate Monetization", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(figure=px.pie(amount_per_package, values='Price', names='Package Name', title='Total Amount per Package Name'))
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(figure=px.pie(grouped_df, values='Count', names='SEX', title='Total F/M per Payment Status'))
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(figure=px.bar(grouped_df, x='Payment Status', y='Count', color='SEX',
                                 title='Payment Type Wise Gender Distribution',
                                 labels={'Payment Status': 'Payment Type', 'Count': 'Count of Gender'}))
    ], style={'width': '40%', 'display': 'inline-block'}),
    
], style={'textAlign': 'center'})  # Center-align all content within the main Div

# Running the app
if __name__ == '__main__':
    app.run_server(debug=False)
