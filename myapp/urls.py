from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from .import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('', views.landing_page, name='landing_page'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('captcha/', include('captcha.urls')),
    path('all-destinations/', views.all_destinations, name='all_destinations'),
    path('destination/<int:destination_id>/reviews/', views.destination_reviews, name='destination_reviews'),
    path('post_reply/<int:review_id>/', views.post_reply, name='post_reply'),
    path('like_review/<int:review_id>/', views.like_review, name='like_review'),
    path('create/', views.create_travel_plan, name='create_travel_plan'),
    path('<int:travel_plan_id>/', views.travel_plan_detail, name='travel_plan_detail'),
    path('<int:travel_plan_id>/edit/', views.update_travel_plan, name='update_travel_plan'),
    path('<int:travel_plan_id>/delete/', views.delete_travel_plan, name='delete_travel_plan'),
    path('travel-plans/', views.travel_plans_list, name='travel_plans_list'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('update/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('list/', views.bookings_list, name='bookings_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
