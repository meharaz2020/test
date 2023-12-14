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
# Calculate total earnings where Payment Status is 'S'
total_earnings = df[df['Payment Status'] == 'S']['Price'].sum()

# Format the total earnings to include only the BDT symbol
total_earnings_formatted = f"৳{total_earnings:,.0f}"  # Assuming 'total_earnings' is in integer format


# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server


# Layout for the dashboard
app.layout = html.Div([
    html.H1("Dashboard For Candidate Monetization", style={'textAlign': 'center'}),
    
    html.Div([
        html.H3(f"Total Earnings : {total_earnings_formatted}", style={'textAlign': 'center', 'margin-bottom': '20px'})
    ]),
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
    dcc.Graph(id='payment-gender-distribution'),
    dcc.Graph(id='price-per-payment-status'),
    dcc.Graph(id='price-per-package'),
    dcc.Graph(id='price-per-method') 
])

# Callback to update the graphs based on the selected date range
@app.callback(
    [Output('amount-per-package', 'figure'),
     Output('gender-per-payment', 'figure'),
     Output('payment-gender-distribution', 'figure'),
     Output('price-per-payment-status', 'figure'),
     Output('price-per-package', 'figure'),  # New output for Package Name wise total price
     Output('price-per-method', 'figure')],  # New output for Package Name wise total price
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
    
    # New graph calculation for Price per Payment Status
    price_per_payment_status = filtered_df.groupby('Payment Status')['Price'].sum().reset_index()
    fig_price_per_payment_status = px.bar(price_per_payment_status, x='Payment Status', y='Price',
                                          title='Total Price per Payment Status',
                                          labels={'Payment Status': 'Payment Status', 'Price': 'Total Price'})
    
    # New graph calculation for Price per Package Name
    price_per_package = filtered_df.groupby('Package Name')['Price'].sum().reset_index()
    fig_price_per_package = px.bar(price_per_package, x='Package Name', y='Price',
                                   title='Total Price per Package Name',
                                   labels={'Package Name': 'Package Name', 'Price': 'Total Price'})
     # New graph calculation for Price per Payment Method

    price_per_Method = filtered_df.groupby('Payment Method')['Price'].sum().reset_index()
    fig_price_per_Method = px.bar(price_per_Method, x='Payment Method', y='Price',
                                   title='Total Price per Payment Method',
                                   labels={'Payment Method': 'Payment Method', 'Price': 'Total Price'})
    
    return fig_amount_per_package, fig_gender_per_payment, fig_payment_gender_distribution, fig_price_per_payment_status, fig_price_per_package,fig_price_per_Method

# Running the app
if __name__ == '__main__':
    app.run_server(debug=False)
