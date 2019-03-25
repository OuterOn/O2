from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from events.models import *
#from events.serializers import *
# from django.db.models import Q
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
from outeron_backend.settings import MEDIA_ROOT, MEDIA_URL

import os, pytz
from datetime import datetime
from termcolor import colored

utc=pytz.UTC


def home(request):
	upcoming_events = Event.objects.filter(datetime__gte = datetime.now())
	past_events = Event.objects.filter(datetime__lte = datetime.now())
	total_perfs = [YouTubeLink.objects.filter(event_id=event, video_type__endswith = "PERFORMANCE").count() for event in past_events]
	past_events_data = zip(past_events, total_perfs)
	feedbacks = Feedback.objects.filter(rating__gte = 3)

	events = {
		"upcoming": upcoming_events,
		"past": past_events_data,
		"feedbacks": feedbacks
	}

	return render(request, 'events/index.html', events)


def event(request, event_id):
	event = Event.objects.get(id=event_id)
	
	sponsors = [Sponsor.objects.get(id=obj.sponsor_id.id) for obj in EventSponsorMap.objects.filter(event_id=event_id)]
	persons = [obj.person_id for obj in EventPersonMap.objects.filter(event_id=event_id, person_type='GUEST_PERFORMER')]
	per_details = list(PerformerDetail.objects.filter(person_id__in=[p.id for p in persons]))
	per_details.sort(key=lambda per_detail: persons.index(per_detail.person_id))
	guests = list(zip(persons, per_details))

	data = dict()
	data["event_obj"] = event
	data["sponsors"] = sponsors
	data["guests"] = guests

	if event.datetime.replace(tzinfo=utc) >= datetime.now().replace(tzinfo=utc):
		prices = EventFee.objects.get(event_id=event_id)
		
		data["prices"] = prices

		return render(request, 'events/pre_event.html', data)

	else:
		photos = [MEDIA_URL + event.title.replace(" ", "-") + "/photos/" + img for img in os.listdir(MEDIA_ROOT + event.title.replace(" ", "-") + "/photos/")]
		yt_links = YouTubeLink.objects.filter(event_id=event_id)
		epm_obj = EventPersonMap.objects.filter(event_id=event_id)
		feedbacks = Feedback.objects.filter(event_person_map__in = epm_obj)

		data["photos"] = photos
		data["yt_links"] = yt_links
		data["feedbacks"] = feedbacks

		return render(request, 'events/post_event.html', data)


def subscribe(request):
	if request.method == "POST":
		if Subscriber.objects.filter(email=request.POST["email"]).count() == 0:
			Subscriber.objects.create(email=request.POST["email"])
			message = "Email added succesfully. Thank you for subscribing."
		else:
			message = "You have already subscribed."
	
	return JsonResponse({"message": message})


def contact(request):
	if request.method == "POST":
		data = request.POST
		message = "Name: %s\n\nEmail: %s\n\nMessage: %s" % (data['name'], data['email'], data['message'])
		try:
			send_mail(
		    	data['subject'],
		    	message,
		    	'imnobody0396@gmail.com',
		    	['outeron.o2@gmail.com'],
		    	fail_silently=False
			)
		except ConnectionRefusedError as e:
			return JsonResponse({"success": "false"})
		return JsonResponse({"success": "true"})

	if request.method == "GET":
		return render(request, 'events/contact.html')


def about(request):
	return render(request, 'events/about.html')


def gallery(request):
	all_links = YouTubeLink.objects.all()
	solo = all_links.filter(tags__icontains = "solo")
	duet = all_links.filter(tags__icontains = "duet")
	group = all_links.filter(tags__icontains = "group")

	data = {
		"all": all_links,
		"solo": solo,
		"duet": duet,
		"group": group
	}
	return render(request, 'events/gallery.html', data)

"""
@csrf_exempt
def event_list(request):
	if request.method == 'GET':
		events = []
		for event in Event.objects.all():
			event_obj = {}
			event_obj["name"] = event.name
			events.append(event_obj)

		return JsonResponse(events, safe=False)

	# elif request.method == 'POST':
	# 	data = JSONParser().parse(request)
	# 	serializer = EventSerializer(data=data)
		
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return JsonResponse(serializer.data, status=201)
	# 	return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def event_detail(request, pk):
    
    try:
        event = Event.objects.get(pk=pk)
        person_list = [EPMobj.person_id for EPMobj in EventPersonMap.objects.filter(event_id=event.event_id, person_type__in=["GUEST_PERFORMER", "ORGANIZER"])]

    except Event.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        event_info = EventSerializer(event)
        guest_list = PersonSerializer(person_list, many=True)
        
       	response = {
        	"event_info": event_info.data,
        	"guest_list": guest_list.data
        }
        return JsonResponse(response)
"""
