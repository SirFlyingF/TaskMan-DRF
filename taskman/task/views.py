from django.shortcuts import render

# Create your views here.


def listview(request):
    return render(request, template_name='task/home.html', context={"tasks":tasks, "title":None})