from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from roadmap.repository import LocationDB
# import pandas as pd

# Create your views here.
def index(request, dataset='哺乳室'):
    LDB = LocationDB()
    rows, locations, names = LDB.getLocationsByDataset(dataset)
    template = loader.get_template('roadmap/index.html')
    context = {
        'rows':rows, 
        'locations': locations,
        'titles': names,
        'dataset':dataset
        }
    return HttpResponse(template.render(context, request))
