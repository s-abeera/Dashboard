from google_sheets_api import extract_all, extract_spec, append, create_data, retrieve_titles
import time
import importlib
from datetime import date
import datetime
import plotly.express as px

import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import dash_table
from dash import html
import numpy as np
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import utils.dash_reusable_components as drc
import utils.figures as figs


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]
    # external_stylesheets=[dbc.themes.DARKLY]
)
app.title = "OncoPrecision Dashboard"
server = app.server


cell_lines = {1: 'Cell line 1', 2: 'Cell line 2',
              3: 'Cell line 3', 4: 'Cell line 4'}

cl = retrieve_titles()[0]
data = extract_all('Cell Line 1')

# date_of_input = data['Date']
# growth = data['Growth Days']


app.layout = html.Div(
    children=[
        # .container class is fixed, .container.scalable is scalable
        html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                                    "Cell Data Dashboard",
                                    style={
                                        "text-decoration": "none",
                                        "color": "inherit",
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url("OP-logo.png"))
                            ],
                            href="https://oncoprecision.bio/home",
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="top-line",
                    children=[
                        dcc.Store(id='session', storage_type='session'),
                        html.H6(
                            id="cell-line",
                        ),
                        html.A("Select Cell line", style={
                               'position': 'center'}),
                        dcc.Dropdown(
                            retrieve_titles(),
                            id="dropdown-select-cell-line",
                            clearable=False,
                            searchable=True,
                            value=cl,
                            style={'width': '200px', 'margin': '0rem auto'},
                        ),
                    ]

                ),
                html.Div(
                    id="app-container",
                    # className="row",
                    children=[
                        html.Div(
                            # className="three columns",
                            id="top-column",
                            children=[

                                html.Br(),
                                html.A("Criovial Label"),
                                html.Br(),
                                dcc.Dropdown(
                                    id="dropdown-select-criovial",
                                    clearable=False,
                                    searchable=True,
                                    value='Criovial label',
                                    style={'width': '200px'}
                                ),
                                html.Br(),
                                html.A("Enter new criovial label"),
                                html.Br(),
                                html.A("Leave empty if none", style={
                                       'font-size': '1em', 'color': 'rgb(115, 115, 115)'}),
                                dcc.Input(
                                    id="criovial_label",
                                    type="text",
                                    placeholder="input text",
                                    style={'color': 'rgb(201, 199, 199)'},
                                    className="dash-bootstrap"
                                ),


                                html.Br(),
                                html.A("Date"),
                                html.Br(),
                                dcc.DatePickerSingle(
                                    id='date',
                                    min_date_allowed=date(2000, 1, 1),
                                    initial_visible_month=datetime.datetime.now(),
                                    date=datetime.datetime.now(),
                                    with_portal=True,
                                    day_size=50,
                                    style={'color': 'orange',
                                           'padding': '2rem 2rem'}
                                ),
                                html.Br(),
                                html.A("Cell Passage"),
                                dcc.Input(
                                    id="cell-passage",
                                    type="text",
                                    placeholder="input cell passage",
                                    style={'color': 'rgb(201, 199, 199)'},
                                ),


                                html.Hr(id='line'),

                                html.A("Viability %"),
                                dcc.Input(
                                    id="viability",
                                    type="number",
                                    min=0,
                                    max=100,
                                    placeholder="input percentage",
                                    style={'color': 'rgb(201, 199, 199)'}
                                ),

                                html.Br(),
                                html.A("Concetration (10^6 ml)"),
                                html.Br(),
                                html.A("Initial", style={
                                       'margin': '1rem 1rem 8rem 0rem'}),
                                html.A("Final", style={
                                       'margin': '1rem 1rem 0rem 9rem'}),
                                html.Br(),
                                dcc.Input(
                                    id="initial-conc",
                                    type="number",
                                    min=0,
                                    max=99999,
                                    placeholder="0.0",
                                    style={'width': '80px',
                                           'color': 'rgb(201, 199, 199)'},
                                ),
                                dcc.Input(
                                    id="final-conc",
                                    type="number",
                                    min=0,
                                    max=999999,
                                    placeholder="0.0",
                                    style={'width': '80px',
                                           'color': 'rgb(201, 199, 199)'},
                                ),

                                html.Br(),
                                html.A("Volume"),
                                html.Br(),
                                html.A("Initial", style={
                                       'margin': '1rem 1rem 8rem 0rem'}),
                                html.A("Final", style={
                                       'margin': '1rem 1rem 0rem 9rem'}),
                                html.Br(),
                                dcc.Input(
                                    id="initial-vol",
                                    type="number",
                                    min=0,
                                    max=99999,
                                    placeholder="0.0",
                                    style={'width': '80px',
                                           'color': 'rgb(201, 199, 199)'},
                                ),
                                dcc.Input(
                                    id="final-vol",
                                    type="number",
                                    min=0,
                                    max=999999,
                                    placeholder="0.0",
                                    style={'width': '80px',
                                           'color': 'rgb(201, 199, 199)'},
                                ),

                                html.Br(),
                                html.A("Observation"),
                                html.Br(),
                                dcc.Textarea(
                                    id="observation",
                                    value='Observations...',
                                    style={'width': '250px', 'height': '120px',
                                           'color': 'rgb(201, 199, 199)'},
                                ),
                                html.Br(),
                                html.A("Reactant Information"),
                                html.Br(),
                                dcc.Textarea(
                                    id="reactant-info",
                                    value='Reactant Information...',
                                    style={'width': '250px', 'height': '120px',
                                           'color': 'rgb(201, 199, 199)'},
                                ),
                                html.Br(),
                                html.Button(
                                    "Submit", id="submit-button", n_clicks=0)
                            ],
                        ),

                        html.Div(
                            id="div-graphs",
                            children=[
                                html.Button('Update', id="update-button",
                                            n_clicks=0, style={'width': '120px'}),
                                html.Br(),
                                dcc.Graph(
                                    id="growth-days-graph",
                                ),
                                dash_table.DataTable(
                                    id='data-table',
                                ),
                            ]
                        ),
                    ],
                )
            ],
        ),
    ]
)

criovial = ''
date_of = '12/13/2022'
cp = ''
vi = ''
i_conc = ''
f_conc = ''
i_vol = ''
f_vol = ''
obs = ''
react_info = ''


@app.callback(
    Output("session", "data"),
    [
        Input("dropdown-select-criovial", "value"),
        Input("cell-passage", "value"),
        Input("viability", "value"),
        Input("initial-conc", "value"),
        Input("final-conc", "value"),
        Input("initial-vol", "value"),
        Input("final-vol", "value"),
        Input("observation", "value"),
        Input("reactant-info", "value"),
    ],
)
def update_data(
    criovial_label,
    cell_passage,
    viability,
    initial_conc,
    final_conc,
    initial_vol,
    final_vol,
    observation,
    reactant_info,
):
    criovial = criovial_label
    cp = cell_passage,
    vi = viability
    i_conc = initial_conc
    f_conc = final_conc
    i_vol = initial_vol
    f_vol = final_vol
    obs = observation
    react_info = reactant_info
    return criovial, cp, vi, i_conc, f_conc, i_vol, f_vol, obs, react_info


@app.callback(
    Output("cell-line", "children"),
    [Input("dropdown-select-cell-line", "value")],
)
def update_header(cell_line):
    cl = cell_line
    return [html.H6("Data for " + cl)]


@app.callback(
    Output("dropdown-select-criovial", "options"),
    [Input("dropdown-select-cell-line", "value")],
)
def update_options(cell_line):
    cl = cell_line
    df = extract_all(cl).copy(deep=True)
    opts = list(np.unique(df['Criovial information'].values))
    return [{'label': opt, 'value': opt} for opt in opts]


@app.callback(
    Output("growth-days-graph", "figure"),
    [
        Input("dropdown-select-criovial", "value")],
)
def update_growth_graph(criovial):
    df = extract_all(cl).copy(deep=True)
    if criovial:
        data = df[df['Criovial information'] == criovial]
        date_of_input = data['Date']
        growth = data['Growth Days']
    fig = px.line(x=date_of_input,
                  y=growth, title=f"Growth days for {cl}, criovial label {criovial}")
    fig.update_xaxes(title='Time')

    fig.update_yaxes(title='Growth day')

    return fig


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
