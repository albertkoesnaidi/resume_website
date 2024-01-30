import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/resume')

def layout():
    return html.Div([
            dbc.Row([
                dbc.Col([dcc.Markdown(children=[''], id='headline_cv')],xs=6,sm=6, md=6, lg=5, xl=5,xxl=5),
                dbc.Col([dcc.Markdown([" "])]),
                dbc.Col([dcc.RadioItems(['English', 'Deutsch'], 'English', inline=True, inputStyle={"margin-left":"15px", "margin-right":"5px"} ,style={"margin-top":"5px"}, id='ri_temp')],xs=5,sm=5, md=5, lg=3, xl=3,xxl=3),

            ]),
            html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ], style={'margin-top':"40px"}),html.Div([
            dbc.Row([
                dbc.Col([], width=4),
                dbc.Col([
                    dbc.Row([dcc.Markdown(children=['Name : Albert Sugiarta Koesnaidi'])]),
                    dbc.Row([dcc.Markdown(children='', id='md_age')]),
                    dbc.Row([dcc.Markdown(children='', id='md_nationality')]),
                    dbc.Row([dcc.Markdown(children='', id='md_phone')]),
                    dbc.Row([dcc.Markdown(children=['E-Mail : koesnaidialbert@gmail.com'])]),
                ]),
                dbc.Col([], width=2)
            ]), html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ]), html.Div([
            dbc.Row([
                dbc.Col([dcc.Markdown(children='', id='md_workexp')], width=5),
                dbc.Col([]),
                dbc.Col([])
            ]),
            dbc.Row([
                dbc.Col([dbc.CardImg(src='../assets/logo-ariane.png', top=True, style={"height":"6rem", "width":"8rem"})],xs=12,sm=12, md=12, lg=3, xl=3,xxl=3),
                dbc.Col([dcc.Markdown(children='', id='text_ariane', style={'margin-top':'30px'})], xs=12,sm=12, md=12, lg=9, xl=9,xxl=9)
            ]), html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ]), html.Div([
            dbc.Row([
                dbc.Col([dcc.Markdown(children='', id='md_sidejob')], width=6),
                dbc.Col([]),
                dbc.Col([])
            ]),
            dbc.Row([
                dbc.Col([dbc.CardImg(src='../assets/kassel.png', top=True, style={"height":"6rem", "width":"12rem"})],xs=12,sm=12, md=12, lg=3, xl=3,xxl=3),
                dbc.Col([dcc.Markdown(children='', id='text_kassel_1', style={'margin-top':'30px'})], xs=12,sm=12, md=12, lg=9, xl=9,xxl=9)
            ]), dbc.Row([
                dbc.Col([dbc.CardImg(src='../assets/kassel.png', top=True, style={"height":"6rem", "width":"12rem"})],xs=12,sm=12, md=12, lg=3, xl=3,xxl=3),
                dbc.Col([dcc.Markdown(children='', id='text_kassel_2', style={'margin-top':'30px'})], xs=12,sm=12, md=12, lg=9, xl=9,xxl=9)
            ]), dbc.Row([
                dbc.Col([dbc.CardImg(src='../assets/rom.png', top=True, style={"height":"6rem", "width":"12rem"})],xs=12,sm=12, md=12, lg=3, xl=3,xxl=3),
                dbc.Col([dcc.Markdown(children='', id='text_rom', style={'margin-top':'30px'})], xs=12,sm=12, md=12, lg=9, xl=9,xxl=9)
            ]), dbc.Row([
                dbc.Col([dbc.CardImg(src='../assets/fichtner.png', top=True, style={"height":"6rem", "width":"12rem"})],xs=12,sm=12, md=12, lg=3, xl=3,xxl=3),
                dbc.Col([dcc.Markdown(children='', id='text_fichtner', style={'margin-top':'30px'})], xs=12,sm=12, md=12, lg=9, xl=9,xxl=9)
            ]), html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ]), html.Div([
            dbc.Row([
                dbc.Col([dcc.Markdown(children='', id='md_education')], width=5),
                dbc.Col([])
            ]), dbc.Row([
                dbc.Col([dbc.CardImg(src='../assets/kassel.png', top=True, style={"height":"6rem", "width":"12rem"})],xs=12,sm=12, md=12, lg=3, xl=3,xxl=3),
                dbc.Col([dcc.Markdown(children='', id='text_edu_kassel', style={'margin-top':'30px'})], xs=12,sm=12, md=12, lg=9, xl=9,xxl=9)
            ]), 
            dbc.Row([
                dbc.Col([dbc.CardImg(src='../assets/biberach.png', top=True, style={"height":"6rem", "width":"12rem"})],xs=12,sm=12, md=12, lg=3, xl=3,xxl=3),
                dbc.Col([dcc.Markdown(children='', id='text_edu_biberach', style={'margin-top':'30px'})], xs=12,sm=12, md=12, lg=9, xl=9,xxl=9)
            ]),
            dbc.Row([
                dbc.Col([dbc.CardImg(src='../assets/konstanz.png', top=True, style={"height":"6rem", "width":"12rem"})],xs=12,sm=12, md=12, lg=3, xl=3,xxl=3),
                dbc.Col([dcc.Markdown(children='', id='text_edu_konstanz', style={'margin-top':'30px'})], xs=12,sm=12, md=12, lg=9, xl=9,xxl=9)
            ])
        ])

@callback(
    Output(component_id='headline_cv', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_headline_cv(ri_val):
    if ri_val == 'English':
        return '### __Curriculum Vitae__'
    else:
        return '### __Lebenslauf__'

@callback(
    Output(component_id='md_age', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_age(ri_val):
    if ri_val == 'English':
        return 'Birthdate and Place : 04-16-1989 / Surabaya, Indonesia'
    else:
        return 'Geburtstag / -ort : 16.04.1989 / Surabaya Indonesien'
    
@callback(
    Output(component_id='md_nationality', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_nationality(ri_val):
    if ri_val == 'English':
        return 'Nationality : Indonesia'
    else:
        return 'Staatsangehörigkeit: : Indonesisch'

@callback(
    Output(component_id='md_phone', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_phone(ri_val):
    if ri_val == 'English':
        return 'Mobile : +6281-733-9551'
    else:
        return 'Mobil : +6281-733-9551'
    
@callback(
    Output(component_id='md_workexp', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_workexp(ri_val):
    if ri_val == 'English':
        return '### Working Experience'
    else:
        return '### Berufserfahrung'

@callback(
    Output(component_id='text_ariane', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_ariane(ri_val):
    if ri_val == 'English':
        return 'Working as a project and montage planner for a solar and heatpump water heater since 2018'
    else:
        return 'Seit 2018 arbeite als Projekt- und Montageplaner für einen Solar- und Wärmepumpen-Wassererhitzer.'
    
    
@callback(
    Output(component_id='md_sidejob', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_sidejob(ri_val):
    if ri_val == 'English':
        return '### Practical Experience / Part-Time Work'
    else:
        return '### Praktische Erfahrung / Nebentätigkeiten'

@callback(
    Output(component_id='text_kassel_1', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_kassel(ri_val):
    if ri_val == 'English':
        return '__12/2017 - 04/2018__ as an academic assistant in the Institute of Thermal Energy in the Thermal Sorption Group'
    else:
        return '__12.2017 - 04.2018__ als Wissenschaftliche Hilfskraft des Instituts thermische Energietechnik in der Gruppe Sorptionswärme'
    
@callback(
    Output(component_id='text_kassel_2', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_kassel2(ri_val):
    if ri_val == 'English':
        return '__06/2016 - 11/2017__ as an academic assistant in the Institute of Thermal Energy in the Process Heat Group'
    else:
        return '__06.2016 - 11.2017__ als Wissenschaftliche Hilfskraft des Instituts thermische Energietechnik In der Gruppe Solarthermie für Prozesswärme'

@callback(
    Output(component_id='text_rom', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_rom(ri_val):
    if ri_val == 'English':
        return '__08/2014 - 02/2015__ as a Scientific assistant for the Passive House Office Building Energon project in Ulm'
    else:
        return '__08.2014 - 02.2015__ als Wissenschaftlicher Mitarbeiter für das Projekt Passivhaus-Bürogebäude Energon in Ulm'

@callback(
    Output(component_id='text_fichtner', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_fichtner(ri_val):
    if ri_val == 'English':
        return "__02/2012 - 07/2012__ Internship as part of the practical phase of the bachelor's degree in the Department of Energy Economics"
    else:
        return '__02.2012 - 07.2012__ Praktikum im Rahmen der Praxisphase des Bachelorstudiums in der Abteilung der Energiewirtschaft'

@callback(
    Output(component_id='md_education', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_education(ri_val):
    if ri_val == 'English':
        return '### Education'
    else:
        return '### Studium'

@callback(
    Output(component_id='text_edu_kassel', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_edu_kassel(ri_val):
    if ri_val == 'English':
        return '__03/2015 - 04/2018__ University of Kassel, Master of Science Regenerative Energy and Energy Efficiency'
    else:
        return '__03.2015 - 04.2018__ Universität Kassel, Master of Science Regenerative Energien und Energieeffizienz'

@callback(
    Output(component_id='text_edu_biberach', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_edu_biberach(ri_val):
    if ri_val == 'English':
        return '__03/2010 - 07/2014__ University of Applied Science Biberach, Bachelor of Engineering Energiesystem'
    else:
        return '__03.2010 - 07.2014__ Hochschule Biberach, Bachelor of Engineering Energiesysteme'

@callback(
    Output(component_id='text_edu_konstanz', component_property='children'),
    Input(component_id='ri_temp', component_property='value'),
)
def update_text_edu_konstanz(ri_val):
    if ri_val == 'English':
        return '__02/2009 - 03/2010__ University of Applied Science Konstanz, Preparatory Course for University in Germany'
    else:
        return '__02.2009 - 03.2010__ Hochschule Konstanz, Ausländer Studienkolleg'

