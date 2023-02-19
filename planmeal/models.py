from django.db import models

class Meal(models.Model):
    name = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=50)
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.name

class MealPlan(models.Model):
    date = models.DateField()
    meal_type = models.CharField(max_length=50)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} - {self.meal_type} - {self.meal.name}'