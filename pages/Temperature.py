import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots

df = pd.read_csv('assets/gistemp_choropleth.csv')
df2 = pd.read_csv('assets/radar_chart_temp.csv')
countries_g3= []

cc = pd.read_csv('assets/Countries Continents.csv')

def country_code(continent):
    x = cc[cc['Countries Continents']==continent]['Entity'].to_list()
    return sorted(list(set(x).intersection(set(df['Entity'].unique()))))

dash.register_page(__name__,path='/Temperature')

def layout():
    return html.Div([
            dbc.Row([
                dbc.Col([dcc.Markdown(children='', id='temp_header')],xs=6,sm=6, md=6, lg=5, xl=5,xxl=5),
                dbc.Col([dcc.Markdown(children='')]),
                dbc.Col([dcc.RadioItems(['English', 'Deutsch'], 'English', inline=True, inputStyle={"margin-left":"15px", "margin-right":"5px"} ,style={"margin-top":"5px"}, id='ri')], xs=5,sm=5, md=5, lg=3, xl=3,xxl=3),

            ]),
            html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ], style={'margin-top':"40px"}),html.Div([
            dbc.Row([
            dbc.Col([dcc.Graph(id='fig1_temp')])
    ])]), html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Markdown(children = [''], id='md_text_2')
                ,dcc.Graph(id='fig2_temp')
            ], xs=12,sm=12, md=12, lg=8, xl=8,xxl=8),
            dbc.Col([
                dcc.Graph(id = 'fig3_temp', style={'marginTop':20, 'marginBottom':1})
            ], xs=12,sm=12, md=12, lg=4, xl=4,xxl=4)
        ])
    ]), html.Div([
        dbc.Row([
            dbc.Col([
            dcc.Dropdown(
                options=['Asia', 'Europe', 'South America', 'North America', 'Africa', 'Oceania', 'World'], multi=False, id='dd_temp_continents'
            )
        ], width=3),
            dbc.Col([
                dcc.Dropdown(options=list(range(df['Year'].min(), df['Year'].max()+1, 1)), value=2017, multi=False, id='dd_year')
            ], width=3),
            dbc.Col([dcc.Markdown(children='')], width=6)
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(id = 'top10_1')]),
        ])
    ]), html.Div([
            dbc.Row([dcc.Markdown(children='', id='source_temperatur', style={'font-size':'10px'})])
        ])

@callback(
    Output(component_id='temp_header', component_property='children'),
    Input(component_id='ri', component_property='value')
)
def update_temp_header(ri_val):
    if ri_val == 'English':
        return '### __Global Temperature Dashboard__'
    else:
        return '### __Globales Temperatur-Dashboard__'

@callback(
    Output(component_id='fig1_temp', component_property='figure'),
    Input(component_id='ri', component_property='value')
)
def update_fig1_temp(ri_val):
    df1 = df.copy()
    fig = px.choropleth(data_frame=df1, locations='alpha-3', color='Surface temperature anomaly', hover_data=['Entity', 'alpha-3'] ,animation_frame='Year', range_color=(min(df['Surface temperature anomaly']), max(df['Surface temperature anomaly'])))
    if ri_val =='English':
        fig.update_layout(
            title = '<b>Animated Global Map Temperature Change in °C</b>',
            title_x = 0.5,
        )
    elif ri_val == 'Deutsch':
        fig.update_layout(
            title = '<b>Animierte weltweite Karte der Temperaturveränderungen in °C</b>',
            title_x = 0.5,
        )
    return fig

@callback(
    Output(component_id='md_text_2', component_property='children'),
    Input(component_id='ri', component_property='value')
)
def update_md_text_2(ri_val):
    if ri_val == 'English':
        return 'You can click multiple countries on the top choropleth graph to do a comparison displayed by the bottom graph. Please refresh the page to clear to make a new comparison.'
    else:
        return 'Sie können mehrere Länder auf dem oberen choroplethen Diagramm anklicken, um einen Vergleich im unteren Diagramm anzuzeigen. Aktualisieren Sie die Seite, um die Auswahl zu löschen und einen neuen Vergleich vorzunehmen.'

@callback(
    Output(component_id='fig2_temp', component_property='figure'),
    Input(component_id='fig1_temp', component_property='clickData'),
    Input(component_id='ri', component_property='value')
)
def update_fig2_temp(val, ri_val):
    g3 = countries_g3
    if val == None:
        g3.clear()
        g3 = ['Indonesia']
    else:
        g3.append(val['points'][0]['customdata'][0])
    df3 = df[df['Entity'].isin(g3)]
    fig_g3 = px.line(data_frame=df3, x='Year', y='Surface temperature anomaly', color='Entity')
    if ri_val == 'English':
        fig_g3.update_layout(
            title = '<b>Comparison in Annual Temperature Change Chosen Countries</b>',
            title_x = 0.5,
            xaxis_title = 'Year',
            yaxis_title = 'Temperature Change in °C'
        )
    else:
        fig_g3.update_layout(
            title = '<b>Vergleich der jährlichen Temperaturveränderung im ausgewählten Land</b>',
            title_x = 0.5,
            xaxis_title = 'Jahr',
            yaxis_title = 'Temperaturveränderung in °C'
        )
    return fig_g3

@callback(
    Output(component_id='fig3_temp', component_property='figure'),
    Input(component_id='fig1_temp', component_property='clickData'),
    Input(component_id='ri', component_property='value')
)
def update_fig3_temp(val, ri_val):
    df3 = df2[df2['year'].isin([1961,2019])]
    if val==None:
        df3 = df3[df3['Area']=='Indonesia']
        fig_g3 = px.line_polar(data_frame=df3, theta='Months', r='dt', color='year', line_close=True)
        if ri_val == 'English':
            fig_g3.update_layout(title=f'<b>Comparison Global temperature change <br> between year 1961 and 2017</b>', title_x=0.5)
        else:
            fig_g3.update_layout(title='<b>Temperaturvergleich der Welt <br> zwischen Jahr 1961 und 2017</b>', title_x=0.5)
    else:
        df3 = df3[df3['Area']==val['points'][0]['customdata'][0]]
        fig_g3 = px.line_polar(data_frame=df3, theta='Months', r='dt', color='year', line_close=True)
        if ri_val == 'English':
            fig_g3.update_layout(title=f'<b>Comparison temperature change <br> in {val["points"][0]["customdata"][0]} between year 1961 and 2017</b>', title_x=0.5)
        else:
            fig_g3.update_layout(title=f'<b>Temperaturvergleich in {val["points"][0]["customdata"][0]} <br> im Jahr zwischen Jahr 1961 und 2017</b>', title_x=0.5)
    return fig_g3

@callback(
    Output(component_id='top10_1', component_property='figure'),
    Input(component_id='dd_year', component_property='value'),
    Input(component_id='dd_temp_continents', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_top10graph(year, val, ri_val):
    df4 = df.copy()
    df4 = df4[df4['Year']==year][['Entity', 'Surface temperature anomaly']]
    if val == None: 
        pass
    elif val=='Asia': 
        df4 = df4[df4['Entity'].isin(country_code('Asia'))]
    elif val=='Europe': 
        df4 = df4[df4['Entity'].isin(country_code('Europe'))]
    elif val=='South America': df4 = df4[df4['Entity'].isin(country_code('South America'))]    
    elif val=='North America': df4 = df4[df4['Entity'].isin(country_code('North America'))]
    elif val=='Africa': df4 = df4[df4['Entity'].isin(country_code('Africa'))]
    elif val=='Oceania': df4 = df4[df4['Entity'].isin(country_code('Oceania'))]
    elif val=='World': df4 = df4
    df4 = df4.sort_values(by='Surface temperature anomaly', ascending=False).head(15)
    fig = px.bar(data_frame=df4, x='Surface temperature anomaly', y='Entity', orientation='h')
    fig.update_layout(yaxis=dict(autorange='reversed'))
    if val == None:
        if ri_val == 'English':
            fig.update_layout(title=f'<b>Top hottest countries in the World in {year}</b>', xaxis_title='Temperature in °C', yaxis_title='Country')
        else:
            fig.update_layout(title=f'<b>Die heißesten Länder der Welt im Jahr {year}</b>', xaxis_title='Temperatur in °C', yaxis_title='Staat')
    else:
        if ri_val == 'English':
            fig.update_layout(title=f'<b>Top hottest countries in {val} in {year}</b>', xaxis_title='Temperature in °C', yaxis_title='Country')
        else: 
            fig.update_layout(title=f'<b>Die heißesten Länder in {val} im Jahr {year}</b>', xaxis_title='Temperatur in °C', yaxis_title='Staat')
    fig.update_layout(title_x=0.5)
    return fig

@callback(
    Output(component_id='source_temperatur', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_source(ri_val):
    if ri_val == 'English':
        return 'Source: https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data'
    else:
        return 'Quelle: https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data'