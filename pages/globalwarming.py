import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

df = pd.read_csv('assets/owid-co2-data.csv')
sea = pd.read_csv('assets/sea_level.csv')
gt_co2 = pd.read_csv('assets/temp_co2.csv')
co2_ppm = pd.read_csv('assets/co2ppm.csv')
ice = pd.read_csv('assets/glaciers_csv.csv')


dash.register_page(__name__,path='/Globalwarming')

def layout():
    return html.Div([
        dbc.Row([
                dbc.Col([dcc.Markdown(children='', id='overview_headline')],xs=6,sm=6, md=6, lg=5, xl=5,xxl=5),
                dbc.Col([dcc.Markdown(children='')]),
                dbc.Col([dcc.RadioItems(['English', 'Deutsch'], 'English', inline=True, inputStyle={"margin-left":"15px", "margin-right":"5px"} ,style={"margin-top":"5px"}, id='ri')], xs=5,sm=5, md=5, lg=3, xl=3,xxl=3),

            ]),
            html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ], style={'margin-top':"40px"}), html.Div([
                dbc.Row([
                dbc.Col([], xs=1,sm=1, md=1, lg=2, xl=2,xxl=2),
                dbc.Col([dcc.Markdown(children=['#### "CO2 is the exhaling breath of our civilization, literally... Changing that pattern requires a scope, a scale, a speed of change that is beyond what we have done in the past." - Al Gore '])], style={'margin-top':'50px', 'margin-bottom':'50px'}),
                dbc.Col([], xs=1,sm=1, md=1, lg=2, xl=2,xxl=2)
        ]), html.Div([
                dbc.Row([dcc.Graph(id='fig0_overview')])
        ])
        ]), html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row([dcc.Graph(id='fig1_overview')]),
                    dbc.Row([dcc.Markdown(children='', id='md_text_fig1')])
                ], style = {'text-align':'justify'} ,xs=12,sm=12, md=12, lg=6, xl=6,xxl=6),
                dbc.Col([
                    dbc.Row([dcc.Graph(id='fig2_overview')]),
                    dbc.Row([dcc.Markdown(children='', id='md_text_fig2')])
                ], style = {'text-align':'justify'} ,xs=12,sm=12, md=12, lg=6, xl=6,xxl=6)
            ]), dbc.Row([
                    dbc.Col([], xs=1,sm=1, md=1, lg=2, xl=2,xxl=2),
                    dbc.Col([dcc.Markdown(children=['### "I have always been fascinated with those who try to look over the horizon and see things that are coming at us" - Al Gore'])], style={'margin-top':'50px', 'margin-bottom':'50px'}),
                    dbc.Col([], xs=1,sm=1, md=1, lg=2, xl=2,xxl=2)
            ]), dbc.Row([
                dbc.Col([
                    dbc.Row([dcc.Graph(id='fig3_overview')]),
                    dbc.Row([dcc.Markdown(children='', id='md_text_fig3')])
                ], style = {'text-align':'justify'} ,xs=12,sm=12, md=12, lg=6, xl=6,xxl=6),
                dbc.Col([
                    dbc.Row([dcc.Graph(id='fig4_overview')]),
                    dbc.Row([dcc.Markdown(children='', id='md_text_fig4')])
                ], style = {'text-align':'justify'} ,xs=12,sm=12, md=12, lg=6, xl=6,xxl=6)
            ]), html.Div([
                dbc.Row([
                    dbc.Col([], xs=1,sm=1, md=1, lg=2, xl=2,xxl=2),
                    dbc.Col([dcc.Markdown(children=['### "Solving the climate crisis is within our grasp, but we need people like you to stand up and act." - Al Gore'])], style={'margin-top':'50px', 'margin-bottom':'50px'}),
                    dbc.Col([], xs=1,sm=1, md=1, lg=2, xl=2,xxl=2)
                ])
            ])

        ]), html.Div([
            dbc.Row([dcc.Markdown(children='', id='source_globalwarming', style={'font-size':'10px'})])
        ])

@callback(
    Output(component_id='overview_headline', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_headline_compariosn(ri_val):
    if ri_val == 'English':
        return '### __Global Warming__'
    else:
        return '### __Globale Erwärmung__'
    
@callback(
    Output(component_id='fig1_overview', component_property='figure'),
    Input(component_id='ri', component_property='value'),
)
def update_fig1_overview(ri_val):
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(x = gt_co2['year'],y = gt_co2['co2'], mode='lines', name='CO2-Emission'), secondary_y=False,)
    fig1.add_trace(go.Scatter(x = gt_co2['year'],y = gt_co2['Mean'], mode='lines', name='Global Temperature in °C'), secondary_y=True)
    if ri_val == 'English':
        fig1.update_layout(title='<b>Global Temperature vs Increasing CO2</b>', title_x=0.5)
        fig1.update_xaxes(title_text='Year')
        fig1.update_yaxes(title_text= 'Million Tons of Carbon' , secondary_y=True)
        fig1.update_yaxes(title_text= 'Temperature in °C' , secondary_y=False)
    else:
        fig1.update_layout(title='<b>Weltweite Temperatur vs. steigendes CO2</b>', title_x=0.5)
        fig1.update_xaxes(title_text='Jahr')
        fig1.update_yaxes(title_text= 'Millionen Tonnen Kohlenstoff' , secondary_y=True)
        fig1.update_yaxes(title_text= 'Temperatur in °C' , secondary_y=False)
    fig1.update_layout(legend=dict(yanchor="bottom", y=-0.3, xanchor="left", x=0.01, orientation='h'))
    return fig1

@callback(
    Output(component_id='md_text_fig1', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_md_fig1(ri_val):
    if ri_val == 'English':
        return "We can see from the graph above that rising the CO2 means increase the global temperature. These two closely linked phenomena contribute to climate change. Human activities, such as the burning of fossil fuels and deforestation, release large amounts of CO2 into the atmosphere, creating a greenhouse effect. This trapped heat leads to a gradual warming of the Earth's surface, resulting in rising global temperatures. The consequences of this warming include more frequent and severe heatwaves, altered precipitation patterns, sea level rise,  and disruptions to ecosystems. Mitigating these effects requires concerted efforts to reduce greenhouse gas emissions and transition to sustainable practices."
    else:
        return "Wir können aus dem obenstehenden Diagramm sehen, dass das Ansteigen des CO2-Gehalts zu einer Erhöhung der globalen Temperatur führt. Diese eng miteinander verbundenen Phänomene tragen zum Klimawandel bei. Menschliche Aktivitäten wie die Verbrennung fossiler Brennstoffe und die Abholzung setzen große Mengen CO2 in die Atmosphäre frei, was einen Treibhauseffekt erzeugt. Die dadurch gefangene Wärme führt zu einer allmählichen Erwärmung der Erdoberfläche und resultiert in steigenden globalen Temperaturen. Die Folgen dieser Erwärmung umfassen häufigere und schwerere Hitzewellen, veränderte Niederschlagsmuster, Anstieg des Meeresspiegels und Störungen von Ökosystemen. Die Milderung dieser Effekte erfordert gemeinsame Anstrengungen zur Reduzierung von Treibhausgasemissionen und zur Umstellung auf nachhaltige Praktiken"
    
@callback(
    Output(component_id='fig2_overview', component_property='figure'),
    Input(component_id='ri', component_property='value'),
)
def update_fig2_overview(ri_val):
    fig2 = px.line(data_frame=sea, x='Year', y='CSIRO Adjusted Sea Level')
    if ri_val == 'English':
        fig2.update_layout(title='<b>CSIRO Adjusted Sea Level</b>', title_x=0.5, xaxis_title='Year', yaxis_title='Sea Level in Inches')
    else:
        fig2.update_layout(title='<b>CSIRO Angepasster Meeresspiegel</b>', title_x=0.5, xaxis_title='Jahr', yaxis_title='Meeresspiegel in Zoll')
    return fig2

@callback(
    Output(component_id='md_text_fig2', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_md_fig2(ri_val):
    if ri_val == 'English':
        return "The rising sea levels is being displayed by the upper graph. The Rising sea levels are a consequence of global climate change, primarily driven by the melting of glaciers and ice caps, and the thermal expansion of seawater as it warms. As Earth's temperature increases due to human activities, such as the burning of fossil fuels, the ice on land and in polar regions melts, contributing to the increase in sea levels. This phenomenon poses a significant threat to coastal areas, leading to higher storm surges, increased coastal erosion, and the risk of flooding for low-lying regions."
    else:
        return "Der Anstieg des Meeresspiegels wird durch das obere Diagramm dargestellt. Der Anstieg des Meeresspiegels ist eine Folge des globalen Klimawandels, der hauptsächlich durch das Schmelzen von Gletschern und Eiskappen sowie die thermische Ausdehnung von Meerwasser aufgrund der Erwärmung verursacht wird. Mit zunehmender Erdtemperatur aufgrund menschlicher Aktivitäten wie der Verbrennung fossiler Brennstoffe schmilzt das Eis auf dem Festland und in den Polargebieten, was zu einem Anstieg des Meeresspiegels führt. Dieses Phänomen stellt eine erhebliche Bedrohung für Küstengebiete dar und führt zu höheren Sturmfluten, verstärkter Küstenerosion und dem Risiko von Überschwemmungen in tiefliegenden Regionen."
    

@callback(
    Output(component_id='fig3_overview', component_property='figure'),
    Input(component_id='ri', component_property='value'),
)
def update_fig3_overview(ri_val):
    fig3 = px.line(data_frame=co2_ppm, x='Date', y='Average')
    if ri_val == 'English':
        fig3.update_layout(title='<b>CO2 PPM Trends in Atmospheric Carbon Dioxide</b>', title_x=0.5, xaxis_title='Year', yaxis_title='CO2 [ppm]')
    else:
        fig3.update_layout(title='<b>Trends der CO2-PPM in atmosphärischem Kohlendioxid</b>', title_x=0.5, xaxis_title='Jahr', yaxis_title='CO2 [ppm]')
    return fig3

@callback(
    Output(component_id='md_text_fig3', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_md_fig3(ri_val):
    if ri_val == 'English':
        return "Seasonal variations in carbon dioxide (CO2) levels refer to the cyclical changes in atmospheric CO2 concentrations that occur throughout the year. This pattern is primarily influenced by natural factors, such as photosynthesis and respiration in plants. During the Northern Hemisphere's growing season (spring and summer), plants absorb CO2 through photosynthesis, causing a temporary decrease in atmospheric CO2 levels. In contrast, during the dormant season (fall and winter), plants release CO2 through respiration, leading to an increase in atmospheric CO2 concentrations. Despite these seasonal fluctuations, the long-term trend over recent decades has shown a consistent rise in global CO2 levels, primarily driven by human activities such as burning fossil fuels and deforestation. This ongoing increase contributes to climate change and its associated impacts on the environment"
    else:
        return "Jahreszeitenabhängige Schwankungen in den Kohlendioxid (CO2)-Levels beziehen sich auf die zyklischen Veränderungen in den atmosphärischen CO2-Konzentrationen, die im Laufe des Jahres auftreten. Dieses Muster wird hauptsächlich von natürlichen Faktoren beeinflusst, wie zum Beispiel der Photosynthese und der Atmung der Pflanzen. Während der Wachstumsperiode der nördlichen Hemisphäre (Frühling und Sommer) nehmen Pflanzen durch die Photosynthese CO2 auf, was zu einem vorübergehenden Rückgang der atmosphärischen CO2-Werte führt. Im Gegensatz dazu setzen Pflanzen während der Ruheperiode (Herbst und Winter) durch die Atmung CO2 frei, was zu einem Anstieg der atmosphärischen CO2-Konzentrationen führt. Trotz dieser saisonalen Schwankungen zeigt der langfristige Trend der letzten Jahrzehnte eine stetige Zunahme der globalen CO2-Werte, die hauptsächlich durch menschliche Aktivitäten wie das Verbrennen fossiler Brennstoffe und die Abholzung verursacht wird. Diese fortlaufende Zunahme trägt zum Klimawandel und den damit verbundenen Auswirkungen auf die Umwelt bei"
    
@callback(
    Output(component_id='fig4_overview', component_property='figure'),
    Input(component_id='ri', component_property='value'),
)
def update_fig4_overview(ri_val):
    fig4 = px.line(data_frame=ice, x='Year', y='Mean cumulative mass balance')
    if ri_val == 'English':
        fig4.update_layout(title='<b>Average cumulative mass balance of reference Glaciers worldwide</b>', title_x=0.5, xaxis_title='Year', yaxis_title='Mean Cumulative Mass Balance')
    else:
        fig4.update_layout(title='<b>Durchschnittliche kumulierte Massenbilanz Weltweit</b>', title_x=0.5, xaxis_title='Jahr', yaxis_title='Durchschnittliche kumulierte Massenbilanz')
    return fig4

@callback(
    Output(component_id='md_text_fig4', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_md_fig4(ri_val):
    if ri_val == 'English':
        return "The decreasing ice mass in Antarctica refers to the ongoing reduction in the total amount of ice across the continent. This phenomenon is primarily driven by factors such as rising temperatures and changes in climate patterns. As temperatures increase, Antarctica experiences higher rates of ice melt, contributing to the decline in ice mass. Additionally, warmer temperatures can lead to the fracturing and calving of ice shelves, further accelerating the loss. The diminishing ice mass in Antarctica has significant implications for global sea level rise, as melted ice contributes to the increasing volume of water in the world's oceans. This trend is a key indicator of climate change and underscores the need for continued monitoring and understanding of the Antarctic ice dynamics"
    else:
        return "Die abnehmende Eismasse in der Antarktis bezieht sich auf die fortlaufende Reduzierung der Gesamtmenge an Eis auf dem Kontinent. Dieses Phänomen wird hauptsächlich durch Faktoren wie steigende Temperaturen und Veränderungen in den Klimamustern angetrieben. Mit zunehmenden Temperaturen erfährt die Antarktis eine höhere Rate an Eisschmelze, was zum Rückgang der Eismasse beiträgt. Zusätzlich können wärmere Temperaturen zu Rissen und Abbrüchen von Eisschelfen führen, was den Verlust weiter beschleunigt. Die abnehmende Eismasse in der Antarktis hat bedeutende Auswirkungen auf den globalen Anstieg des Meeresspiegels, da geschmolzenes Eis zum zunehmenden Volumen von Wasser in den Weltmeeren beiträgt. Dieser Trend ist ein wichtiger Indikator für den Klimawandel und unterstreicht die Notwendigkeit einer fortlaufenden Überwachung und des Verständnisses der Antarktis-Eisdynamik"

#################################
@callback(
    Output(component_id='fig0_overview', component_property='figure'),
    Input(component_id='ri', component_property='value'),
)
def show_fig0(ri_val):
    df1 = df.copy()
    df1 = df1[df1['country']=='World']
    fig = px.area(data_frame=df1, x='year', y='co2')
    fig.update_layout(yaxis_range=[0,40000])
    if ri_val =='English':
        fig.update_layout(title='<b>Historical Timeline of the Rising Carbon-Dioxide</b>', title_x=0.5)
        fig.add_shape(type="rect", x0=1760, y0=0, x1=1840, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1760,1840,1840,1760,1760], 
                y=[0,0,40000,40000,0], fill="toself", mode='lines', name='', opacity=0,
                text='<b>The Industrial Revolution happened from 1760 until 1840</b>'))
        
        fig.add_shape(type="rect", x0=1938, y0=0, x1=1939, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1938,1939,1939,1938,1938], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Year 1938: Guy Callendar discovered a proof that global temperature are rising </b>'))

        fig.add_shape(type="rect", x0=1958, y0=0, x1=1959, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1958,1959,1959,1958,1958], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Year 1958: CO2 levels are rising and fossil fuels are to blame </b>'))
        
        fig.add_shape(type="rect", x0=1985, y0=0, x1=1986, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1985,1986,1986,1985,1985], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Year 1985: Ozon Hole is discovered for the first time </b>'))

        fig.add_shape(type="rect", x0=1992, y0=0, x1=1993, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1992,1993,1993,1992,1992], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Year 1992: Global coral reefs are at threat </b>'))
        
        fig.add_shape(type="rect", x0=2007, y0=0, x1=2008, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[2007,2008,2008,2007,2007], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Year 2007: The Arctic is warming twice as fast as the rest of the planet </b>'))
        
        fig.add_shape(type="rect", x0=2018, y0=0, x1=2019, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[2018,2019,2019,2018,2018], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Year 2019: The Ice Collapses are "irreversible" </b>'))
    else:
        fig.update_layout(title='<b>Historischer Zeitstrahl des steigenden Kohlendioxids</b>', title_x=0.5)
        fig.add_shape(type="rect", x0=1760, y0=0, x1=1840, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1760,1840,1840,1760,1760], 
                y=[0,0,40000,40000,0], fill="toself", mode='lines', name='', opacity=0,
                text='<b>Die Industrielle Revolution ereignete sich von 1760 bis 1840</b>'))
        
        fig.add_shape(type="rect", x0=1938, y0=0, x1=1939, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1938,1939,1939,1938,1938], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Jahr 1938: Guy Callendar entdeckte einen Beweis dafür, dass die globale Durchschnittstemperatur steigt </b>'))

        fig.add_shape(type="rect", x0=1958, y0=0, x1=1959, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1958,1959,1959,1958,1958], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Jahr 1958: Die CO2-Werte steigen, und fossile Brennstoffe sind dafür verantwortlich </b>'))
        
        fig.add_shape(type="rect", x0=1985, y0=0, x1=1986, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1985,1986,1986,1985,1985], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Jahr 1985: Das Ozonloch wird zum ersten Mal entdeckt </b>'))

        fig.add_shape(type="rect", x0=1992, y0=0, x1=1993, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[1992,1993,1993,1992,1992], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Jahr 1992: Globale Korallenriffe sind bedroht </b>'))
        
        fig.add_shape(type="rect", x0=2007, y0=0, x1=2008, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[2007,2008,2008,2007,2007], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>Jahr 2007: Die Arktis erwärmt sich doppelt so schnell wie der Rest des Planeten </b>'))
        
        fig.add_shape(type="rect", x0=2018, y0=0, x1=2019, y1=40000, fillcolor='orange', line_color='orange', opacity=0.3)
        fig.add_trace(go.Scatter(x=[2018,2019,2019,2018,2018], y=[0,0,40000,40000,0], fill="toself",mode='lines',name='',opacity=0,
                text='<b>JAhr 2019: Die Eiskollapsen sind nicht "rückgängig" zu machen </b>'))
        
        
    return fig

@callback(
    Output(component_id='source_globalwarming', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_source(ri_val):
    if ri_val == 'English':
        return 'Source: "A Brief History of Climate Change Discoveries" - (https://www.discover.ukri.org/), https://datahub.io/core/co2-fossil-by-nation, https://datahub.io/core/global-temp, https://datahub.io/core/co2-ppm, https://datahub.io/core/sea-level-rise, https://datahub.io/core/glacier-mass-balance'
    else:
        return 'Quelle: "A Brief History of Climate Change Discoveries" - (https://www.discover.ukri.org/), https://datahub.io/core/co2-fossil-by-nation, https://datahub.io/core/global-temp, https://datahub.io/core/co2-ppm, https://datahub.io/core/sea-level-rise, https://datahub.io/core/glacier-mass-balance'