# -*- coding: utf-8 -*-
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


def index(request):
	return render(request, 'index.html')

@api_view(('GET',))
def api(request, format=None):
	return Response({
		'reader': reverse('reader-api', request=request, format=format),
	})