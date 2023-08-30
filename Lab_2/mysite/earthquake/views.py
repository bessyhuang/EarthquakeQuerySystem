from django.shortcuts import render
from decouple import config
from pymongo import MongoClient
from .forms import SearchForm

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# Create your views here.
dbClient = MongoClient(config('MONGODB_CONNECTION_STRING'))
dbInUse = dbClient.Earthquake


def index(request):
    context = { 'search_form': SearchForm() }
    return render(request, 'earthquake/index.html', context)


def search(request):
    context = {}
    if request.method == 'POST':
        mag_search = request.POST['fsearch_mag']
        result = list(dbInUse.global_earthquake.find({'mag': { '$gte': eval(mag_search)}}))
        context['Earthq'] = result
        
        if (result != []):
            df = pd.DataFrame(result)
            fig = px.density_mapbox(df, lat='latitude', lon='longitude', radius=10,
                        center=dict(lat=0, lon=180), zoom=0, mapbox_style="stamen-terrain", z='mag')
            graph = fig.to_html(full_html=False, default_height=600, default_width=1000)
            context['fig'] = graph
            return render(request, 'earthquake/search_result.html', context)
        else:
            return render(request, 'earthquake/search_result.html', context)
