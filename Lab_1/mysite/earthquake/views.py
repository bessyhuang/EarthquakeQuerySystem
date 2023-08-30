from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
from pymongo import MongoClient


# Create your views here.
dbClient = MongoClient(config('MONGODB_CONNECTION_STRING'))
dbInUse = dbClient.Earthquake


def index(request):
    result = list(dbInUse.global_earthquake.find(
		{'latitude': {'$gt': 70}}, 
		{'_id': 0, 'place': 1, 'depth': 1, 'time': 1, 'mag': 1}
	     ))
    return HttpResponse(result)

