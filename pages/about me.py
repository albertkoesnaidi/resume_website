import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/',order=0)

def layout():
    return html.Div([
    dbc.Row([
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Markdown(children='', id='about_header')],xs=4,sm=4, md=4, lg=4, xl=4,xxl=4),
                dbc.Col([dcc.Markdown([" "])],xs=3,sm=3, md=3, lg=5, xl=5,xxl=5),
                dbc.Col([dcc.RadioItems(['English', 'Deutsch'], 'English', inline=True, inputStyle={"margin-left":"15px", "margin-right":"5px"} ,style={"margin-top":"5px"}, id='ri_about')])
            ]),
            html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ], style={'margin-top':"40px"})
    ]),
    html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="../assets/photo-1.jpg", top=True, style={"height":"25rem", "width":"20rem"}),
                    ],
                    style={"height":"25rem", "width":"15rem","margin-top":"50px"},
                )
                ], xs=6,sm=6, md=6, lg=3, xl=3,xxl=3),
                dbc.Col([
                    dcc.Markdown(children='', id='md_text_abme1'),
                    dcc.Markdown(children='', id='md_text_abme1_1'),
                    dcc.Markdown(children='', id='md_text_abme1_2'),
                    dcc.Markdown(children='', id='md_text_abme1_3'),
                ], style={"margin-top":"175px", "margin-left":"100px"}, xs=6,sm=6, md=6, lg=4, xl=4,xxl=4),
            ]),
            dbc.Row([
                dbc.Col([dcc.Markdown(children='', id="md_text_p1")], style={"margin":"auto", "text-align":'justify'}, xs=9,sm=9, md=9, lg=4, xl=4,xxl=4),
                dbc.Col([dcc.Markdown(children='', id="md_text_p2")], style={"margin":"auto", "text-align":'justify'}, xs=9,sm=9, md=9, lg=4, xl=4,xxl=4),
                dbc.Col([dcc.Markdown(children='', id="md_text_p3")], style={"margin":"auto", "text-align":'justify'}, xs=9,sm=9, md=9, lg=4, xl=4,xxl=4)
            ], style={"margin-top":"70px", "margin-left":"30px"})
            ],style={"background-color":"grey"}), 
    dbc.Row([html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset", "margin-top":"50px", "margin-bottom":"25px"})]),
    dbc.Row([
        dbc.Col([], width=3),
        dbc.Col([dcc.Markdown(children='', id='md_bottom', style={'text-align':'center'})]),
        dbc.Col([], width=3)
    ], style={"margin-top":"25px"})
])

@callback(
    Output(component_id='about_header', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_header(ri_val):
    if ri_val=='Deutsch':
        return'### Über Mich'
    else:
        return '### About Me'
    
@callback(
    Output(component_id='md_text_abme1', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_md_text_1(ri_val):
    if ri_val=='English':
        return"### I'm Albert Koesnaidi."
    else:
        return '### Ich bin Albert Koesnaidi.'

@callback(
    Output(component_id='md_text_abme1_1', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_md_text_2(ri_val):
    if ri_val=='English':
        return"I'm a self-taught data analyst / data scientist."
    else:
        return 'Ich bin ein selbstständig erlernter Datenanalyst / Datenwissenschaftler'
    
@callback(
    Output(component_id='md_text_abme1_2', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_md_text_3(ri_val):
    if ri_val=='English':
        return"I'm passionate about data."
    else:
        return 'Ich bin begeistert für Daten'

@callback(
    Output(component_id='md_text_abme1_3', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_md_text_3(ri_val):
    if ri_val=='English':
        return"I'm learning Pyhton and Arduino"
    else:
        return 'Ich lerne Python und Arduino'
    
@callback(
    Output(component_id='md_text_p1', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_md_text_p1(ri_val):
    if ri_val=='English':
        return"It was back in the pandemic era of Covid-19, where I had a lot of spare time and discovered about Microprocessor-Arduino. I was really hooked up building a sensor like temperature or humidity as well as photoresistor and coding it into Arduino with java."
    else:
        return "Es war in der Pandemie-Ära von Covid-19, als ich viel Freizeit hatte und von Mikroprozessoren-Arduino erfuhr. Ich war wirklich begeistert davon, einen Sensor wie Temperatur oder Luftfeuchtigkeit sowie einen Fotowiderstand zu bauen und ihn mit Java in Arduino zu programmieren."

@callback(
    Output(component_id='md_text_p2', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_md_text_p2(ri_val):
    if ri_val=='English':
        return "In order to analyze and visualize the data I need to learn Python. Learning Python was relative easy for me because I have had Python in my college education. At this time around I got to know about Machine Learning and Data Science. "
    else:
        return "Um die Daten zu analysieren und zu visualisieren, musste ich Python lernen. Das Erlernen von Python fiel mir relativ leicht, da ich während meines Studiums bereits Erfahrungen mit Python gesammelt hatte. In dieser Zeit erfuhr ich auch erstmals von Machine Learning."

@callback(
    Output(component_id='md_text_p3', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_md_text_p3(ri_val):
    if ri_val=='English':
        return'With the eagerness to learn, I was teaching myself about those topics. With Machine Learning I want to tackle our biggest problem, and that is Global Warming. So with this website I want to show you our actual state regarding the global warming.'
    else:
        return "Mit dem Eifer zu lernen, habe ich mir selbst Wissen zu diesen Themen angeeignet. Mit Machine Learning möchte ich unser größtes Problem angehen, und das ist die globale Erwärmung. Mit dieser Website möchte ich Ihnen unseren aktuellen Zustand bezüglich der globalen Erwärmung zeigen"

@callback(
    Output(component_id='md_bottom', component_property='children'),
    Input(component_id='ri_about', component_property='value'))

def update_markdown(ri_val):
    if ri_val=='Deutsch':
        return'## Eine wachstumsorientierte Denkweise ist eine der beste Eigenschaften, die ein Mensch haben kann'
    else:
        return '## A Growth Mindeset Is One of The Best Thing A Human Can Have'
    
   




