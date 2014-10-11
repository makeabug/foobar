# -*- coding: utf-8 -*-
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


def index(request):
	return render(request, 'index.html')

@api_view(('GET',))
def api_root(request, format=None):
	"""
	This is the entry point for the API described in the
	Follow the hyperinks each resource offers to explore the API.
	Note that you can also explore the API from the command line,
	  for instance using the `curl` command-line tool.
	For example: `curl -X GET http://restframework.herokuapp.com/
	-H "Accept: application/json; indent=4"`
	"""
	return Response({
		'reader': reverse('readers:reader-api', request=request, format=format),
	})