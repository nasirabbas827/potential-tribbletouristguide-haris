from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import user_registerForm, LoginForm, UserUpdateForm
from .models import user_register

def register(request):
    if request.method == 'POST':
        form = user_registerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = user_registerForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = user_register.objects.get(username=username)
                if user.password == password:
                    request.session['username'] = username
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid password.')
            except user_register.DoesNotExist:
                messages.error(request, 'Username does not exist.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from .models import user_register, Destination, Event, Activity, TravelTip, Notification, TravelPlan, Booking

def home(request):
    username = request.session.get('username')

    # If the user is not logged in, redirect to landing page
    if not username:
        return redirect('landing_page')

    try:
        # Fetch the user object using the session username
        user = user_register.objects.get(username=username)
    except user_register.DoesNotExist:
        return redirect('login')  # If user does not exist, force re-login

    # Fetch destinations based on user preference
    preferred_season = user.preferred_travel_season
    suggested_destinations = Destination.objects.filter(best_season__icontains=preferred_season)

    # Fetch last visited destination for personalized recommendations
    last_visited_destination = user.last_visited_destination

    # Fetch events and activities related to the last visited destination
    recommended_events = Event.objects.filter(location=last_visited_destination) if last_visited_destination else []
    recommended_activities = Activity.objects.filter(event__location=last_visited_destination) if last_visited_destination else []

    # Fetch all other data
    events = Event.objects.all()
    destinations = Destination.objects.all()
    activities = Activity.objects.all()
    travel_tips = TravelTip.objects.all()
    notifications = Notification.objects.all()  # Get all notifications
    travel_plans = TravelPlan.objects.filter(user=user)  # Fetch travel plans for this user
    bookings = Booking.objects.filter(user=user)  # Fetch bookings for this user

    context = {
        'username': username,
        'suggested_destinations': suggested_destinations,  # Only relevant destinations
        'events': events,
        'destinations': destinations, 
        'activities': activities,
        'travel_tips': travel_tips,
        'notifications': notifications,  # Pass notifications to template
        'travel_plans': travel_plans,  # Pass user travel plans to template
        'bookings': bookings,  # Pass user bookings to template
        'recommended_events': recommended_events,  # Events for the last visited destination
        'recommended_activities': recommended_activities,  # Activities for the last visited destination
    }
    
    return render(request, 'home.html', context)


def landing_page(request):
    """Landing page for unregistered users."""
    destinations = Destination.objects.all()[:6]  # Show a few destinations for preview
    events = Event.objects.all()[:6]  # Show some upcoming events

    context = {
        'destinations': destinations,
        'events': events
    }

    return render(request, 'landing_page.html', context)





def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

def update_profile(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user = get_object_or_404(user_register, username=username)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'update_profile.html', {'form': form})



from .models import Destination, Review
from django.http import HttpResponseRedirect

def all_destinations(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    
    destinations = Destination.objects.all()
    return render(request, 'all_destinations.html', {'destinations': destinations, 'username': username, })

def destination_reviews(request, destination_id):
    username = request.session.get('username')
    if not username:
        return redirect('login')


    destination = get_object_or_404(Destination, id=destination_id)
    reviews = Review.objects.filter(destination=destination)
    return render(request, 'destination_reviews.html', {
        'username': username,
        'destination': destination,
        'reviews': reviews
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Destination, Review, user_register, Like, Reply  # Make sure to import user_register
from .forms import ReviewForm
from django.contrib import messages

def destination_reviews(request, destination_id):
    # Get the destination object by its ID
    destination = get_object_or_404(Destination, id=destination_id)

    # Get all reviews for this destination
    reviews = Review.objects.filter(destination=destination).order_by('-created_at')

    # Check if the user is logged in via session
    username = request.session.get('username')
    
    if not username:
        return redirect('login')  # If no username found in session, redirect to login

    # Fetch the user object using the session username
    try:
        user = user_register.objects.get(username=username)
    except user_register.DoesNotExist:
        return redirect('login')  # If user does not exist, force re-login

    # Handle the form submission (POST request)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new review object but do not save it yet
            review = form.save(commit=False)
            
            # Associate the review with the correct user (from the session)
            review.user = user  # Use the user object retrieved from session
            
            # Associate the review with the correct destination
            review.destination = destination

            # Save the review to the database
            review.save()

            # Add a success message
            messages.success(request, 'Your review has been posted successfully!')

            # Redirect back to the destination reviews page
            return redirect('destination_reviews', destination_id=destination.id)
    else:
        # Initialize an empty form for GET request
        form = ReviewForm()

    # Render the reviews page with the form
    return render(request, 'destination_reviews.html', {
        'username': username,
        'destination': destination,
        'reviews': reviews,
        'form': form
    })



from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Like

def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Check if the user is logged in using session (check for 'username' in the session)
    username = request.session.get('username')
    
    if not username:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    # Fetch the user object based on the username stored in the session
    user = get_object_or_404(user_register, username=username)

    # Check if the user has already liked the review
    like, created = Like.objects.get_or_create(user=user, review=review)
    if not created:
        like.delete()  # If the like already exists, remove it

    # Redirect to the same page after the like action
    return redirect('destination_reviews', destination_id=review.destination.id)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Reply
from .forms import ReplyForm

def post_reply(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Check if the user is logged in using session (check for 'username' in the session)
    username = request.session.get('username')
    
    if not username:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    # Fetch the user object based on the username stored in the session
    user = get_object_or_404(user_register, username=username)

    # Check if the form is valid and process the reply
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = user  # Associate the reply with the logged-in user
            reply.review = review  # Associate the reply with the specific review
            reply.save()  # Save the reply to the database
            
            # Redirect to the same page after posting the reply
            return redirect('destination_reviews', destination_id=review.destination.id)
    else:
        form = ReplyForm()  # Initialize an empty form

    return render(request, 'post_reply.html', {'form': form, 'review': review})


from django.shortcuts import render, get_object_or_404, redirect
from .models import TravelPlan
from .forms import TravelPlanForm

# Create a new Travel Plan
def create_travel_plan(request):
    # Check if the user is logged in using session (check for 'username' in the session)
    username = request.session.get('username')
    if not username:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    if request.method == 'POST':
        form = TravelPlanForm(request.POST)
        if form.is_valid():
            travel_plan = form.save(commit=False)
            travel_plan.user = get_object_or_404(user_register, username=username)  # Assign the logged-in user
            travel_plan.save()
            form.save_m2m()  # Save ManyToMany relations
            return redirect('travel_plan_detail', travel_plan_id=travel_plan.id)
    else:
        form = TravelPlanForm()
    return render(request, 'travel_plans/create_travel_plan.html', {'form': form})

# Read/View a Travel Plan
def travel_plan_detail(request, travel_plan_id):
    # Check if the user is logged in using session (check for 'username' in the session)
    username = request.session.get('username')
    if not username:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    travel_plan = get_object_or_404(TravelPlan, id=travel_plan_id)
    return render(request, 'travel_plans/travel_plan_detail.html', {'travel_plan': travel_plan})

# Update a Travel Plan
def update_travel_plan(request, travel_plan_id):
    # Check if the user is logged in using session (check for 'username' in the session)
    username = request.session.get('username')
    if not username:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    travel_plan = get_object_or_404(TravelPlan, id=travel_plan_id)
    if request.method == 'POST':
        form = TravelPlanForm(request.POST, instance=travel_plan)
        if form.is_valid():
            form.save()
            return redirect('travel_plan_detail', travel_plan_id=travel_plan.id)
    else:
        form = TravelPlanForm(instance=travel_plan)
    return render(request, 'travel_plans/update_travel_plan.html', {'form': form})

# Delete a Travel Plan
def delete_travel_plan(request, travel_plan_id):
    # Check if the user is logged in using session (check for 'username' in the session)
    username = request.session.get('username')
    if not username:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    travel_plan = get_object_or_404(TravelPlan, id=travel_plan_id)
    if request.method == 'POST':
        travel_plan.delete()
        return redirect('travel_plans_list')
    return render(request, 'travel_plans/delete_travel_plan.html', {'travel_plan': travel_plan})

# List all Travel Plans for a user
def travel_plans_list(request):
    # Check if the user is logged in using session (check for 'username' in the session)
    username = request.session.get('username')
    if not username:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    travel_plans = TravelPlan.objects.filter(user__username=username)
    return render(request, 'travel_plans/travel_plans_list.html', {'travel_plans': travel_plans})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, TravelPlan
from .forms import BookingForm

# Create a new Booking
def create_booking(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user = get_object_or_404(user_register, username=username)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = user  # Assign the logged-in user
            booking.save()
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form})

# Read/View a Booking
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

# Update a Booking
def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(instance=booking)

    return render(request, 'bookings/update_booking.html', {'form': form})

# Delete a Booking
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('bookings_list')
    return render(request, 'bookings/delete_booking.html', {'booking': booking})

# List all Bookings for a user
def bookings_list(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user = get_object_or_404(user_register, username=username)
    
    bookings = Booking.objects.filter(user=user)
    return render(request, 'bookings/bookings_list.html', {'bookings': bookings})
