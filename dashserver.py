
import dash
import dash_html_components as html
import dash_core_components as dcc
from flaskserver import server


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Configure Dash App
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets,
    routes_pathname_prefix='/dash/'
)


# app.layout = html.Div("My Dash app")
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])
# app.layout = html.Div([
#    html.Div(id='content'),
#    dcc.Location(id='location', refresh=False),
#    html.Div(dt.DataTable(rows=[{}]), style={‘display’: ‘none’})
# ])
if __name__ == '__main__':
    app.run_server(debug=True)

