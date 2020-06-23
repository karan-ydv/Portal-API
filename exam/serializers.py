from rest_framework import serializers
from .models import Question, Test, Response as res
import datetime

class OptionListField(serializers.ListField):
    child = serializers.CharField()

class QuestionSerializer(serializers.ModelSerializer):
    questionType = serializers.CharField(source='Type')
    questionCode = serializers.CharField(source='code')
    questionDesc = serializers.CharField(source='statement')
    questionOptions = serializers.SerializerMethodField('get_options')
    questionNo = serializers.IntegerField(source='id')
    
    class Meta:
        model = Question
        fields = ('questionType', 'questionDesc', 'questionCode', 'questionOptions', 'questionNo')
    
    def get_options(self, obj):
        return [obj.A, obj.B, obj.C, obj.D ]

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = res
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    positive_marks = serializers.CharField(source='corr_score')
    negative_marks = serializers.CharField(source='wrong_score')
    end_time = serializers.SerializerMethodField(method_name='get_end_time')
    number_of_questions = serializers.SerializerMethodField(method_name='get_number_of_questions')
    class Meta:
        model = Test
        fields = ('test_code', 'start_time', 'end_time', 'positive_marks', 'negative_marks', 'number_of_questions')
    def get_number_of_questions(self, obj):
        return obj.questions.all().count()
    def get_end_time(self, obj):
        return (obj.start_time + datetime.timedelta(minutes = obj.duration))