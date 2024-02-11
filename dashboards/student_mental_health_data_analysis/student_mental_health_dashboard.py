import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

all_data = pd.read_csv('csv/student_mental_health.csv')
feature_importance = pd.read_csv('csv/feature_importance.csv')
classifier_results = pd.read_csv('csv/random_forest_classifier_results.csv')
mse = None
with open('csv/randforestreg_mse', 'r') as mean_squared_error:
    mse = float(mean_squared_error.read())

app.layout = html.Div([
    html.H1('Student mental health analysis'),
    html.Div(id = 'output_container', children = []),
    html.Div(id = 'tmp')
])

@app.callback(
    Output(component_id = 'output_container', component_property = 'children'),
    [Input(component_id = 'tmp', component_property = 'value')]
)
def update_layout():
    return all_data

if __name__ == '__main__':
    app.run_server(debug = True)
