from django.shortcuts import render
from django.http import HttpResponse
import sys
import os
from agents import run_my_agent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def index(request):
    result = None
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        result = run_my_agent(user_input)
    
    return render(request, "main/index.html", {"result": result})