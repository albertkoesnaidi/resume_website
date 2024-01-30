import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv('assets/owid-energy-data.csv')
cc = pd.read_csv('assets/Countries Continents.csv')
countries = []

def country_code(continent):
    if continent == 'World':
        return list(set(df['country'].unique()).intersection(set(cc['Entity'])))
    else:
        x = cc[cc['Countries Continents']==continent]['Entity'].to_list()
        return sorted(list(set(x).intersection(set(df['country'].unique()))))

dash.register_page(__name__,path='/Energy')

def layout():
    return html.Div([
            dbc.Row([
                dbc.Col([dcc.Markdown(children=[''], id='header_energie')],xs=6,sm=6, md=6, lg=5, xl=5,xxl=5),
                dbc.Col([dcc.Markdown([" "])]),
                dbc.Col([dcc.RadioItems(['English', 'Deutsch'], 'English', inline=True, inputStyle={"margin-left":"15px", "margin-right":"5px"} ,style={"margin-top":"5px"}, id='ri')], xs=5,sm=5, md=5, lg=3, xl=3,xxl=3)
            ]),
            html.Hr(style={"borderWidth":"0.5vh", "width": "100%", "borderColor": "black" ,"opacity": "unset"})
        ],style={'margin-top':"40px"}),html.Div([
        dbc.Row([
            dcc.RadioItems(options=['Asia', 'Europe', 'Oceania', 'South America', 'North America', 'World'], value='Asia', inline=True, id='rdi_continents',inputStyle={"margin-left":"10px", "margin-right":"5px"})
        ]),
        dbc.Row([
            html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id = 'top_fossil')], xs=12,sm=12, md=12, lg=6, xl=6,xxl=6),
                dbc.Col([dcc.Graph(id = 'top_renewable')], xs=12,sm=12, md=12, lg=6, xl=6,xxl=6)
            ])
            ,dbc.Row([
                    dbc.Col([dcc.Dropdown(id='dropd1', options=['Asia', 'Europe', 'Oceania', 'South America', 'North America'], value="Asia", multi=False)], width=2),
                    dbc.Col([dcc.Dropdown(id='dropd2', options=country_code('Asia'),multi=False)], width=4),
                    dbc.Col([dcc.Markdown(' ')], width=6)
            ])
            ,dbc.Row([
                dcc.Markdown(children='', id='text_energie1', style={'margin-top':'20px'})
            ])
            , dbc.Row([
                dbc.Col([dcc.Graph(id = 'line_energie')], xs=12,sm=12, md=12, lg=7, xl=7,xxl=7),
                dbc.Col([dcc.Graph(id = 'bar_click_year_energie')], xs=12,sm=12, md=12, lg=5, xl=5,xxl=5)
            ])
            
            , dbc.Row([
                dbc.Col([dcc.Graph(id = 'bar_total_energie')], xs=12,sm=12, md=12, lg=4, xl=4,xxl=4),
                dbc.Col([dcc.Graph(id = 'pie_fossil')], xs=12,sm=12, md=12, lg=4, xl=4,xxl=4),
                dbc.Col([dcc.Graph(id = 'pie_renewable')], xs=12,sm=12, md=12, lg=4, xl=4,xxl=4)
            ]),
            dbc.Row([dcc.Markdown(children='', id='headline_energie_comparison')]),
            dbc.Row([
                    dbc.Col([dcc.Dropdown(id='dropd4', options=['Asia', 'Europe', 'Oceania', 'South America', 'North America'], value="Asia", multi=False)], width=2),
                    dbc.Col([dcc.Dropdown(id='dropd5', options=country_code('Asia'),multi=False)], width=4),
                    dbc.Col([dcc.Markdown(' ')], width=6)
            ]),
            dbc.Row([
                    dcc.Markdown(children='', id='comparison_energie_text', style={'margin-top':'10px'})
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id = 'fig_compare_fossil')], xs=12,sm=12, md=12, lg=6, xl=6,xxl=6),
                dbc.Col([dcc.Graph(id = 'fig_compare_renewable')], xs=12,sm=12, md=12, lg=6, xl=6,xxl=6)
            ])
        ])
        ])
    ]) , html.Div([
            dbc.Row([dcc.Markdown(children='', id='source_energie', style={'font-size':'10px'})])
        ])

@callback(
    Output(component_id='header_energie', component_property='children'),
        Input(component_id='ri', component_property='value'),
)
def update_header_energie(ri_val):
    if ri_val == 'English':
        return '### __Global Energy-Dashboard__'
    else:
        return '### __Globales Energie-Dashboard__'

@callback(
    Output(component_id='dropd2', component_property='options'),
        Input(component_id='dropd1', component_property='value'),
)
def update_dd(val):
    return country_code(val)

@callback(
    Output(component_id='top_fossil', component_property='figure'),
    Input(component_id='rdi_continents', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_top_fossil(val, ri_val):
    ts = df.copy()
    ts['fossil_electricity'] = ts['fossil_electricity'].replace(0,np.NaN)
    ts = ts.dropna(subset=['fossil_electricity'], axis=0)
    if val == 'World':
        df3 = ts[ts['country'].isin(country_code('World'))]
    else: 
        df3 = ts[ts['country'].isin(country_code(val))]
    df3_gb = df3.groupby('country')['fossil_electricity'].sum().sort_values(ascending=False).head(20)
    fig = px.bar(data_frame=df3_gb, y=df3_gb.index, x=df3_gb.values, orientation='h')
    fig.update_layout(yaxis=dict(autorange='reversed'), xaxis_title='TWh')
    if ri_val == 'English':
        fig.update_layout(
                title = '<b>Top Fossil Energy User</b>',
                title_x=0.5,
                yaxis_title='Countries'
            )
    else:
        fig.update_layout(
                title = '<b>Top Verbraucher von fossilen Energien</b>',
                title_x=0.5,
                yaxis_title='Länder',
            )
    return fig

@callback(
    Output(component_id='top_renewable', component_property='figure'),
    Input(component_id='rdi_continents', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_top_renewable(val, ri_val):
    ts = df.copy()
    ts['renewables_electricity'] = ts['renewables_electricity'].replace(0,np.NaN)
    ts = ts.dropna(subset=['renewables_electricity'], axis=0)
    if val == 'World':
        df3 = ts[ts['country'].isin(country_code('World'))]
    else: 
        df3 = ts[ts['country'].isin(country_code(val))]
    df3_gb = df3.groupby('country')['renewables_electricity'].sum().sort_values(ascending=False).head(20)
    fig = px.bar(data_frame=df3_gb, y=df3_gb.index, x=df3_gb.values, orientation='h')
    fig.update_layout(yaxis=dict(autorange='reversed'))
    if ri_val == 'English':
        fig.update_layout(
                title = '<b>Top Renewable Energy User</b>',
                title_x = 0.5,
                xaxis_title='Energy [TWh]',
                yaxis_title = 'Countries'
            )
    else:
        fig.update_layout(
                title = '<b>Top-Nutzer der erneuerbaren Energien</b>',
                title_x = 0.5,
                xaxis_title='Energie [TWh]',
                yaxis_title='Länder'
            )
    return fig

@callback(
    Output(component_id='text_energie1', component_property='children'),
    Input(component_id='ri', component_property='value'))
def update_text_energie1(ri_val):
    if ri_val == 'English':
        return 'Please use the top Dropdown-menu for the bottom graph and you can click the line graph to choose which year will be displayen on the rightside graph'
    else:
        return 'Bitte verwenden Sie das oberste Dropdown-Menü für das untere Diagramm, und Sie können auf das Liniendiagramm klicken, um auszuwählen, welches Jahr im Diagramm auf der rechten Seite angezeigt werden soll.'
    
@callback(
    Output(component_id='line_energie', component_property='figure'),
    Input(component_id='dropd2', component_property='value'),
    Input(component_id='ri',component_property='value')
)
def update_line_energie(value, ri_val):
    df2 = df.copy()
    df2 = df2.dropna(subset=['coal_electricity'])
    df2['fossil'] = df2['coal_electricity'] + df2['oil_electricity'] + df2['gas_electricity']
    df2['renewables'] = df2['renewables_electricity'] + df2['other_renewable_electricity']
    if value == None:
        df2 = df2[df2['country']=='Indonesia']
    else:
        df2 = df2[df2['country']==value]
    fig2= go.Figure()
    fig2.add_scatter(x=df2['year'], y=df2['fossil'], mode='lines', name='Fossil Fuels')
    fig2.add_scatter(x=df2['year'], y=df2['renewables'], mode='lines', name='Renewables Sources')
    fig2.add_scatter(x=df2['year'], y=df2['nuclear_electricity'], mode='lines', name='Nuclear Energy')
    fig2.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
    if (ri_val == 'English'):
        if value == None:
            fig2.update_layout(title="<b> Indonesia's Annual Energy Development Different Type </b>", title_x=0.5, xaxis_title='Year' ,yaxis_title='Energy [TWh]')
        else:
            fig2.update_layout(title=f"<b> {value}'s Annual Energy Development Different Type </b>", title_x=0.5, xaxis_title='Year' ,yaxis_title='Energy [TWh]')
    elif (ri_val == 'Deutsch'):
        if value == None:
            fig2.update_layout(title='<b> Jährliche Energieentwicklung verschiedener Typen von Indonesien </b>', title_x=0.5, xaxis_title='Jahr', yaxis_title='Energie [TWh]')
        else:
            fig2.update_layout(title=f'<b> Jährliche Energieentwicklung verschiedener Typen von {value} </b>', title_x=0.5, xaxis_title='Jahr', yaxis_title='Energie [TWh]')
    return fig2

@callback(
    Output(component_id='bar_click_year_energie', component_property='figure'),
    Input(component_id='line_energie', component_property='clickData'),
    Input(component_id='dropd2', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_bar_energie_click(year, country, ri_val):
    fossil_list = ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity']
    df2 = df[['year', 'country', 'coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity', 'other_renewable_electricity', 'solar_electricity', 'wind_electricity', 'hydro_electricity']]
    if (year == None) and (country == None):
        df2 = df2[(df2['country']=='Indonesia') & (df2['year'] == 2000)]
        df2 = df2.drop(columns=['year']).set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
        df2['source'] = df2['type'].apply(lambda x:'Fossil Fuel' if x in fossil_list else 'Renewables')
        fig2 = px.bar(data_frame=df2, x='source', y='value', color='type')
        if ri_val == 'English':
            fig2.update_layout(title="<b> Indonesia's Energy Composition in the Year 2000 </b>", title_x=0.5 ,xaxis_title='Energy Type', yaxis_title='Energy [TWh]')
        else:
            fig2.update_layout(title="<b>Indonesias Energieverteilung im  Jahr 2000 </b>", title_x=0.5 ,xaxis_title='Energietyp', yaxis_title='Energie [TWh]')
    elif (country != None) and (year == None):
        df2 = df2[(df2['country']==country) & (df2['year'] == 2000)]
        df2 = df2.drop(columns=['year']).set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
        df2['source'] = df2['type'].apply(lambda x:'Fossil Fuel' if x in fossil_list else 'Renewables')
        fig2 = px.bar(data_frame=df2, x='source', y='value', color='type')
        if ri_val == 'English':
            fig2.update_layout(title=f"<b>{country}'s Energy Composition in the Year 2000 </b>", title_x=0.5 ,xaxis_title='Energy Type', yaxis_title='Energy [TWh]')
        else:
            fig2.update_layout(title=f"<b>{country}s Energieverteilung im Jahr 2000 </b>", title_x=0.5 ,xaxis_title='Energietyp', yaxis_title='Energie [TWh]')
    elif (country == None) and (year != None):
        df2 = df2[(df2['country']=='Indonesia') & (df2['year'] == year['points'][0]['x'])]
        df2 = df2.drop(columns=['year']).set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
        df2['source'] = df2['type'].apply(lambda x:'Fossil Fuel' if x in fossil_list else 'Renewables')
        fig2 = px.bar(data_frame=df2, x='source', y='value', color='type')
        if ri_val == 'English':
            fig2.update_layout(title=f"<b>Indonesia's Energy Composition in the Year {year['points'][0]['x']} </b>", title_x=0.5 ,xaxis_title='Energy Type', yaxis_title='Energy [TWh]')
        else:
            fig2.update_layout(title=f"<b>Indonesias Energieverteilung im Jahr {year['points'][0]['x']} </b>", title_x=0.5 ,xaxis_title='Energietyp', yaxis_title='Energie [TWh]')

    else:
        df2 = df2[(df2['year']==year['points'][0]['x']) & (df2['country']==country)]
        df2 = df2.drop(columns=['year']).set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
        df2['source'] = df2['type'].apply(lambda x:'Fossil Fuel' if x in fossil_list else 'Renewables')
        fig2 = px.bar(data_frame=df2, x='source', y='value', color='type')
        if ri_val == 'English':
            fig2.update_layout(title=f"<b>{country}'s Energy Composition in the Year {year['points'][0]['x']} </b>", title_x=0.5 ,xaxis_title='Energy Type', yaxis_title='Energy [TWh]')
        else:
            fig2.update_layout(title=f"<b>{country}s Energieverteilung im Jahr {year['points'][0]['x']} </b>", title_x=0.5 ,xaxis_title='Energietyp', yaxis_title='Energie [TWh]')
    return fig2

@callback(
    Output(component_id='bar_total_energie', component_property='figure'),
    Input(component_id='dropd2', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_bar_total_energie(value, ri_val):
    df_gb1 = df.groupby('country')[['fossil_electricity', 'renewables_electricity', 'nuclear_electricity']].sum()
    if value == None:
        df_fin1 = df_gb1[df_gb1.index=='Indonesia'].unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
        fig = px.bar(data_frame=df_fin1, x='type', y='value')    
        if ri_val == 'English':
            fig.update_layout(title=f"<b> Indonesia's Total Energy Composition </b>", title_x =0.5, yaxis_title= 'Energy [TWh]')
        else:
            fig.update_layout(title=f"<b> Zusammensetzung der Gesamtenergie von Indonesia </b>", title_x =0.5, yaxis_title='Energie [TWh]')
    else:
        df_fin1 = df_gb1[df_gb1.index==value].unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
        fig = px.bar(data_frame=df_fin1, x='type', y='value')    
        if ri_val == 'English':
            fig.update_layout(title=f"<b> {value}'s Total Energy Composition </b>", title_x =0.5, yaxis_title= 'Energy [TWh]')
        else:
            fig.update_layout(title=f"<b> Zusammensetzung der Gesamtenergie von {value} </b>", title_x =0.5, yaxis_title='Energie [TWh]')
    return fig

@callback(
    Output(component_id='pie_fossil', component_property='figure'),
    Input(component_id='dropd2', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_pie_fossil(value, ri_val):
    df_gb1 = df.groupby('country')[['coal_electricity', 'oil_electricity', 'gas_electricity', 'nuclear_electricity']].sum()
    if value == None:
        df_fin1 = df_gb1[df_gb1.index=='Indonesia'].unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    else:
        df_fin1 = df_gb1[df_gb1.index==value].unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    fig =  px.pie(data_frame=df_fin1, values='value', names='type', title='Fossil Composition') 
    if ri_val == 'English':
        if value == None:
            fig.update_layout(title="<b>Indonesia's Fossil Energy</b>", title_x=0.5)
        else: 
            fig.update_layout(title=f"<b>{value}'s Fossil Energy</b>", title_x=0.5)
    elif ri_val == 'Deutsch':
        if value == None:
            fig.update_layout(title="<b>Fossile Energie Indonesiens</b>", title_x=0.5)
        else: 
            fig.update_layout(title=f"<b>Fossile Energie {value}s</b>", title_x=0.5)
    return fig

@callback(
    Output(component_id='pie_renewable', component_property='figure'),
    Input(component_id='dropd2', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_pie_renewable(value, ri_val):
    df_gb1 = df.groupby('country')[['other_renewable_electricity', 'solar_electricity', 'wind_electricity', 'hydro_electricity']].sum()
    if value == None:
        df_fin1 = df_gb1[df_gb1.index=='Indonesia'].unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    else:
        df_fin1 = df_gb1[df_gb1.index==value].unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    fig = px.pie(data_frame=df_fin1, values='value', names='type')
    if ri_val == 'English':
        if value == None:
            fig.update_layout(title="<b>Indonesia's Renewable Energy</b>", title_x=0.5)
        else: 
            fig.update_layout(title=f"<b>{value}'s Renewable Energy</b>", title_x=0.5)
    elif ri_val == 'Deutsch':
        if value == None:
            fig.update_layout(title="<b>Erneuerbare Energien Indonesiens</b>", title_x=0.5)
        else: 
            fig.update_layout(title=f"<b>Erneuerbare Energien {value}s</b>", title_x=0.5)
    return fig
@callback(
    Output(component_id='dropd5', component_property='options'),
        Input(component_id='dropd4', component_property='value'),
)
def update_dd(val):
    return country_code(val)

@callback(
    Output(component_id='headline_energie_comparison', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_headline_compariosn(ri_val):
    if ri_val == 'English':
        return '### Energy Comparison'
    else:
        return '### Energievergleichung'
    
@callback(
    Output(component_id='comparison_energie_text', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_headline_compariosn(ri_val):
    if ri_val == 'English':
        return 'You can pick multiple countries from different continents to be shown in the following bottom graphs. Please refresh the page to reset the countries'
    else:
        return 'Sie können mehrere Länder aus verschiedenen Kontinenten auswählen, um sie in den folgenden unteren Diagrammen anzuzeigen. Bitte aktualisieren Sie die Seite, um die Länder zurückzusetzen'

@callback(
    Output(component_id='fig_compare_fossil', component_property='figure'),
    Input(component_id='dropd5', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_compare_fossil(val, ri_val):
    country_list = countries
    df1 = df[['country', 'coal_electricity', 'oil_electricity', 'gas_electricity', 'nuclear_electricity']]
    df1 = df1.set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    df1 = df1.groupby(['country', 'type']).sum().reset_index()
    if val == None:
        country_list.clear()
        df1 = df1[df1['country']=='Indonesia']
    else:
        country_list.append(val)
        df1 = df1[df1['country'].isin(country_list)]
    fig = px.bar(data_frame=df1, x='country', y='value', color='type')
    if ri_val == 'English':
        fig.update_layout(title='<b>Comparison of Fossil Energy</b>', title_x=0.5, xaxis_title='Countries', yaxis_title='Energy [TWh]')
    else:
        fig.update_layout(title='<b>Vergleich der fossilen Energie</b>', title_x=0.5, xaxis_title='Länder', yaxis_title='Energie [TWh]')
    return fig

@callback(
    Output(component_id='fig_compare_renewable', component_property='figure'),
    Input(component_id='dropd5', component_property='value'),
    Input(component_id='ri', component_property='value')
)
def update_compare_renewable(val, ri_val):
    country_list = countries
    df1 = df[['country', 'solar_electricity', 'hydro_electricity', 'wind_electricity', 'other_renewable_electricity']]
    df1 = df1.set_index('country').unstack().reset_index().rename(columns={'level_0':'type', 0:'value'})
    df1 = df1.groupby(['country', 'type']).sum().reset_index()
    if val == None:
        country_list.clear()
        df1 = df1[df1['country']=='Indonesia']
    else:
        country_list.append(val)
        df1 = df1[df1['country'].isin(country_list)]
    fig = px.bar(data_frame=df1, x='country', y='value', color='type')
    if ri_val == 'English':
        fig.update_layout(title='<b>Comparison of Renewable Energy</b>', title_x=0.5, xaxis_title='Countries', yaxis_title='Energy [TWh]')
    else:
        fig.update_layout(title='<b>Vergleich der erneuerbaren Energie</b>', title_x=0.5, xaxis_title='Länder', yaxis_title='Energie [TWh]')
    return fig

@callback(
    Output(component_id='source_energie', component_property='children'),
    Input(component_id='ri', component_property='value'),
)
def update_source(ri_val):
    if ri_val == 'English':
        return 'Source: https://github.com/owid/energy-data'
    else:
        return 'Quelle: https://github.com/owid/energy-data'


