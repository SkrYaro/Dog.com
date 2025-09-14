from django.urls import path

from panel import views, adminView

urlpatterns = [
    path("report/chat:<int:chat_id>",views.chat,name = "reportChat"),
    path("report/close/chat:<int:chat_id>",views.close,name = "closeChat"),
    path("report/list/user:<int:user_id>",views.chat_list,name = "reportList"),
    path("report/create/chat",views.createReport ,name = "reportCreate"),
    path("moder/list",adminView.admin_list,name = "adminReportList"),
    path("model/report/del/<int:chat_id>",adminView.dele,name = "adminReportDelete"),
    ]