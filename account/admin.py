from django.contrib import admin
from models import Profile

"""
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'is_admin', 'joined')

    list_filter = ('joined', 'is_admin')
    search_fields = ('username', 'email')

    date_hierarchy = 'joined'
    ordering = ['joined']
    
admin.site.register(User, UserAdmin)
"""

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'surname', 'phone',
                    'bank', 'account_number', 'matched', 'package',
                    'PH_time', 'PHed', 'no_of_payers', 'no_of_paid',
                    'deactivated',
                    )
    raw_id_fields = ('user',)
    list_filter = ('PHed', 'no_of_payers', 'no_of_paid', 'matched', 'package', 'PH_time',
                   'deactivated')
    raw_id_fields = ('upliner', 'downliner')
    search_fields = ('user', 'upliner', 'downliner', 'first_name', 'surname',
                     'phone', 'bank', 'account_number')
    ordering = ['PHed', 'no_of_payers', 'matched', 'package', 'PH_time']
    
admin.site.register(Profile, ProfileAdmin)

"""
class UserFollowersAdmin(admin.ModelAdmin):
    list_display = ('user', 'count')

    list_filter = ('user', 'count', 'followers')
    raw_id_fields = ('user', 'followers')
    date_hierarchy = 'date'
    ordering = ['date', 'count']
    
admin.site.register(UserFollowers, UserFollowersAdmin)
"""

