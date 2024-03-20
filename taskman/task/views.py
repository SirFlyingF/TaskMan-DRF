from django.shortcuts import render

# Create your views here.

tasks = [
    {
        "title" : "Hardcode test one",
        "description" : "Hardcode desc test"
    },
    {
        "title" : "Hardcode test two",
        "description" : "Hardcode desc test"
    }
]

def listview(request):
    return render(request, template_name='task/home.html', context={"tasks":tasks, "title":None})