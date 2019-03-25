from django.db import models


def user_directory_path(instance, filename):
    return 'performers/{0}_{1}'.format(instance.person_id.first_name, instance.person_id.last_name + "." + filename.split(".")[-1])

def gallery_directory_path(instance, filename):
	return '{0}/photos/{1}'.format(instance.event_id.title.replace(" ", "-"), filename)

def sponsor_directory_path(instance, filename):
	return 'sponsors/{0}'.format(filename)

def event_icon_directory_path(instance, filename):
	return '{0}/{1}'.format(instance.title.replace(" ", "-"), filename)


class Interest(models.Model):
	categories = (
		("MUSIC", "Music"),
		("SPORTS", "Sports")
	)

	id = models.IntegerField(primary_key=True)
	category = models.CharField(max_length=20, choices=categories)
	name = models.CharField(max_length=20)

	def __str__(self):
		return u'%s' % (self.name)


class Person(models.Model):
	sex_choices = (
		("M", "Male"),
		("F", "Female"),
		("DNM", "Other")
	)

	id = models.CharField(max_length=10, primary_key=True)
	first_name  = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	sex = models.CharField(max_length=3, choices=sex_choices)
	age = models.PositiveSmallIntegerField()
	email = models.EmailField(blank=True, null=True)
	phone_number = models.CharField(max_length=10, blank=True, null=True, help_text="Only 10-digit mobile number.")
	one_liner = models.TextField(max_length=200, blank=True, null=True)
	interest_area = models.ForeignKey(Interest, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return u'%s %s' % (self.first_name, self.last_name)


class Event(models.Model):
	countries = (
		("IN", "India"),
	)

	id = models.CharField(max_length=10, primary_key=True)
	title = models.CharField(max_length=50)
	one_liner = models.CharField(max_length=500)
	datetime = models.DateTimeField()
	icon = models.ImageField(upload_to=event_icon_directory_path)
	country = models.CharField(max_length=2, choices=countries)
	city = models.CharField(max_length=30)
	venue_name = models.CharField(max_length=50)
	venue_address = models.TextField()
	guest_invites = models.PositiveSmallIntegerField()
	seats_booked = models.PositiveSmallIntegerField()
	appeared = models.PositiveSmallIntegerField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return u'%s' % (self.title)

	class Meta:
		ordering = ['datetime']


class EventFee(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	performer_fee = models.PositiveIntegerField()
	audience_fee = models.PositiveIntegerField()

	def __str__(self):
		return u'%s' % (self.event_id.title)


class EventPersonMap(models.Model):
	person_types = (
		("PAID_PERFORMER", "Paid Performer"),
		("GUEST_PERFORMER", "Guest Performer"),
		("GUEST_SPEAKER", "Guest Speaker"),
		("VOLUNTEER", "Volunteer"),
		("ORGANIZER", "Organizer"),
		("AUDIENCE", "Audience"))

	person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	person_type = models.CharField(max_length=20, choices=person_types)

	def __str__(self):
		return u'%s | %s %s' % (self.event_id.title, self.person_id.first_name, self.person_id.last_name)


class PerformerDetail(models.Model):
	occupation_types = (
		("ST", "Student"),
		("CO", "Corporate"),
		("SE", "Self-Employed"),
		("UE", "Unemployed")
	)

	person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
	bio = models.TextField(blank=True, null=True)
	occupation_type = models.CharField(max_length=2, choices=occupation_types)
	education = models.TextField(help_text="Enter your latest degree.")
	interest_area = models.ForeignKey(Interest, on_delete=models.CASCADE, help_text="Please enter upto 5 aspirational interests.")
	photograph = models.ImageField(upload_to=user_directory_path)
	linkedin_link = models.URLField(blank=True, null=True)
	facebook_link = models.URLField(blank=True, null=True)
	twitter_handle = models.CharField(max_length=50, blank=True, null=True)
	youtube_channel = models.CharField(max_length=50, blank=True, null=True)
	instagram_handle = models.CharField(max_length=50, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return u'%s %s' % (self.person_id.first_name, self.person_id.last_name)


class Sponsor(models.Model):
	sponsor_classes = (
		("PT", "Platinum"),
		("AU", "Gold"),
		("AG", "Silver")
	)

	id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=10, blank=True, null=True)
	email = models.EmailField()
	logo = models.ImageField(upload_to=sponsor_directory_path)
	website = models.URLField()
	sponsor_class = models.CharField(max_length=3, choices=sponsor_classes)

	def __str__(self):
		return u'%s' % self.name


class EventSponsorMap(models.Model):
	sponsorship_types = (
		("MEDIA", "Media"),
		("FINANCIAL", "Financial"),
		("IN KIND", "In Kind")
	)

	sponsor_id = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	sponsorship_type = models.CharField(max_length=10, choices=sponsorship_types)
	amount = models.FloatField(blank=True, null=True)

	def __str__(self):
		return u'%s | %s' % (self.event_id.title, self.sponsor_id.name)


class Freebie(models.Model):
	product_types = (
		("KEYCHAIN", "Key Chain"),
		("STICKER", "Strickers"),
		("SOUVENIR", "Souvenir"),
		("T-SHIRTS", "T-SHIRTS")
	)

	id = models.CharField(max_length=10, primary_key=True)
	product_type = models.CharField(max_length=20, choices=product_types)
	vendor_name = models.CharField(max_length=50)
	vendor_email = models.EmailField(blank=True, null=True)
	vendor_phone = models.CharField(max_length=10, blank=True, null=True)
	pincode = models.IntegerField()
	total_units = models.PositiveSmallIntegerField()
	unit_price = models.FloatField()


class EventFreebieMap(models.Model):
	freebie_id = models.ForeignKey(Freebie, on_delete=models.CASCADE)
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	distribution_count = models.PositiveSmallIntegerField()
	total_cost = models.FloatField()


class TravelCost(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
	cab = models.FloatField()
	flight = models.FloatField(blank=True, null=True)
	other = models.FloatField(blank=True, null=True)
	explain_others = models.CharField(max_length=100, blank=True, null=True)
	total = models.FloatField()

	def __str__(self):
		return u'%s %s' % (self.person_id.first_name, self.person_id.last_name)


class Expense(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	venue = models.FloatField()
	food_inlcusive = models.BooleanField()
	food = models.FloatField(blank=True, null=True)
	sound = models.FloatField(blank=True, null=True)
	camera = models.FloatField(blank=True, null=True)
	media = models.FloatField(blank=True, null=True)
	freebies = models.FloatField(blank=True, null=True)
	travel = models.FloatField(blank=True, null=True)
	others = models.FloatField(blank=True, null=True)
	explain_others = models.CharField(max_length=100, blank=True, null=True)
	total = models.FloatField(blank=True, null=True)

	def __str__(self):
		return u'%s' % self.event_id.title


class Photo(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=gallery_directory_path)

	def __str__(self):
		return u'%s' % self.image


class YouTubeLink(models.Model):
	video_types = (
		("USER_PERFORMANCE", "User Performance"),
		("GUEST_PERFORMANCE", "Guest Performance"),
		("IN_HOUSE", "In House")
	)

	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	link = models.URLField()
	title = models.CharField(max_length=50)
	video_type = models.CharField(max_length=20, choices=video_types)
	description = models.TextField(blank=True, null=True)
	tags = models.CharField(max_length=100, help_text="separated tags with a comma.")
	
	def __str__(self):
		return u'%s' % self.title


class Feedback(models.Model):
	rating_choices = (
		(1, "*"),
		(2, "**"),
		(3, "***"),
		(4, "****"),
		(5, "*****")
	)
	event_person_map = models.ForeignKey(EventPersonMap, on_delete=models.CASCADE)
	rating = models.PositiveIntegerField(choices=rating_choices)
	comment = models.TextField()

	def __str__(self):
		return u'%s | %s' % (self.event_person_map.person_id.id, self.rating)



class Subscriber(models.Model):
	email = models.EmailField()

	def __str__(self):
		return u'%s' % self.email






