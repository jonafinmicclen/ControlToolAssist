import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Button('Add Point', id='add-button', n_clicks=0),
    html.Button('Remove Point', id='remove-button', n_clicks=0),
    dcc.Dropdown(
        id='interpolation-dropdown',
        options=[
            {'label': 'Linear', 'value': 'linear'},
            {'label': 'Spline', 'value': 'spline'}
        ],
        value='linear',
        style={'width': '200px'}
    )
])

points = {'x': [1, 2, 3, 4, 5], 'y': [10, 5, 20, 15, 25]}

@app.callback(
    Output('graph', 'figure'),
    [Input('add-button', 'n_clicks'),
     Input('remove-button', 'n_clicks'),
     Input('interpolation-dropdown', 'value')]
)
def update_graph(add_clicks, remove_clicks, interpolation_method):
    if add_clicks > 0:
        x, y = np.random.rand(2) * 10  # Randomly generate x, y coordinates for the new point
        points['x'].append(x)
        points['y'].append(y)

    if remove_clicks > 0 and len(points['x']) > 1:
        points['x'].pop()
        points['y'].pop()

    fig = {
        'data': [
            {'x': points['x'], 'y': points['y'], 'type': 'scatter', 'mode': 'markers+lines', 'name': 'Data Points'},
        ],
        'layout': {
            'title': f'Interpolation: {interpolation_method}',
            'xaxis': {'title': 'X-axis'},
            'yaxis': {'title': 'Y-axis'},
        }
    }

    if interpolation_method == 'spline':
        fig['data'].append({'x': np.linspace(min(points['x']), max(points['x']), 100),
                            'y': np.interp(np.linspace(min(points['x']), max(points['x']), 100),
                                           points['x'], points['y']),
                            'type': 'scatter', 'mode': 'lines', 'name': 'Interpolation'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
