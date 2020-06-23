from django.contrib import admin
from .models import Question, Test, Response, Answer
from django.utils import timezone
# Register your models here.
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['get_question_id', 'get_question_statement', 'get_ans']

    def get_ans(self, obj):
        return obj.get_ans_display()
    def get_question_id(self, obj):
        return obj.question.id
    def get_question_statement(self, obj):
        return obj.question.statement
    get_ans.short_description = 'Correct Option'
    get_question_id.short_description = 'question id'
    get_question_statement.short_description = 'statement'

admin.site.register(Answer, AnswerAdmin)

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]
    list_display = ('id', 'Type', 'statement', 'correct_answer')
    def correct_answer(self, obj):
        return obj.answer.get_ans_display()

admin.site.register(Question, QuestionAdmin)

class TestAdmin(admin.ModelAdmin):
    def stime(self, obj):
        return obj.start_time
    def etime(self, obj):
        return (obj.start_time + timezone.timedelta(minutes=obj.duration))
    stime.admin_order_field = 'timefield'
    stime.short_description = 'Start Time'
    etime.short_description = 'End Time'

    list_display = ('test_code', 'stime', 'etime')

admin.site.register(Test, TestAdmin)

def update_score(modeladmin, request, queryset):
    for response in queryset:
        test = Test.objects.get(test_code = response.test_code)
        questions = test.questions.all()
        score = 0
        for question in questions:
            label = "Q" + str(question.id)
            sbmtd_ans = getattr(response, label)
            if sbmtd_ans == "":
                continue
            if sbmtd_ans == question.answer.ans:
                score += test.corr_score
            else:
                score += test.wrong_score
        response.score = score
        response.save()
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('student_no', 'name', 'branch', 'test_code', 'score')
    actions = [update_score]
    def student_no(self, obj):
        return obj.student.student_number
    def name(self, obj):
        return obj.student.user.first_name+' '+obj.student.user.last_name
    def branch(self, obj):
        return obj.student.get_branch_display()
admin.site.register(Response, ResponseAdmin)