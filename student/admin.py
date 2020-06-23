from django.contrib import admin
from .models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['student_number', 'get_name', 'get_username', 'branch', 'get_test_code']
    def get_name(self, obj):
        return obj.user.first_name +' '+ obj.user.last_name
    def get_username(self, obj):
        return obj.user.username
    def get_test_code(self, obj):
        if hasattr(obj.user.profile, 'test'):
            return obj.user.profile.test.test_code
        return None
    get_name.short_description = 'Name'
    get_username.short_description = 'Userame'
    get_test_code.short_description = 'Test Code'
admin.site.register(Profile, ProfileAdmin)
