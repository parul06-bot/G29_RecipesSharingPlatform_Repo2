from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, JsonResponse
from .models import Recipe, Feedback, Like, Wishlist
from .forms import RecipeForm, UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count

# Create your views here.
def main_view(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request,'aboutus.html')

def breakfast_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(meal_type='Breakfast', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(meal_type='Breakfast')
    return render(request, 'breakfast.html', {'recipes': recipes})

def chinese_recipes_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(cuisine='Chinese', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(cuisine='Chinese')
    return render(request, 'chinese_recipes.html', {'recipes': recipes})

def chinese_view(request):
    return render(request,'chinese.html')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get user's liked recipes
    liked_recipes = Recipe.objects.filter(likes__user=request.user)
    # Get user's wishlist items using the correct field name
    wishlist_recipes = Recipe.objects.filter(in_wishlists__user=request.user)
    
    context = {
        'liked_recipes': liked_recipes,
        'wishlist_recipes': wishlist_recipes,
        'likes_count': liked_recipes.count(),
        'wishlist_count': wishlist_recipes.count(),
    }
    return render(request, 'dashboard.html', context)

def dinner_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(meal_type='Dinner', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(meal_type='Dinner')
    return render(request, 'dinner.html', {'recipes': recipes})

def edit_recipe_view(request):
    return render(request,'edit_recipe.html')

@login_required(login_url='login', redirect_field_name='next')
def feedback_view(request):
    # Create default recipes if none exist
    if Recipe.objects.count() == 0:
        # Create a default admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            email='admin@example.com',
            is_staff=True,
            is_superuser=True
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # Create default recipes
        default_recipes = [
            {
                'title': 'Butter Chicken',
                'description': 'A rich and creamy Indian curry dish made with tender chicken in a spiced tomato-based sauce.',
                'ingredients': '- 500g chicken\n- 2 cups tomato puree\n- 1 cup cream\n- Spices (garam masala, turmeric, etc.)',
                'instructions': '1. Marinate chicken\n2. Cook in tandoor or oven\n3. Prepare curry sauce\n4. Combine and simmer',
                'cuisine': 'Indian',
                'meal_type': 'Non-Veg'
            },
            {
                'title': 'Masala Dosa',
                'description': 'Crispy fermented crepe made from rice batter and black lentils, served with spiced potato filling.',
                'ingredients': '- Rice\n- Black lentils\n- Potatoes\n- Spices',
                'instructions': '1. Prepare batter\n2. Ferment overnight\n3. Make potato filling\n4. Cook dosa',
                'cuisine': 'Indian',
                'meal_type': 'Veg'
            },
            {
                'title': 'Paneer Tikka',
                'description': 'Grilled Indian cottage cheese cubes marinated in spiced yogurt.',
                'ingredients': '- Paneer\n- Yogurt\n- Bell peppers\n- Indian spices',
                'instructions': '1. Marinate paneer\n2. Thread onto skewers\n3. Grill until charred',
                'cuisine': 'Indian',
                'meal_type': 'Veg'
            },
            {
                'title': 'Biryani',
                'description': 'Fragrant rice dish cooked with aromatic spices and layered with meat or vegetables.',
                'ingredients': '- Basmati rice\n- Meat or vegetables\n- Saffron\n- Whole spices',
                'instructions': '1. Cook rice\n2. Prepare curry\n3. Layer and steam',
                'cuisine': 'Indian',
                'meal_type': 'Non-Veg'
            },
            {
                'title': 'Kung Pao Chicken',
                'description': 'Spicy stir-fried Chinese dish made with cubes of chicken, peanuts, vegetables, and chili peppers.',
                'ingredients': '- Chicken\n- Peanuts\n- Vegetables\n- Soy sauce',
                'instructions': '1. Cut chicken\n2. Prepare sauce\n3. Stir fry\n4. Combine ingredients',
                'cuisine': 'Chinese',
                'meal_type': 'Non-Veg'
            },
            {
                'title': 'Vegetable Spring Rolls',
                'description': 'Crispy rolls filled with mixed vegetables and glass noodles.',
                'ingredients': '- Spring roll wrappers\n- Mixed vegetables\n- Glass noodles\n- Soy sauce',
                'instructions': '1. Prepare filling\n2. Roll wrappers\n3. Deep fry until golden',
                'cuisine': 'Chinese',
                'meal_type': 'Veg'
            },
            {
                'title': 'Mapo Tofu',
                'description': 'Spicy Sichuan dish with soft tofu in a flavorful sauce.',
                'ingredients': '- Soft tofu\n- Ground pork\n- Sichuan peppercorns\n- Doubanjiang',
                'instructions': '1. Cook pork\n2. Add sauce\n3. Add tofu\n4. Simmer',
                'cuisine': 'Chinese',
                'meal_type': 'Non-Veg'
            },
            {
                'title': 'Beef Tacos',
                'description': 'Mexican street food consisting of corn tortillas filled with seasoned beef and toppings.',
                'ingredients': '- Tortillas\n- Ground beef\n- Lettuce\n- Cheese',
                'instructions': '1. Cook meat\n2. Prepare toppings\n3. Heat tortillas\n4. Assemble tacos',
                'cuisine': 'Mexican',
                'meal_type': 'Non-Veg'
            },
            {
                'title': 'Vegetarian Enchiladas',
                'description': 'Rolled tortillas filled with beans and vegetables, covered in chili pepper sauce.',
                'ingredients': '- Tortillas\n- Black beans\n- Mixed vegetables\n- Enchilada sauce',
                'instructions': '1. Prepare filling\n2. Roll tortillas\n3. Cover with sauce\n4. Bake',
                'cuisine': 'Mexican',
                'meal_type': 'Veg'
            },
            {
                'title': 'Guacamole',
                'description': 'Fresh avocado dip with lime, tomatoes, and onions.',
                'ingredients': '- Avocados\n- Lime\n- Tomatoes\n- Onions',
                'instructions': '1. Mash avocados\n2. Mix ingredients\n3. Season',
                'cuisine': 'Mexican',
                'meal_type': 'Veg'
            },
            {
                'title': 'Pepperoni Pizza',
                'description': 'Classic Italian pizza with tomatoes, mozzarella, and pepperoni.',
                'ingredients': '- Pizza dough\n- Tomatoes\n- Mozzarella\n- Pepperoni',
                'instructions': '1. Roll dough\n2. Add toppings\n3. Bake',
                'cuisine': 'Italian',
                'meal_type': 'Non-Veg'
            },
            {
                'title': 'Vegetarian Pasta Primavera',
                'description': 'Fresh pasta with seasonal vegetables in a light cream sauce.',
                'ingredients': '- Pasta\n- Mixed vegetables\n- Olive oil\n- Parmesan',
                'instructions': '1. Cook pasta\n2. Sauté vegetables\n3. Combine with sauce',
                'cuisine': 'Italian',
                'meal_type': 'Veg'
            }
        ]

        # Create recipes
        for recipe_data in default_recipes:
            Recipe.objects.create(created_by=admin_user, **recipe_data)

    # Get all recipes for the template
    recipes = Recipe.objects.all().order_by('cuisine', 'title')
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    # Print debug information
    print(f"Number of recipes found: {recipes.count()}")
    for recipe in recipes:
        print(f"Recipe: {recipe.title} - Cuisine: {recipe.cuisine}")
    
    context = {
        'recipes': recipes,
        'feedbacks': feedbacks
    }
    return render(request, 'feedback.html', context)

def indian_recipes_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(cuisine='Indian', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(cuisine='Indian')
    return render(request, 'indian_recipes.html', {'recipes': recipes})

def italian_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(cuisine='Italian', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(cuisine='Italian')
    return render(request, 'italian.html', {'recipes': recipes})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        next_url = request.POST.get('next')  # Get next URL from form
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                # Check if user has admin role if admin is selected
                if role == 'admin' and not user.is_staff:
                    messages.error(request, 'You do not have admin privileges.')
                    return render(request, 'login.html')
                
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                # Check for next parameter to redirect after login
                if next_url:
                    return redirect(next_url)
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    return render(request, 'login.html')

def lunch_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(meal_type='Lunch', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(meal_type='Lunch')
    return render(request, 'lunch.html', {'recipes': recipes})

def mexican_recipes_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(cuisine='Mexican', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(cuisine='Mexican')
    return render(request, 'mexican_recipes.html', {'recipes': recipes})

def pastry_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(cuisine='Pastry', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(cuisine='Pastry')
    return render(request, 'pastry.html', {'recipes': recipes})

def ramen_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(cuisine='Japanese', meal_type='Ramen', is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.filter(cuisine='Japanese', meal_type='Ramen')
    return render(request, 'ramen.html', {'recipes': recipes})

def register_view(request):
   if request.user.is_authenticated:
        return redirect('index')
   if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if not all([name, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=name).exists():
            messages.error(request, 'This name is already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already in use.')
        else:
            # Create the user
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password
            )
            messages.success(request, f'Account created successfully! Please login to continue.')
            return redirect('login')
   return render(request,'register.html')

def search_results_view(request):
    return render(request,'search_results.html')

@login_required(login_url='login', redirect_field_name='next')
def share_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            messages.success(request, 'Your recipe has been shared successfully!')
            return redirect('view_recipes')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = RecipeForm()
    return render(request, 'share_recipe.html', {'form': form})

def view_recipes_view(request):
    # For regular users, only show published recipes
    if not request.user.is_staff:
        recipes = Recipe.objects.filter(is_published=True)
    else:
        # For staff/admin, show all recipes
        recipes = Recipe.objects.all()
    
    filter_type = request.GET.get('filter')
    liked_recipes = []
    wishlist_recipes = []
    
    if request.user.is_authenticated:
        # Get IDs of recipes liked by the user
        liked_recipes = list(Like.objects.filter(user=request.user).values_list('recipe_id', flat=True))
        # Get IDs of recipes in user's wishlist
        wishlist_recipes = list(Wishlist.objects.filter(user=request.user).values_list('recipe_id', flat=True))
        
        # Apply filters if requested
        if filter_type == 'liked':
            recipes = recipes.filter(likes__user=request.user)
        elif filter_type == 'wishlist':
            recipes = recipes.filter(in_wishlists__user=request.user)
    
    context = {
        'recipes': recipes,
        'liked_recipes': liked_recipes,
        'wishlist_recipes': wishlist_recipes,
        'filter_type': filter_type
    }
    return render(request, 'view_recipes.html', context)


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if not (request.user == recipe.created_by or request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed to edit this recipe.")
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('manage_recipes')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'admin/edit_recipe.html', {'form': form, 'recipe': recipe})

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if not (request.user == recipe.created_by or request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed to delete this recipe.")
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('view_recipes')
    return render(request, 'recipe_delete.html', {'recipe': recipe})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    storage = messages.get_messages(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

@login_required
@require_POST
def submit_feedback(request):
    try:
        print("Received feedback submission")  # Debug log
        
        # Get form data
        name = request.POST.get('name', request.user.username)
        email = request.POST.get('email', request.user.email)
        message = request.POST.get('message')
        rating = request.POST.get('rating')
        cuisine = request.POST.get('recipe')
        feedback_type = request.POST.get('feedback_type')
        
        print(f"Form data: name={name}, email={email}, rating={rating}, cuisine={cuisine}, type={feedback_type}")  # Debug log
        
        # Validate required fields
        if not all([message, rating, cuisine, feedback_type]):
            missing = []
            if not message: missing.append('message')
            if not rating: missing.append('rating')
            if not cuisine: missing.append('cuisine')
            if not feedback_type: missing.append('feedback type')
            return JsonResponse({
                'success': False,
                'message': f'Please fill in all required fields: {", ".join(missing)}'
            })
        
        try:
            # Get or create a recipe for the cuisine
            recipe, created = Recipe.objects.get_or_create(
                cuisine=cuisine,
                defaults={
                    'title': f'{cuisine.title()} Cuisine',
                    'created_by': request.user,
                    'description': 'General cuisine feedback',
                    'ingredients': 'N/A',
                    'instructions': 'N/A',
                    'meal_type': 'General'
                }
            )
            print(f"Recipe {'created' if created else 'found'}: {recipe}")  # Debug log
            
            # Create feedback
            feedback = Feedback.objects.create(
                name=name,
                email=email,
                message=message,
                rating=int(rating),
                recipe=recipe,
                feedback_type=feedback_type
            )
            print(f"Feedback created: {feedback}")  # Debug log
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your feedback!'
            })
            
        except Exception as e:
            print(f"Error creating feedback: {str(e)}")  # Debug log
            return JsonResponse({
                'success': False,
                'message': f'Error saving feedback: {str(e)}'
            })
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug log
        return JsonResponse({
            'success': False,
            'message': 'An unexpected error occurred. Please try again.'
        })

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_recipes = Recipe.objects.count()
    total_feedback = Feedback.objects.count()
    recent_recipes = Recipe.objects.order_by('-created_at')[:5]
    recent_feedback = Feedback.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_recipes': total_recipes,
        'total_feedback': total_feedback,
        'recent_recipes': recent_recipes,
        'recent_feedback': recent_feedback
    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'admin/manage_users.html', context)

@user_passes_test(is_admin)
def manage_recipes(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    context = {
        'recipes': recipes
    }
    return render(request, 'admin/manage_recipes.html', context)

@user_passes_test(is_admin)
def manage_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'admin/manage_feedback.html', context)

@user_passes_test(is_admin)
def view_user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_recipes = Recipe.objects.filter(created_by=user).order_by('-created_at')
    user_feedback = Feedback.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'user': user,
        'user_recipes': user_recipes,
        'user_feedback': user_feedback
    }
    return render(request, 'admin/user_details.html', context)

@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.username} has been {status}.')
    else:
        messages.error(request, 'Cannot modify superuser status.')
    return redirect('manage_users')

@user_passes_test(is_admin)
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    messages.success(request, 'Feedback has been deleted.')
    return redirect('manage_feedback')

@user_passes_test(is_admin)
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    messages.success(request, 'Recipe has been deleted.')
    return redirect('manage_recipes')

@user_passes_test(lambda u: u.is_staff)
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            messages.success(request, 'Recipe added successfully!')
            return redirect('manage_recipes')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm()
    
    return render(request, 'admin/add_recipe.html', {'form': form})

@user_passes_test(is_admin)
def toggle_recipe_status(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.is_published = not recipe.is_published
    recipe.save()
    status = 'published' if recipe.is_published else 'unpublished'
    messages.success(request, f'Recipe "{recipe.title}" has been {status}.')
    return redirect('manage_recipes')

@login_required
def toggle_like(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    like, created = Like.objects.get_or_create(user=request.user, recipe=recipe)
    
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True
    
    return JsonResponse({
        'is_liked': is_liked,
        'likes_count': recipe.likes.count()
    })

@login_required
def toggle_wishlist(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, recipe=recipe)
    
    if not created:
        wishlist_item.delete()
        is_wishlisted = False
    else:
        is_wishlisted = True
    
    return JsonResponse({
        'is_wishlisted': is_wishlisted,
        'wishlist_count': recipe.in_wishlists.count()
    })

@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('manage_users')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('manage_users')
        
        try:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Set role-based permissions
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            elif role == 'staff':
                user.is_staff = True
            
            user.save()
            messages.success(request, f'User {username} has been created successfully!')
            return redirect('manage_users')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return redirect('manage_users')
    
    return redirect('manage_users') 