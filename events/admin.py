from django.contrib import admin
from .models import *


def fullname(obj):
	if isinstance(obj, Person):
		return ("%s %s" % (obj.first_name, obj.last_name))
	elif isinstance(obj, Feedback):
		return ("%s %s" % (obj.event_person_map.person_id.first_name, obj.event_person_map.person_id.last_name))

	return ("%s %s" % (obj.person_id.first_name, obj.person_id.last_name))


def event_name(obj):
	if isinstance(obj, Feedback):
		return ("%s" % (obj.event_person_map.event_id.title))

	return ("%s" % (obj.event_id.title))


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'city', 'country', 'datetime')


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
	list_display = ('name', 'category')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	list_display = ('id', fullname, 'age', 'sex')


@admin.register(Freebie)
class FreebieAdmin(admin.ModelAdmin):
	list_display = ('id', 'product_type', 'vendor_name', 'unit_price', 'total_units')


@admin.register(EventFee)
class EventFeeAdmin(admin.ModelAdmin):
	list_display = (event_name, 'performer_fee', 'audience_fee')


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'email', 'website')


@admin.register(PerformerDetail)
class PerformerDetailAdmin(admin.ModelAdmin):
	list_display = (fullname, 'occupation_type')


@admin.register(TravelCost)
class TravelCostAdmin(admin.ModelAdmin):
	list_display = (fullname, event_name, 'cab', 'flight', 'total')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = (event_name, 'venue', 'food', 'sound', 'camera', 'freebies', 'travel', 'others', 'total')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = (event_name, 'image')


@admin.register(YouTubeLink)
class YouTubeLinkAdmin(admin.ModelAdmin):
	list_display = ('title', event_name, 'link', 'description')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
	list_display = (fullname, event_name, 'rating', 'comment')


admin.site.register(Subscriber)
admin.site.register(EventPersonMap)
admin.site.register(EventSponsorMap)
admin.site.register(EventFreebieMap)
