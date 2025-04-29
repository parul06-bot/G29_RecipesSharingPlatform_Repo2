# from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()  # Could be JSONField or ManyToManyField for more complexity
    instructions = models.TextField()
    cuisine = models.CharField(max_length=100, blank=True)
    meal_type = models.CharField(max_length=100, blank=True)  # e.g., Breakfast, Lunch
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('general', 'General'),
        ('recipe', 'Recipe'),
        ('suggestion', 'Suggestion')
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    rating = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_icon(self):
        icons = {
            'general': 'fa-comment',
            'recipe': 'fa-utensils',
            'suggestion': 'fa-lightbulb'
        }
        return icons.get(self.feedback_type, 'fa-comment')

    def __str__(self):
        return f"Feedback from {self.name} - Rating: {self.rating}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='in_wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} wishlisted {self.recipe.title}"