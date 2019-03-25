from rest_framework import serializers
from events.models import *


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event 
		fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = Person
 		fields = ('name', 'youtube_channel', 'linkedin_profile_link', 'facebook_profile_link', 'twitter_profile_link')
