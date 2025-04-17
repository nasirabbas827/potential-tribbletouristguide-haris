from django.db import models

class user_register(models.Model):
    id = models.AutoField(primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    full_name = models.CharField(max_length=255, default="John Doe")
    first_name = models.CharField(max_length=100, default="John")
    last_name = models.CharField(max_length=100, default="Doe")
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Consider hashing passwords properly
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    age = models.PositiveIntegerField(default=18)
    
    nationality = models.CharField(max_length=100, default="Pakistani")
    city = models.CharField(max_length=100, default="Lahore")
    postal_address = models.TextField(default="123 Default Street")
    mobile_no = models.CharField(max_length=15, blank=True, null=True)  # Not unique anymore

    AGE_RANGE_CHOICES = [
    ('18-25', '18-25'),
    ('26-35', '26-35'),
    ('36-45', '36-45'),
    ('46-60', '46-60'),
    ('60+', '60+'),
    ]

    age_range = models.CharField(
    max_length=10,
    choices=AGE_RANGE_CHOICES,
    default='18-25',
    blank=True,
    null=True
    )

    preferred_travel_season = models.CharField(max_length=50, choices=[
        ('Summer', 'Summer'),
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Autumn', 'Autumn'),
        ('All Seasons', 'All Seasons'),
    ], default="Summer")

    preferred_travel_type = models.CharField(max_length=50, choices=[
        ('Adventure', 'Adventure'),
        ('Relaxation', 'Relaxation'),
        ('Cultural', 'Cultural'),
        ('Historical', 'Historical'),
        ('Nature', 'Nature'),
    ], default="Adventure")

    budget_range = models.CharField(max_length=50, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ], default="Low")

    # Last visited destination
    last_visited_destination = models.ForeignKey(
        'Destination',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='last_visited_by_users'
    )
    # Last visited destination
    last_visited_destination = models.ForeignKey(
        'Destination',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='users_last_visited'
    )

    def __str__(self):
        return f"{self.username} - {self.full_name}"



from django.db import models

class Destination(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    best_season = models.CharField(max_length=50, blank=True, null=True, default="All Seasons")
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    activities = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Travel Tip Model
class TravelTip(models.Model):
    id = models.AutoField(primary_key=True)
    tip_title = models.CharField(max_length=255, unique=True)
    tip_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tip_title

# Event Model
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    date = models.DateField()
    location = models.ForeignKey(Destination, on_delete=models.CASCADE)  # Linked to a Destination
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location.name}"

# Activity Model
class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Activity linked to an Event
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.event.title}"

# Notification Model
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification - {self.message[:30]}..."



class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    user = models.ForeignKey(user_register, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    review_image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s review for {self.destination.name}"
    
# Likes Model
class Like(models.Model):
    user = models.ForeignKey(user_register, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.review.destination.name}'s review"

# Replies Model 
class Reply(models.Model):
    user = models.ForeignKey(user_register, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, related_name='replies', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.review.destination.name}'s review"


class TravelPlan(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(user_register, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    destinations = models.ManyToManyField(Destination)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='planning')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s plan: {self.title}"

class Booking(models.Model):
    TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('flight', 'Flight'),
        ('tour', 'Tour'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(user_register, on_delete=models.CASCADE)
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, null=True, blank=True)
    booking_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    provider_name = models.CharField(max_length=255)
    booking_reference = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='confirmed')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s {self.booking_type} booking with {self.provider_name}"