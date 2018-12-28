from django.shortcuts import render
from django.views.generic import View
import io
from rest_api.models import Employee
from rest_api.serializers import EmployeeSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse

# Create your views here.
"""
A view function is simply a Python function that takes a Web request and returns a Web response,
This response can be the HTML contents of a Web page, or a redirect, or a 404 error, or an XML document, or an image . . . or anything 
The view itself contains whatever arbitrary logic is necessary to return that response,

They are callable. A view can be either function or a class-based view. CBVs inherit the method as_view() which uses a dispatch() method to call the appropriate method depending on the HTTP verb (get, post, etc)
They must accept an HttpRequest object as its first positional argument
They must return an HttpResponse object or raise an exception
When writing views, we have a choice: function- or class-based? Both have their advantages and disadvantages.

Function-Based Views
explicit and easy to read/understand
use conditionals to handle different HTTP methods
not reusable; can sometimes lead to code duplication and bigger view files
use decorators to add functionality
good for one-off or specialized functionality
Class-Based Views
can be a bit more implicit and difficult to read, especially when using Django’s generic views
rely on the dispatch() method inherited from View to call different HTTP methods
because they are classes, they are reusable through inheritance, and we can add functionality with mixins
good for functionality which will be repeated in multiple places in an application
 """
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt,name='dispatch') 
class EmployeeCRUD_CBV(View):
 	def get(self, request, *args, **kwargs):
 		json_data = request.body
 		stream = io.BytesIO(json_data)
 		data = JSONParser().parse(stream)
 		id = data.get('id', None)
 		if id is not None:
 			emp = Employee.objects.get(id=id)
 			serializers = EmployeeSerializer(emp)
 			json_data = JSONRenderer().render(serializers.data)
 			return HttpResponse(json_data, content_type='application/json')
 		qs = Employee.objects.all()
 		serializers = EmployeeSerializer(qs, many=True)
 		json_data = JSONRenderer().render(serializers.data)
 		return HttpResponse(json_data, content_type='application/json') 

 	def post(self, request, *args, **kwargs):
 		json_data =request.body
 		stream = io.BytesIO(json_data)
 		data = JSONParser().parse(stream)
 		serializer = EmployeeSerializer(data = data)
 		if serializer.is_valid():
 			serializer.save()
 			msg = {'msg':'Create resource successfully'}
 			json_data = JSONRenderer().render(msg)
 			return HttpResponse(json_data, content_type='application/json')
 		json_data = JSONRenderer().render(serializer.errors)
 		return HttpResponse(json_data, content_type='application/json')

 	# def put(self, request, *args, **kwargs):
 	# 	json_data = request.body
 	# 	stream = io.BytesIO(json_data)
 	# 	data =JSONParser().parse(stream)
 	# 	id = data.get('id', None)
 	# 	if id is not None:
 	# 		emp = Employee.objects.get(id=id)
 	# 		serializer = EmployeeSerializer(data = data)
 	# 		if serializer.is_valid():
 	# 			serializer.save()
 	# 			msg = {'msg':'Update resourece successfully'}
 	# 			json_data = JSONRenderer().render(msg)
 	# 			return HttpResponse(json_data, content_type='application/json')
 	# 		json_data = JSONRenderer().render(serializer.errors)
 	# 		return HttpResponse(json_data, content_type='application/json')


