from rest_framework import viewsets
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser, AllowAny

from student.models import Profile
from .models import Question, Response as res, Test
from .serializers import QuestionSerializer, ResponseSerializer, TestSerializer
from django.utils import timezone 

@api_view(['GET'])
def QuestionsView(request):
    """
    Lists all the questions
    """
    try:
        test = request.user.profile.tests.all()[0]
    except:
        return Response(data={"test": "not registered for any test"}, status=status.HTTP_404_NOT_FOUND)

    now = timezone.now()
    startTime = test.start_time
    endTime = startTime + timezone.timedelta(minutes=test.duration)
    if now < startTime or now > endTime:
        return Response(data={"test":"test has not begun or has ended"}, status=status.HTTP_403_FORBIDDEN)

    queryset = test.questions.all()
    data = { "data" : [] }

    for question in queryset:
        serialzer = QuestionSerializer(question)
        data['data'].append(serialzer.data)
    return Response(data=data)

@api_view(['GET','POST'])
def TestView(request):
    
    if request.method == 'GET':
        try:
            test = request.user.profile.tests.all()[0]
        except:
            return Response(data={"test": "not registered for any test"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TestSerializer(test)
        return Response(serializer.data)
    if request.method == 'POST':
        test_code = request.data.get('test_code', 0)
        if test_code == 0:
            return Response(data = {"test_code" : "test code was not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = request.user.profile
        except:
            return Response(data={"data": "failed", "message": "user does not have a profile"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.profile.tests.all().count():
            return Response(data={"failure" : "already registered for a test"})

        try:
            test = Test.objects.filter(test_code=test_code)[0]
        except:
            return Response(data = {"test_code" : f"test code invalid {test_code}" }, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.profile.tests.add(test)
        return Response(data= {"success": "registered for test"})

@api_view(['GET', 'POST'])
def ResponseView(request):
    try:
        test = request.user.profile.tests.all()[0]
    except:
        return Response(data={"test": "not registered for any test"}, status=status.HTTP_404_NOT_FOUND)
    try:
        response = request.user.profile.response
    except:
        response = res()
        response.student = request.user.profile
        response.test_code = test.test_code
        response.score = 0
        response.save()
    if request.method == 'GET':
        serializer = ResponseSerializer(response)
        data = {}
        data['test_code'] = test.test_code
        for question in test.questions.all():
            label = "Q" + str(question.id)
            data[label]=serializer.data[label]
        return Response(data)
    if request.method == 'POST':
        now = timezone.now()
        startTime = test.start_time
        endTime = startTime + timezone.timedelta(minutes=test.duration)
        if now < startTime or now > endTime:
            return Response(data={"test":"test has not begun or has ended"}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        try:
            qNo = data['questionNo']
            ans = data['correctOption']
            qType = data['questionType']
            label = "Q"+qNo
            if qType != "5":
                assert ans in ['1', '2', '3' ,'4']
            else:
                qset = Question.objects.filter(Type = "5")
                print(qset)
                for index, item in enumerate(qset):
                    if str(item.id) == qNo:
                        label = "algo"+str(index+1)
                        break
                print(label)
        except:
            return Response(data={"failed":"invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            setattr(response, label, data['correctOption'])
            response.save()
        except:
            return Response(data={"failed" :"unable to save response with given input"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"response":"successfully saved "})

@api_view()
@permission_classes([AllowAny])
def error404(request):
    return Response(
        data={
            "status" : "404",
            "error" : "Path not found.",
            # "path" : path
        },
        status=status.HTTP_404_NOT_FOUND
    )

def error500(request):
    return JsonResponse(
        data={
            "status" : "500",
            "error" : "Internal server error.",
            # "path" : path
        },
        status=500
    )
