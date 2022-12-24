from django.contrib import admin
from .models import Menu, MenuActions, WorkSpaceUser, Role, Channel, ReportText, Reports
from django.utils.html import format_html


class ReportsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Reports, ReportsAdmin)


class ChannelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Channel, ChannelAdmin)


class ReportTextAdmin(admin.ModelAdmin):
    pass


admin.site.register(ReportText, ReportTextAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'Role']


admin.site.register(Role, RoleAdmin)


class WorkSpaceUserAdmin(admin.ModelAdmin):
    def image(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.ImageURL))

    list_display = ['FirstName',
                    'LastName',
                    'FullName',
                    'Email',
                    'PhoneNumber',
                    'image',
                    'DateJoined',
                    'RoleDescription']


admin.site.register(WorkSpaceUser, WorkSpaceUserAdmin)


class MenuAdmin(admin.ModelAdmin):
    list_display = ['MenuDescription']


admin.site.register(Menu, MenuAdmin)


class MenuActionsAdmin(admin.ModelAdmin):
    pass


admin.site.register(MenuActions, MenuActionsAdmin)
