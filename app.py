import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample data (you can replace this with your own dataset)
df = pd.DataFrame({
    "X": [1, 2, 3, 4, 5],
    "Y": [10, 15, 13, 18, 20]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Plotly Dash Dashboard"),
    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter(df, x='X', y='Y', title='Scatter Plot')
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)
