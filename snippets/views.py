from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer




# Create your views here.
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

@csrf_exempt
def snippet_list(request):
	"""
	List all code snippets, or create a new snippet.
	"""
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
	"""
	Retrieve, update or delete a code snippet.
	"""
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return HttpResponse(status=404)
	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		return JsonResponse(serializer.data)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(snippet, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		snippet.delete()
		return HttpResponse(status=204)

def index(request):
	LEXERS = [item for item in get_all_lexers() if item[1]]
	LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
	STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
	return JsonResponse(LANGUAGE_CHOICES, safe=False)