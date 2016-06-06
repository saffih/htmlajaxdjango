from django.conf.urls import url

from . import views
urlpatterns = [
   # examples
   url(r'^htmlajax$|^$', views.HtmlAjaxView.as_view()),
   url(r'^htmlajaxurl$', views.ContactView.as_view()),
   url(r'^htmlajaxsuccess$', views.HtmlAjaxSuccessView.as_view()),
   url(r'^hello$', views.hello),
]

