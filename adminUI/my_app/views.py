from django.shortcuts import render, redirect

from my_app.models import Users



def index(request):
    users_list = Users.objects.all().order_by('id')
    context = {'users_list': users_list}
    if 'delete' in request.POST:
    	user_id = request.POST['delete']
    	Users.objects.filter(id=user_id).delete()
    if  'edit' in request.POST:
    	id= request.POST['edit']
    	return redirect('/users/edit/%s'%id)
    return render(request, 'my_app/index.html', context)

def add(request):
	if "save" in request.POST:
		user = Users()
		user.login = request.POST['login']
		user.fullname = request.POST['fullname']
		user.token = request.POST['token']
		user.save()
		return redirect('index')
	return render(request, 'my_app/add.html')
def edit(request, id):
	if "save" in request.POST:
		user = Users.objects.get(id=id) 
		user.login = request.POST['login']
		user.fullname = request.POST['fullname']
		user.token = request.POST['token']
		user.save()
		return redirect('index')
	return render(request, 'my_app/add.html')
