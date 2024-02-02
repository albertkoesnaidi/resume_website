import dash
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SANDSTONE, dbc.icons.BOOTSTRAP])
server = app.server

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About me", href="/")),
        dbc.NavItem(dbc.NavLink('Global Warming', href='/Globalwarming')),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Global Temperature", href='/Temperature'),
                dbc.DropdownMenuItem("CO2-Emission", href="/co2"),
                dbc.DropdownMenuItem("Energy", href="/Energy"),
                
                
            ],
            nav=True,
            in_navbar=True,
            label="Dashboard",
        ),
        dbc.NavItem(dbc.NavLink('Resume', href='/resume')),
        html.A(href='https://github.com/albertkoesnaidi', children=[html.I(className='bi bi-github ps-3', style={'color':'white', 'font-size':'27px'})])
    ],
    brand="Albert Koesnaidi",
    brand_href="/",
    color='dark',
    dark=True,
)

app.layout = dbc.Container([header, dash.page_container], fluid=False)


if __name__ == '__main__':
    app.run_server(debug=False)
