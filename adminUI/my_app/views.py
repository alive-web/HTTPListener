from django.shortcuts import render

from my_app.models import Users


def index(request):
    users_list = Users.objects.all().order_by('login')
    context = {'users_list': users_list}
    return render(request, 'my_app/index.html', context)