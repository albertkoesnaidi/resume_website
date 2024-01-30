import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(__name__,order=3, path='/co2')

df = pd.read_csv('assets/owid-co2-data.csv')
cc = pd.read_csv('assets/Countries Continents.csv')

def country_code(continent):
    x = cc[cc['Countries Continents']==continent]['Entity'].to_list()
    return sorted(list(set(x).intersection(set(df['country'].unique()))))

countries = []

def layout():
    return html.Div([
            dbc.Row([
                dbc.Col([dcc.Markdown(children='', id='co2_header')],xs=6,sm=6, md=6, lg=5, xl=5,xxl=5),
                dbc.Col([dcc.Markdown([" "])]),
                dbc.Col([dcc.RadioItems(['English', 'Deutsch'], 'English', inline=True, inputStyle={"margin-left":"15px", "margin-right":"5px"} ,style={"margin-top":"5px"}, id='ri')], xs=5,sm=5, md=5, lg=3, xl=3,xxl=3)
            ]),
            html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ], style={'margin-top':"40px"}), html.Div([
            dbc.Row([
                dbc.Col([dbc.Col([dcc.Dropdown(id='dropd_conti', options=['Asia', 'Europe', 'Oceania', 'South America', 'North America'], multi=False)])], width=4),
                dbc.Col([dcc.Markdown([' '])], width=8)
            ])
            ,dbc.Row([
                dbc.Col([dcc.Graph(id='top5')], xs=12,sm=12, md=12, lg=8, xl=8,xxl=8),
                dbc.Col([dcc.Graph(id = 'pie_co2_click')], xs=12,sm=12, md=12, lg=4, xl=4,xxl=4)
            ])
        ]), html.Div([
            dbc.Row([
                dbc.Col([dcc.Dropdown(id='dropd3', options=['Asia', 'Europe', 'Oceania', 'South America', 'North America'], value="Asia", multi=False)],width=4),
                dbc.Col([dcc.Dropdown(id='dropd4', options=country_code('Asia'),multi=False)], width=4),
                dbc.Col([], width=4)
            ]),
            dbc.Row([
                dbc.Col([dcc.Markdown(children=[''], id='md_co2_1')])
            ])
        ]), html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id='line_co2')],xs=12,sm=12, md=12, lg=6, xl=6,xxl=6),
                dbc.Col([dcc.Graph(id='stackedbar')], xs=12,sm=12, md=12, lg=6, xl=6,xxl=6)
            ])
        ]), html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id = 'box_gas')], width=12),
                dbc.Col([dcc.Graph(id = 'box_capita')], width=12),
                dbc.Col([dcc.Graph(id = 'box_temp_gas')], width=12)
            ])
        ]), html.Div([
            dbc.Row([dcc.Markdown(children='', id='source_co2', style={'font-size':'10px'})])
        ])

@callback(
    Output(component_id='co2_header', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_header_co2(ri_val):
    if ri_val == 'English':
        return '### __CO2 Emission Dashboard__'
    else:
        return '### __CO2 Emissionen-Dashboard__'

@callback(
    Output(component_id='dropd4', component_property='options'),
        Input(component_id='dropd3', component_property='value'),
)
def update_dd(val):
    return country_code(val)

@callback(
    Output(component_id='top5', component_property='figure'),
    Input(component_id='dropd_conti', component_property='value'),
    Input(component_id='ri', component_property='value')
)  
def update_top_bar(val, ri_val):
    df_copy = df
    cc_copy = cc
    if val == None:
        cc_list = list(cc_copy['Entity'].unique())
        df_copy = df_copy[df_copy['country'].isin(cc_list)]
    else:
        df_copy = df_copy[df_copy['country'].isin(country_code(val))]
    df_gb = df_copy.groupby('country')['co2'].sum().sort_values(ascending=False).head(15)
    fig = px.bar(data_frame=df_gb, x=df_gb.values, y=df_gb.index, orientation='h')
    fig.update_layout(yaxis=dict(autorange='reversed'))
    if val == None:
        if ri_val == 'English':
            fig.update_layout(title = f'<b>Top CO2-Emmiter Countries in the World</b>', xaxis_title='CO2-Eimssion in Ton CO2', yaxis_title='Country')

        else:
            fig.update_layout(title = f'<b>Die Länder mit den höchsten CO2-Emissionen weltweit</b>', xaxis_title='CO2-Eimssionen in Tonnen CO2', yaxis_title='Staat')
    else:
        if ri_val == 'English':
            fig.update_layout(title = f'<b>Top CO2-Emitter Countries in {val}</b>', xaxis_title='CO2-Eimssion in Ton CO2', yaxis_title='Country')
        else:
            fig.update_layout(title = f'<b>Die Länder mit den höcsten CO2-Emissionen in {val}</b>', xaxis_title='CO2-Eimssionen in Tonnen CO2', yaxis_title='Staat')
    fig.update_layout(title_x=0.5)
    return fig


@callback(
    Output(component_id='pie_co2_click', component_property='figure'),
        Input(component_id='dropd_conti', component_property='value'),
        Input(component_id='ri', component_property='value')
)    
def update_pie_co2(val, ri_val):
    df_copy = df
    df1 = df_copy[['country', 'coal_co2', 'gas_co2', 'oil_co2', 'flaring_co2', 'other_industry_co2']]
    df1 = df1.set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    if val == None:
        df1 = df1[df1['country']=='World']
        fig = px.pie(data_frame=df1, values='value', names='type', title='Pie Chart Composition')
        fig.update_layout(title_x=0.5)
        if ri_val == 'English':
            fig.update_layout(title='<b>Global CO2 Composition</b>')
        else:
            fig.update_layout(title='<b>Globale CO2-Verteilung</b>')
    else:
        df1 = df1[df1['country']==val]
        fig = px.pie(data_frame=df1, values='value', names='type', title='Pie Chart Composition')
        fig.update_layout(title_x=0.5)
        if ri_val == 'English':
            fig.update_layout(title=f'<b>CO2 Composition in {val}</b>')
        else:
            fig.update_layout(title=f'<b>CO2-Verteilung in {val}</b>')
    return fig

@callback(
    Output(component_id='md_co2_1', component_property='children'),
        Input(component_id='ri', component_property='value'),
)  
def update_md_co2_1(ri_val):
    if ri_val == 'English':
        return 'The dropdown-menu is used for the following five graphs. You can pick multiple countries to do a comparison. Please refresh the page to clear all the selected countries'
    else:
        return 'Das Dropdown-Menü wird für die folgenden fünf Diagramme verwendet. Sie können mehrere Länder auswählen, um einen Vergleich durchzuführen. Bitte aktualisieren Sie die Seite, um alle ausgewählten Länder zu löschen'

@callback(
    Output(component_id='line_co2', component_property='figure'),
        Input(component_id='dropd4', component_property='value'),
        Input(component_id='ri', component_property='value')
)  
def update_line_co2(val, ri_val):
    country_list1 = countries
    df_copy = df.copy()
    df_copy = df_copy[['country', 'year', 'co2']]
    if val == None:
        country_list1.clear()
        country_list1 = ['Indonesia']
    else:
        country_list1.append(val)
    df_copy = df_copy[df_copy['country'].isin(country_list1)]
    fig = px.line(data_frame=df_copy, x='year', y='co2', color='country')
    if ri_val == 'English':
        fig.update_layout(title='<b>Annual Graph of CO2-Emission selected country</b>', xaxis_title='Year', yaxis_title='CO2-Eission in Ton CO2')
    else:
        fig.update_layout(title='<b>Jährliches Diagramm der CO2-Emissionen für die ausgewählte Länder</b>', xaxis_title='Jahr', yaxis_title='CO2-Emissionen in Tonnen CO2')
    fig.update_layout(title_x = 0.5)
    return fig


@callback(
    Output(component_id='stackedbar', component_property='figure'),
        Input(component_id='dropd4', component_property='value'),
        Input(component_id='ri', component_property='value')
)  
def update_stackedbar(val, ri_val):
    country_list2 = countries
    df_copy = df[['country', 'coal_co2', 'gas_co2', 'oil_co2', 'flaring_co2', 'other_industry_co2']]
    df_copy = df_copy.groupby('country').sum().reset_index()
    df_copy = df_copy.set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    if val == None:
        country_list2.clear()
        country_list2 = ['Indonesia']
    else:
        country_list2.append(val)
    df_copy = df_copy[df_copy['country'].isin(country_list2)]
    fig= px.bar(data_frame=df_copy, x='country', y='value', color='type')
    if ri_val == 'English':
        fig.update_layout(title='<b>Composition of the Total CO2-Emission Selected Countries</b>', xaxis_title='Country', yaxis_title='CO2-Comission in Million Tonnes CO2')
    else:
        fig.update_layout(title='<b>Verteilung der Total CO2-Emissionen gewählte Staaten</b>', xaxis_title='Staaten', yaxis_title='CO2-Comissionen in Millionen Tonnen CO2')
    fig.update_layout(title_x=0.5)
    return fig

@callback(
    Output(component_id='box_gas', component_property='figure'),
        Input(component_id='dropd4', component_property='value'),
        Input(component_id='ri', component_property='value')
)  
def update_gas_box(val, ri_val):
    country_list = countries
    df_copy = df[['country', 'nitrous_oxide', 'methane', 'co2']]
    if val == None:
        country_list.clear()
        country_list = ['Indonesia', 'Singapore']
    else:
        country_list.append(val)
    df_copy = df_copy[df_copy['country'].isin(country_list)]
    df_copy = df_copy.set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    fig = px.box(data_frame=df_copy, x='country', y='value', color='type')
    if ri_val == 'English':
        fig.update_layout(title='<b>Composition Dangeraous Gases</b>', xaxis_title='Countries', yaxis_title='Million Tonnes of Carbon Dioxide Equivalents')
    else:
        fig.update_layout(title='<b>Zusammensetzung gefährlicher Gase</b>', xaxis_title='Länder', yaxis_title='Millionen Tonnen der Kohlendioxid Gleichwertig')
    fig.update_layout(title_x=0.5)
    fig.update_layout(legend=dict(yanchor="bottom", y=-0.3, xanchor="left", x=0.01, orientation='h'))
    return fig

@callback(
    Output(component_id='box_capita', component_property='figure'),
        Input(component_id='dropd4', component_property='value'),
        Input(component_id='ri', component_property='value')
)  
def update_capita_box(val, ri_val):
    country_list = countries
    df_copy = df[['country', 'co2_per_capita', 'co2_per_gdp', 'co2_per_unit_energy']]
    if val == None:
        country_list.clear()
        country_list = ['Indonesia', 'Singapore']
    else:
        country_list.append(val)
    df_copy = df_copy[df_copy['country'].isin(country_list)]
    df_copy = df_copy.set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    fig = px.box(data_frame=df_copy, x='country', y='value', color='type')
    if ri_val == 'English':
        fig.update_layout(title='<b>Specific Comparison CO2-Emission</b>', xaxis_title='Countries', yaxis_title='Million Tonnes of Carbon Dioxide Equivalents')
    else:
        fig.update_layout(title='<b>Spezifischer Vergleich CO2-Emissionen</b>', xaxis_title='Länder', yaxis_title='Millionen Tonnen der Kohlendioxid Gleichwertig')
    fig.update_layout(title_x=0.5)
    fig.update_layout(legend=dict(yanchor="bottom", y=-0.3, xanchor="left", x=0.01, orientation='h'))
    return fig

@callback(
    Output(component_id='box_temp_gas', component_property='figure'),
        Input(component_id='dropd4', component_property='value'),
        Input(component_id='ri', component_property='value')
)  
def update_temp_gas_box(val,ri_val):
    country_list = countries
    df_copy = df[['country', 'temperature_change_from_ch4', 'temperature_change_from_co2', 'temperature_change_from_n2o', 'temperature_change_from_ghg']]
    if val == None:
        country_list.clear()
        country_list = ['Indonesia', 'Singapore']
    else:
        country_list.append(val)
    df_copy = df_copy[df_copy['country'].isin(country_list)]
    df_copy = df_copy.set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    fig = px.box(data_frame=df_copy, x='country', y='value', color='type')
    if ri_val == 'English':
        fig.update_layout(title='<b>Temperature Increase from Different Dangerous Gases</b>', xaxis_title='Countries', yaxis_title='Million Tonnes of Carbon Dioxide Equivalents')
    else:
        fig.update_layout(title='<b>Temperaturanstieg durch verschiedene gefährliche Gase</b>', xaxis_title='Länder', yaxis_title='Millionen Tonnen der Kohlendioxid Gleichwertig')
    fig.update_layout(title_x=0.5)
    fig.update_layout(legend=dict(yanchor="bottom", y=-0.5, xanchor="left", x=0.01, orientation='h'))
    return fig

@callback(
    Output(component_id='source_co2', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_source(ri_val):
    if ri_val == 'English':
        return 'Source: https://github.com/owid/co2-data'
    else:
        return 'Quelle: https://github.com/owid/co2-data'