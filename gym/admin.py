from django.contrib import admin
from .models import *
#from django_jalali.admin.filters import JDateFieldListFilter

admin.sites.AdminSite.site_header = 'پنل مدیریت ورزشکاران'
admin.sites.AdminSite.site_title = "پنل مدیریت"
admin.sites.AdminSite.index_title = 'ویرایش اطلاعات'

class ImageInline(admin.TabularInline):
     model=Image
     extra = 0   


@admin.register(Costumer)
class PostAdmin(admin.ModelAdmin):
   list_display = ['title','user_c']
   ordering = ['title']
   list_filter =['user_c']
   search_fields =['title','description']
   rew_id_flield =['user_c']
#   date_hierarchy ='publish'
#   prepopulated_fields = {'slug':['title']}
#   list_editable = ['status']
   list_display_links = ['user_c']
   inlines = [ImageInline]
   
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']

#class ImageInline(admin.TabularInline):
#     model=Image
#     extra = 1     

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'bio', 'job', 'photo']
    