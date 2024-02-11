import pickle
import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash import dash_table
from dash_bootstrap_templates import load_figure_template

# Change the figure theme
load_figure_template('DARKLY')

dash_app = Dash(__name__)

# Loading and processing the data for use with
# pickle and pandas

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_pickle = os.path.join(current_dir, 'spotify_dashboard_data.pkl')

with open(file_path_pickle, 'rb') as file:
    spotify = pickle.load(file)

# Sorting total stream data and making the columns better for display
countries_total_streams = spotify['countries_total_streams'].sort_index(ascending = True)
countries_total_streams.columns = [
        col.replace('_', ' ').capitalize()
        for col in countries_total_streams.columns
]

# Rename columns for better display
new_cols = {'Glbl streams': 'Global streams', 'Middle east north africa west asia streams': 'Middle eastern, north african, west asian streams'}
countries_total_streams.rename(columns = new_cols, inplace = True)

# Sort the cumulative sum streams and rename the columns for better display
cumsum_country_streams = spotify['cumsum_country_bins'].sort_index(ascending = True)
cumsum_country_streams.columns = [
        col.replace('_', ' ').capitalize()
        for col in cumsum_country_streams.columns
]
cumsum_country_streams.rename(columns = new_cols, inplace = True)

# Load the data for the world map
file_path_iso = os.path.join(current_dir, 'iso.csv')
countries_total_songs = pd.read_csv(file_path_iso).drop('Unnamed: 0', axis = 1)

# Load data for artists and drop nan values
artists_streams_to_songs = spotify['filtered_artists_data']
artists_streams_to_songs.dropna(inplace = True)



# The figures for the dashboard

line_chart = px.line(
    cumsum_country_streams,
    x = cumsum_country_streams.index,
    y = cumsum_country_streams.columns,
    title = 'Cumulative streams from Jan. 2017 to Dec. 2021'
)
line_chart.update_layout(
    title = {'x': 0.5},
    xaxis = dict(
        showgrid = False,
        tickmode = 'array',
        tickvals = [],
        fixedrange=True
    ),
    yaxis_title = '',
    xaxis_title = '',
    legend_title_text = 'Region',
    uirevision='True',
    yaxis=dict(fixedrange=True),
    hovermode='closest',
    dragmode=False,
    font = dict(family = 'Montserrat, sans-serif', size = 16)
)

scatter_chart = px.scatter(
    artists_streams_to_songs[artists_streams_to_songs['total_streams'] < 20000000],
    x = 'num_songs',
    y = 'total_streams',
    color_continuous_scale = 'Blues'
)
scatter_chart.update_layout(
    title = {'text': 'Artists top 200 appearences and streams', 'x': 0.5},
    xaxis = dict(
        showgrid = False,
        fixedrange=True
    ),
    yaxis = dict(
        showgrid = False,
        fixedrange=True
    ),
    yaxis_title = 'Total streams',
    xaxis_title = 'Songs with top 200 appearences',
    uirevision='True',
    hovermode='closest',
    dragmode=False,
    font = dict(family = 'Montserrat, sans-serif', size = 16)
)

chloropleth_chart = px.choropleth(
    countries_total_songs, 
    locations="iso_code",
    color="total_songs",
    hover_name="country",
    color_continuous_scale=px.colors.sequential.Blues,
    title = 'Total songs for every country on Spotify'
)
chloropleth_chart.update_layout(
    title = {'text': '', 'x': 0.5},
    coloraxis_colorbar = dict(title = 'Total songs'),
    uirevision='True',
    xaxis=dict(fixedrange=True),
    yaxis=dict(fixedrange=True),
    hovermode='closest',
    dragmode=False,
    font = dict(family = 'Montserrat, sans-serif', size = 16)
)


# CSS styling for markdown
styles = {
    'fontFamily': 'Montserrat, sans-serif',
    'fontSize': '16px',
    'lineHeight': '1.5',
}

# The layout for the dashboard
dash_app.layout = html.Div([
    dcc.Markdown('''
    # Spotify hits

    Below are the results of my analysis on 
    a spotify data set that includes songs
    that were in the top 200 throughout the 
    years 2017 to 2021.
    ''', style = styles),
    html.Div([
        dcc.Markdown('''
        ### Regional listening trends across the planet

        As expected, western cluntries 
        typically have a significant 
        number of listens, likely due to 
        long standing technological 
        infrastructure, leading to more 
        music being created and listened to. 
        While places like Latin America 
        seem to be catching up, which is 
        likely due to increased music 
        production and listening, from 
        better infrastructure and people 
        world wide also taking an interest 
        in the ever increasing popularization
        of latin music.
        ''', style = styles),
        dcc.Graph(
            id = 'cumsum_country_streams', 
            figure = line_chart
        )
    ]),
    html.Br(),
    html.Div([
        dcc.Markdown('''
        ### Artists, song  count by stream volume
        Here you can see points representing
        artists with the number of times a song
        appeared on the top 200 during the 
        years 2017-2021 versus the total 
        streams that they have for those songs.
        ''', style = styles),
        dcc.Graph(
            id = 'artists_streams_to_songs',
            figure = scatter_chart)
    ]),
    html.Br(),
    html.Div([
        dcc.Markdown('''
        ### Total stream volume for songs from a particular country

        Not all countries allow Spotify,
        and I don't believe all countries
        have the necessary infrastfucture
        for an internet service such as Spotify.
        As a result some regions like China
        and most of Africa do not use it.
        ''', style = styles),
        dcc.Graph(
            id = 'countries_total_songs',
            figure = chloropleth_chart)
    ]),
])

if __name__ == '__main__':
    app.run_server(debug = True)
