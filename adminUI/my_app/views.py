from django.shortcuts import render, redirect
from my_app.models import Users


def index(request):
    users_list = Users.objects.all().order_by('id')
    context = {'users_list': users_list}
    if 'delete' in request.POST:
    	user_id = request.POST['delete']
    	Users.objects.filter(id=user_id).delete()
    return render(request, 'my_app/index.html', context)

def _user_save(request, user):
	if "save" in request.POST:
		user.login = request.POST['login']
		user.fullname = request.POST['fullname']
		user.token = request.POST['token']
		user.save()
		return redirect('index')
	return render(request, 'my_app/add.html', {'user': user})    

def add(request):
	user = Users()
	return _user_save(request, user)
	
def edit(request, id):
	user = Users.objects.get(id=id) 
	return _user_save(request, user)
