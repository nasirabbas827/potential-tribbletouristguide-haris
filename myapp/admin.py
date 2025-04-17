from django.contrib import admin
from .models import user_register  , Destination , Event , Notification , TravelTip , Activity

admin.site.register(user_register)
admin.site.register(Destination)
admin.site.register(Event)
admin.site.register(TravelTip)
admin.site.register(Notification)
admin.site.register(Activity)


