from django.shortcuts import render
from rest_framework import *
from django.http import HttpResponse
from .serializer import *
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework import status,viewsets
@api_view(['GET'])
def home(request):
    #reverse Relation from gender to Student
    #---------------------------------------------
    # gen=Gender.objects.get(gender='Male')
    # print(gen.student.all())
    #----------------------------------------------
    data=Student.objects.all()
    serializer=StudentSerializer(data,many=True)
    return render(request, 'index.html', {'students_data':serializer.data})
    # return Response({
    #     'status':True,
    #     'Message':'Students Fetched!',
    #     'data':serializer.data
    # })

@api_view(['POST'])
def post_student(request):
    try:
        data=request.data
        serializer=StudentSerializer(data=data)
        print(data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status':True,
                'Message':'successfully created Student!',
                'data':data
            })
    except Exception as e:
        print(e)
    return Response({
        'status':False,
        'Message':'Something Went Wrong',
        'data':serializer.errors
    })


@api_view(["DELETE"])
def delete_student(request, id):
    data = Student.objects.get(id=id)
    print(data)
    if not hasattr(data, 'id'):
        return Response({
            'status': False,
            'message': 'id is required',
            'data': {}
        })

    data.delete()

    return Response({
        'status': 200,
        'message': 'Successfully deleted',
    })

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            if not data.get('id'):
                return Response({
                    'status': False,
                    'message': 'id is required',
                    'data' :{}
                    })
            Student_obj=Student.objects.get(id=data.get('id'))
            data = request.data
            serializer=StudentSerializer(Student_obj,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': 'Successfully Student Updated!',
                    'data':data
                    })
        except Exception as e:
            print(e)
        return Response({
                    'status': False,
                    'message': 'Nothing Happened!',
                    'data':{}
                    })

    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data
            if not data.get('id'):
                return Response({
                'status': False,
                'message': 'id is required',
                'data' :{}
             })
            obj=Student.objects.get(id = data.get('id'))
            serializer =StudentSerializer(obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': 'Success Student Patched!',
                    'data':serializer.data
            })
            return Response({
            'status': False,
            'message': 'Something Went Wrong!',
            'data':serializer.errors
            })
        except Exception as e:
            print(e)
        return Response({
            'status':False,
            'message':'Invalid id',
            'data':{}
    })




