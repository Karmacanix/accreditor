from django.contrib import admin

# Register your models here.
from simple_history.admin import SimpleHistoryAdmin
from .models import Application, InformationClassification, DHBs, ApplicationType, TechInstall, TechDelivery 


class ApplicationHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["name", "assess_status"]
    history_list_display = ["assess_status"]
    search_fields = ['name', 'user__username']


class InformationClassicationHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["app", "updated",]
    history_list_display = ["app"]
    search_fields = ['name', 'user__username']


class ApplicationTypeHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["name", "icon_html"]
    history_list_display = ["name",]
    search_fields = ['name', ]


class DHBsHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["name", ]
    history_list_display = ["name",]
    search_fields = ['name', ]


class TechDeliveryAdmin(SimpleHistoryAdmin):
	list_display = ["name", ]
	history_list_display = ["name",]
	search_fields = ['name', ]


class TechInstallAdmin(SimpleHistoryAdmin):
	list_display = ["name", ]
	history_list_display = ["name",]
	search_fields = ['name', ]


admin.site.register(Application, ApplicationHistoryAdmin)
admin.site.register(InformationClassification, InformationClassicationHistoryAdmin)
admin.site.register(ApplicationType, ApplicationTypeHistoryAdmin)
admin.site.register(DHBs, DHBsHistoryAdmin)
admin.site.register(TechDelivery, TechDeliveryAdmin)
admin.site.register(TechInstall, TechInstallAdmin)