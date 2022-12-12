# Import the necessary modules
import json


from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import requests
import json
import pdb
from djangoProject1 import misinfo_getter


# Define the API endpoints
@require_http_methods(["GET", "POST"])
def get_score(request, video_id):
    # Retrieve the data and return as JSON

    # pdb.set_trace()

    if request.method == 'GET':
        id = video_id

        print(id)

        # print(request.data)
        #print(request.path)

        x = misinfo_getter.scrape_youtube(id)
        response = HttpResponse(
            {  x }
        )
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        #print(x)
        print(response)
        #pdb.set_trace()

        return HttpResponse(response)
