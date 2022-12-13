from django.core import mail
import geoip2.database
import geoip2.errors
from . import models
from django.http import HttpResponse

# Mixin defination
class VerifyLocation:

    def send_alert(self, details):
        # send the email.
        recepient = details.username
        sender = "securitymeasure@email.com"
        subject = "Suspected login attempt detected"
        message = """Someone tries to access your account from
                  somewhere
                  """
        connectionbackend = mail.get_connection(
            "django.core.mail.backends.console.EmailBackend"
            )
        mail.send_mail(subject, message, sender, [recepient],
                       connection = connectionbackend
                       )


    def DidLocationChange(self, request):
        try:
            details = models.UserDetails.objects.get(
                username=request.POST['Username']
                )

            try:
                with geoip2.database.Reader(
                    # Replace this path with a path to geoip database file path
                    "c:/users/g-corp/geolite2-city.mmdb"
                    ) as ipdata:
                    # Reading the ip details.
                    ipdetails = ipdata.city(request.META["REMOTE_ADDR"])
                    
            except geoip2.errors.GeoIP2Error:
                ipdetails = None

            if ipdetails:
                # If visistor's country differs with the stored original contry
                # send alert.
                if details.country != ipdetails.country.name:
                    self.send_alert(details)

                # If country matches the stored country info and city fails,
                # send alert.
                elif details.city != "nodata" and ipdetails.city.name is not None:
                    if details.city != ipdetails.city.name:
                        self.send_alert(details)

                elif details.city == "nodata" and ipdetails.city.name is not None:
                    self.send_alert(details)

                elif details.city != "nodata" and ipdetails.city.name is None:
                    self.send_alert(details)

                # If country and city matched the stored country, city information,
                # then coordinates check is run.
                elif (details.longitude != ipdetails.location.longitude
                      and details.latitude != ipdetails.location.latitude
                      ):
                    self.send_alert(details)

                return None
                
        except models.UserDetails.DoesNotExist:

            auth = authenticate(username = request.POST['Username'],
                                password = request.POST['Password']
                                )

            if auth:
                try:
                    with geoip2.database.Reader(
                        # Replace this path with a path to geoip database file path
                        "c:/users/g-corp/geolite2-city.mmdb"
                        ) as ipdata:
                        # Reading ip details.
                        ipdetails = ipdata.city(request.META["REMOTE_ADDR"])
                        
                except geoip2.errors.GeoIP2Error:
                    ipdetails = None

                if ipdetails is not None:
                    if ipdetails.city.name:
                        models.UserDetails.objects.create(
                            username = request.POST['Username'],
                            country = ipdetails.country.name,
                            city = ipdetails.city.name,
                            longitude = ipdetails.location.longitude,
                            latitude = ipdetails.location.latitude,
                            deviceName = request.META["HTTP_USER_AGENT"],
                            date = datetime.today()
                            )

                    else:
                        models.UserDetails.objects.create(
                            username = request.POST['Username'],
                            country = ipdetails.country.name,
                            city = "nodata",
                            longitude = ipdetails.location.longitude,
                            latitude = ipdetails.location.latitude,
                            deviceName = request.META["HTTP_USER_AGENT"],
                            date = datetime.today()
                            )
            return None
