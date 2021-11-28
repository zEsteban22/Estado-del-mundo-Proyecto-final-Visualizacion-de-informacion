from math import inf
import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# definición de variables para las animaciones
_año=1990
_añoFin=2020

#Cargamos los datos

#Datos Renzo
#df_cambioClimatico = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/1_climate-change.xlsx')
df_precipitaciones = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/2_average-monthly-precipitation.xlsx')
df_CO2 = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/3_co-emissions-per-capita.xlsx')
df_gasesEfectoInvernadero = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
df_poblacion = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/5_future-population-projections-by-country.xlsx')

#Datos Esteban
#df_cambioClimatico = pd.read_excel('Datos/1_climate-change.xlsx')
#df_precipitaciones = pd.read_excel('Datos/2_average-monthly-precipitation.xlsx')
#df_CO2 = pd.read_excel('Datos/3_co-emissions-per-capita.xlsx')
#df_gasesEfectoInvernadero = pd.read_excel('Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
#df_poblacion = pd.read_excel('Datos/5_future-population-projections-by-country.xlsx')

#Para hacer el gráfico de dispersión con todos los datos, se deben meter todos los datos en un mismo dataframe
df_universal=pd.DataFrame([ 
    {#                                                _.-=/ Esta parte es para sacar los registros en un rango de 5 años \=-._                _.-=/ Aquí se hace el pegue por código \=-._                 v Para finalmente sacar el promedio del indicador
        'gasesEI':df_gasesEfectoInvernadero[df_gasesEfectoInvernadero['Año'].between(registro_poblacion['Año']-2,registro_poblacion['Año']+3)][df_gasesEfectoInvernadero['Código']==registro_poblacion['Código']]['Emisiones'].mean(),
        'CO2Percap':df_CO2[df_CO2['Año'].between(registro_poblacion['Año']-2,registro_poblacion['Año']+3)][df_CO2['Código']==registro_poblacion['Código']]['Emisiones'].mean(),
        'Precipitaciones':df_precipitaciones[df_precipitaciones['Año'].between(registro_poblacion['Año']-2,registro_poblacion['Año']+3)][df_precipitaciones['Código']==registro_poblacion['Código']]['Promedio mensual de precipitación'].mean(),
        'Año': registro_poblacion['Año'], 
        'Entidad': registro_poblacion['Entidad'], 
        'Código': registro_poblacion['Código'], 
        'Población': registro_poblacion['Población']
    }
    for i, registro_poblacion in df_poblacion.iterrows() 
    if (registro_poblacion['Código'] == df_precipitaciones['Código']).any() and (registro_poblacion['Código'] == df_CO2['Código']).any() and (registro_poblacion['Código'] == df_gasesEfectoInvernadero['Código']).any()  
])

#Se crean los gráficos
def generarGraficos(año):
    return\
        px.choropleth(df_poblacion[df_poblacion["Año"]==año],
            locations='Código',
            color='Población',
            height=700,
            hover_name='Entidad',
            color_continuous_scale='ylorrd',
            title="Gráfico de proyección de población por país"),\
        px.choropleth(df_CO2[df_CO2["Año"].between(año-2,año+3)].groupby(['Entidad','Código']).mean().reset_index(),
            locations='Código',
            color='Emisiones',
            height=700,
            hover_name='Entidad',
            color_continuous_scale=['green',"yellow",'orange','red'],
            title="Gráfico de emisiones de CO2 per cápita por país"),\
        px.choropleth(df_gasesEfectoInvernadero[df_gasesEfectoInvernadero["Año"].between(año-2,año+3)].groupby(['Entidad','Código']).mean().reset_index(),
            locations='Código',
            color='Emisiones',
            height=700,
            hover_name='Entidad',
            color_continuous_scale=['green',"yellow",'orange','red'],
            title="Gráfico de emisiones totales de gases de efecto invernadero por país"),\
        px.scatter_geo(df_precipitaciones[df_precipitaciones["Año"].between(año-2,año+3)].groupby(['Entidad','Código']).mean().reset_index(),
            locations='Código',
            height=700,
            hover_name='Entidad',
            size='Promedio mensual de precipitación',
            color='Promedio mensual de precipitación',
            color_continuous_scale=['lightblue','darkblue'],
            title="Gráfico de precipitación"),\
        px.scatter(df_universal[df_universal['Año']==año],
            size='Precipitaciones',
            color='Población',
            x='CO2Percap',
            y='gasesEI',
            height=700,
            hover_name='Entidad')

#Se crea la página
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Col([
    dcc.Interval(id="timer",disabled=True,interval=5000),
    html.H1("El Estado del Mundo por año por país.",style={'textAlign': 'center',"marginTop":"20px"}),
    html.Hr(),
    dcc.Slider(
                id='slider_años',
                min=1990,
                max=2015,
                step=5,
                marks={str(year): str(year) for year in range(1970,2020,5)},
                value=_año
            ),
    html.H2("1990", id="año", style={'textAlign': 'center',"marginTop":"20px"}),
    dcc.Graph(id='graficoPoblacion'),
    html.P("En este gráfico vemos como China y la India están muy por encima del resto de países del mundo, pero después de ellos se pueden apreciar a ciertos otros países con tonos más intensos que los de sus vecinos, como Estados Unidos, Brasil, Nigeria, Indonesia y Rusia "),
    dcc.Graph(id='graficoCO2'),
    html.P("En el gráfico anterior se puede apreciar una mayoría de países en tonos blancos y unos cuantos en tonos oscuros de amarillo los cuales son: Estados Unidos, Canadá, Omán, Kazajistán y Australia. Seguido de ellos, en tonos más azules se encuentran ciertos países árabes como lo son: Arabia Saudita, Emiratos Árabes Unidos y Kuwait, así como uno no árabe y que además se encuentra en América el cual es Trinidad y Tobago. Pero además casi imperseptible a simple vista debido a su pequeño territorio está el país con más emisiones de CO2 percápita del mundo: Qatar"),
    dcc.Graph(id='graficogasesEI'),
    html.P("Con la anterior visualización podemos apreciar cómo China lidera el ranking mundial de emisiones de gases de efecto invernadero, teniendo además ciertos países que le siguen relativamente de cerca: Estados Unidos, La India, Rusia y Brazil"),
    dcc.Graph(id='graficoPrecipitaciones'),
    dcc.Graph(id='graficoDispersion')
], width={"size": 8, "offset": 2})#Disposición en pantalla como una sola columna ancha en el centro de la pantalla.

#Se crean los enlaces entre los componentes visuales y los datos visualizados
@app.callback(
    [    
        Output('año','children'),
        Output(component_id='graficoPoblacion', component_property='figure'),
        Output(component_id='graficoCO2', component_property='figure'),
        Output(component_id='graficogasesEI', component_property='figure'),
        Output(component_id='graficoPrecipitaciones', component_property='figure'),
        Output(component_id='graficoDispersion', component_property='figure'),
    ],
    [Input(component_id='slider_años', component_property='value')]
)
def actualizarRango(año):
    return str(año),*generarGraficos(año=año)

if __name__=='__main__':
    app.run_server()