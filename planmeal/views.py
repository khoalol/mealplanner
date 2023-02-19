from django.utils import timezone
from datetime import timedelta
from .models import Meal, MealPlan
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


def index(request):
    # Get the current week's meal plan
    current_date = timezone.now().date()
    current_week_start = current_date - timedelta(days=current_date.weekday())
    current_week_end = current_week_start + timedelta(days=6)
    current_week_meals = MealPlan.objects.filter(date__range=(current_week_start, current_week_end)).order_by('date', 'meal_type')

    # Get the previous week's meal plan
    prev_week_start = current_week_start - timedelta(days=7)
    prev_week_end = current_week_end - timedelta(days=7)
    prev_week_meals = MealPlan.objects.filter(date__range=(prev_week_start, prev_week_end)).order_by('date', 'meal_type')

    # Get the next week's meal plan
    next_week_start = current_week_start + timedelta(days=7)
    next_week_end = current_week_end + timedelta(days=7)
    next_week_meals = MealPlan.objects.filter(date__range=(next_week_start, next_week_end)).order_by('date', 'meal_type')

    context = {
        'current_week_meals': current_week_meals,
        'prev_week_meals': prev_week_meals,
        'next_week_meals': next_week_meals
    }
    return render(request, 'meal_planner/index.html', context)

def add_meal(request):
    if request.method == 'POST':
        meal_name = request.POST['meal_name']
        meal_type = request.POST['meal_type']
        ingredients = request.POST['ingredients']
        instructions = request.POST['instructions']
        meal = Meal.objects.create(name=meal_name, meal_type=meal_type, ingredients=ingredients, instructions=instructions)
        meal.save()
        return redirect('meal_planner:meal_detail', meal_id=meal.id)
    else:
        return render(request, 'meal_planner/add_meal.html')

def edit_meal(request, meal_id):
    meal = get_object_or_404(Meal, pk=meal_id)

    if request.method == 'POST':
        meal.name = request.POST['meal_name']
        meal.meal_type = request.POST['meal_type']
        meal.ingredients = request.POST['ingredients']
        meal.instructions = request.POST['instructions']
        meal.save()
        return redirect('meal_planner:meal_detail', meal_id=meal.id)
    else:
        context = {'meal': meal}
        return render(request, 'meal_planner/edit_meal.html', context)

def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, pk=meal_id)
    meal.delete()
    return redirect('meal_planner:index')

def add_meal_plan(request, meal_type, date):
    if request.method == 'POST':
        meal_id = request.POST['meal_id']
        meal_plan = MealPlan.objects.create(date=date, meal_type=meal_type, meal_id=meal_id)
        meal_plan.save()
        return redirect('meal_planner:index')
    else:
        meals = Meal.objects.all()
        context = {
            'meal_type': meal_type,
            'date': date,
            'meals': meals
        }
        return render(request, 'meal_planner/add_meal_plan.html', context)

def signupuser(request):
    if request.method == 'GET':
        return render(request, "meal/signup.html", {"form": UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, "meal/signup.html", {"form": UserCreationForm, 'error': 'Username taken please choose another one.'})
        else:
            return render(request, "meal/signup.html", {"form": UserCreationForm, 'error': 'Passwords did not match'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'meal/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'meal/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')