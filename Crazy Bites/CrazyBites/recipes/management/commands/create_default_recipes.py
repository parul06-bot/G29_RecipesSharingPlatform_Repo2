from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Creates default recipes for the application'

    def handle(self, *args, **kwargs):
        # Create admin user if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            email='admin@example.com',
            is_staff=True,
            is_superuser=True
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exists'))

        # Delete existing recipes
        Recipe.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted existing recipes'))

        # Create default recipes
        default_recipes = [
            {
                'title': 'Butter Chicken',
                'description': 'A rich and creamy Indian curry dish made with tender chicken in a spiced tomato-based sauce.',
                'ingredients': '- 500g chicken\n- 2 cups tomato puree\n- 1 cup cream\n- Spices (garam masala, turmeric, etc.)',
                'instructions': '1. Marinate chicken\n2. Cook in tandoor or oven\n3. Prepare curry sauce\n4. Combine and simmer',
                'cuisine': 'Indian',
                'meal_type': 'Dinner'
            },
            {
                'title': 'Masala Dosa',
                'description': 'Crispy fermented crepe made from rice batter and black lentils, served with spiced potato filling.',
                'ingredients': '- Rice\n- Black lentils\n- Potatoes\n- Spices',
                'instructions': '1. Prepare batter\n2. Ferment overnight\n3. Make potato filling\n4. Cook dosa',
                'cuisine': 'Indian',
                'meal_type': 'Breakfast'
            },
            {
                'title': 'Biryani',
                'description': 'Fragrant rice dish cooked with aromatic spices and layered with meat or vegetables.',
                'ingredients': '- Basmati rice\n- Meat or vegetables\n- Saffron\n- Whole spices',
                'instructions': '1. Cook rice\n2. Prepare curry\n3. Layer and steam',
                'cuisine': 'Indian',
                'meal_type': 'Dinner'
            },
            {
                'title': 'Kung Pao Chicken',
                'description': 'Spicy stir-fried Chinese dish made with cubes of chicken, peanuts, vegetables, and chili peppers.',
                'ingredients': '- Chicken\n- Peanuts\n- Vegetables\n- Soy sauce',
                'instructions': '1. Cut chicken\n2. Prepare sauce\n3. Stir fry\n4. Combine ingredients',
                'cuisine': 'Chinese',
                'meal_type': 'Dinner'
            },
            {
                'title': 'Dim Sum',
                'description': 'Variety of small Chinese dumplings filled with meat or vegetables.',
                'ingredients': '- Dumpling wrappers\n- Ground pork\n- Shrimp\n- Vegetables',
                'instructions': '1. Prepare filling\n2. Wrap dumplings\n3. Steam',
                'cuisine': 'Chinese',
                'meal_type': 'Lunch'
            },
            {
                'title': 'Tacos',
                'description': 'Mexican street food consisting of corn tortillas filled with various meats and toppings.',
                'ingredients': '- Tortillas\n- Ground beef\n- Lettuce\n- Cheese',
                'instructions': '1. Cook meat\n2. Prepare toppings\n3. Heat tortillas\n4. Assemble tacos',
                'cuisine': 'Mexican',
                'meal_type': 'Lunch'
            },
            {
                'title': 'Enchiladas',
                'description': 'Rolled tortillas filled with meat and covered in chili pepper sauce.',
                'ingredients': '- Tortillas\n- Chicken\n- Enchilada sauce\n- Cheese',
                'instructions': '1. Prepare filling\n2. Roll tortillas\n3. Cover with sauce\n4. Bake',
                'cuisine': 'Mexican',
                'meal_type': 'Dinner'
            },
            {
                'title': 'Margherita Pizza',
                'description': 'Classic Italian pizza with tomatoes, mozzarella, and basil.',
                'ingredients': '- Pizza dough\n- Tomatoes\n- Mozzarella\n- Basil',
                'instructions': '1. Roll dough\n2. Add toppings\n3. Bake',
                'cuisine': 'Italian',
                'meal_type': 'Dinner'
            },
            {
                'title': 'Pasta Carbonara',
                'description': 'Creamy pasta dish with eggs, cheese, pancetta, and black pepper.',
                'ingredients': '- Spaghetti\n- Eggs\n- Pecorino Romano\n- Pancetta',
                'instructions': '1. Cook pasta\n2. Prepare sauce\n3. Combine',
                'cuisine': 'Italian',
                'meal_type': 'Dinner'
            }
        ]

        # Create recipes
        for recipe_data in default_recipes:
            Recipe.objects.create(created_by=admin_user, **recipe_data)
            self.stdout.write(self.style.SUCCESS(f'Created recipe: {recipe_data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(default_recipes)} recipes')) 