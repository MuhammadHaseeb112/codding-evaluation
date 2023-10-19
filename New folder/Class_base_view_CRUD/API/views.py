from django.shortcuts import render
from django.http import HttpResponse
import io 
from rest_framework.parsers import JSONParser
from .models import Student
from .serializer import StudentSerializer
from rest_framework.renderers import JSONRenderer
import json
from django.views.decorators.csrf import csrf_exempt # used to exempt CSRF in Function base views
# Create your views here.

from django.utils.decorators import method_decorator  # used to exempt CSRF in class base views
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class StudentApi(View):
    def get(self, request, *args, **kwargs):
        # json_data = request.body
        # stream = io.BytesIO(json_data)
        # python_data = JSONParser().parse(stream)
        # id = python_data.get(pk, None)
        # print(id)
        # pk = None
        try:
            pk = kwargs['pk']
        except:
            pk = None
        if pk is not None:
            try:
                stu = Student.objects.get(id=pk)
            except:
                error_data = {'error': 'Student not found.'}
                return HttpResponse(json.dumps(error_data), content_type='application/json', status=404)
                # return HttpResponse(json_data, content_type='application/json')
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')
    
    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = StudentSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')
    
    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        # id = python_data.get('pk')
        pk = kwargs['pk']
        stu = Student.objects.get(id=pk)
        serializer = StudentSerializer(stu, data=python_data, partial=True) # partial=True means its allow data to update partially 
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        pk = kwargs['pk']
        json_data= request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        # id = python_data.get('pk')
        stu = Student.objects.get(id=pk)
        stu.delete()
        res = {'msg': 'Data Deleted'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')

