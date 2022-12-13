from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.http import HttpResponse
import geoip2.database
import geoip2.errors
from .forms import Loginform
from . import models
from .mixin import VerifyLocation

class Requesthandler(VerifyLocation, APIView):

    def get(self, request, *args, **kwargs):
        form = Loginform()
        template = "demo.html"
        return HttpResponse(render(request, template, {"form":form}))

    def post(self, request, *args, **kwargs):
        self.DidLocationChange(request)
        user = authenticate(username = request.POST['Username'],
                            password = request.POST['Password']
                            )

        if user:
            try:
                with geoip2.database.Reader(
                    "c:/users/g-corp/geolite2-city.mmdb"
                    ) as ipdata:
                    ipdetails = ipdata.city(request.META["REMOTE_ADDR"])
            except geoip2.errors.GeoIP2Error:
                ipdetails = None

            if ipdetails is not None:
                if ipdetails.city.name:
                    models.UserDetails.objects.update(
                        username = request.POST['Username'],
                        country = ipdetails.country.name,
                        city = ipdetails.city.name,
                        longitude = ipdetails.location.longitude,
                        latitude = ipdetails.location.latitude,
                        deviceName = request.META['HTTP_USER_AGENT'],
                        date = datetime.today()
                        )
                else:
                    models.UserDetails.objects.update(
                        username = request.POST['Username'],
                        country = ipdetails.country.name,
                        city = "nodata",
                        longitude = ipdetails.location.longitude,
                        latitude = ipdetails.location.latitude,
                        deviceName = request.META['HTTP_USER_AGENT'],
                        date = datetime.today()
                        )
                    
            return HttpResponse("Logged in Successfully!")

        form = Loginform()
        return HttpResponse(render(request, 'demo.html', {'form':form}))


        
