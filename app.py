import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

url = 'https://raw.githubusercontent.com/meharaz2020/ex/master/CM.xlsx'

# Read Excel file from the URL
df = pd.read_excel(url)

# Calculate CM day wise subscriptions
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Layout for the dashboard
app.layout = html.Div([
    html.H1("Dashboard For Candidate Monetization", style={'textAlign': 'center'}),
    
    dcc.DatePickerRange(
        id='date-range-picker',
        min_date_allowed=df['Purchase Date'].min(),
        max_date_allowed=df['Purchase Date'].max(),
        initial_visible_month=df['Purchase Date'].max(),
        start_date=df['Purchase Date'].min(),
        end_date=df['Purchase Date'].max(),
        display_format='YYYY-MM-DD',
        style={'margin': '20px'}
    ),
    
    dcc.Graph(id='amount-per-package'),
    dcc.Graph(id='gender-per-payment'),
    dcc.Graph(id='payment-gender-distribution')
])

# Callback to update the graphs based on the selected date range
@app.callback(
    [Output('amount-per-package', 'figure'),
     Output('gender-per-payment', 'figure'),
     Output('payment-gender-distribution', 'figure')],
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_graphs(start_date, end_date):
    filtered_df = df[(df['Purchase Date'] >= start_date) & (df['Purchase Date'] <= end_date)]
    
    amount_per_package = filtered_df.groupby('Package Name')['Price'].sum().reset_index()
    grouped_df = filtered_df.groupby('Payment Status')['SEX'].value_counts().reset_index(name='Count')
    
    fig_amount_per_package = px.pie(amount_per_package, values='Price', names='Package Name', title='Total Amount per Package Name')
    fig_gender_per_payment = px.pie(grouped_df, values='Count', names='SEX', title='Total F/M per Payment Status')
    fig_payment_gender_distribution = px.bar(grouped_df, x='Payment Status', y='Count', color='SEX',
                                             title='Payment Type Wise Gender Distribution',
                                             labels={'Payment Status': 'Payment Type', 'Count': 'Count of Gender'})
    
    return fig_amount_per_package, fig_gender_per_payment, fig_payment_gender_distribution

# Running the app
if __name__ == '__main__':
    app.run_server(debug=False)
