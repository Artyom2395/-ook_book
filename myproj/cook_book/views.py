from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Recipe, RecipeProduct

@transaction.atomic
def add_product_to_recipe(request):
    """
    Добавляет продукт к рецепту или обновляет его вес, если продукт уже присутствует в рецепте.

    Эта функция обрабатывает GET-запрос, принимая три параметра: recipe_id, product_id и weight.
    Она добавляет указанный продукт к рецепту с заданным ID или обновляет вес продукта, 
    если он уже присутствует в рецепте. В случае успешного добавления или обновления, функция
    возвращает JSON-ответ с подтверждением успеха операции.

    Параметры:
    request: HttpRequest
        Запрос от пользователя. Ожидается, что в GET-параметрах будут указаны recipe_id (ID рецепта),
        product_id (ID продукта) и weight (вес продукта в граммах).

    Возвращает:
    JsonResponse
        JSON-ответ с результатом операции. В случае успеха возвращает {'success': True, 'created': [True/False]}.
        Если параметры невалидны или отсутствуют, возвращает сообщение об ошибке с соответствующим HTTP-статусом.
    """
    
    recipe_id = request.GET.get('recipe_id')
    product_id = request.GET.get('product_id')
    weight = request.GET.get('weight')

    if not (recipe_id and product_id and weight):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        recipe = Recipe.objects.get(id=recipe_id)
        product = Product.objects.get(id=product_id)
        weight = int(weight)
    except (Recipe.DoesNotExist, Product.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    recipe_product, created = RecipeProduct.objects.update_or_create(
        recipe=recipe, product=product, defaults={'weight': weight})

    return JsonResponse({'success': True, 'created': created})

@transaction.atomic
def cook_recipe(request):
    """
    Увеличивает счетчик использования каждого продукта, входящего в состав указанного рецепта.

    При вызове этой функции для каждого продукта, используемого в рецепте, увеличивается значение 
    times_used, которое отражает, сколько раз продукт был использован в приготовлении блюд.

    Параметры:
    request: HttpRequest
        Запрос от пользователя. Ожидается, что в GET-параметрах будет указан recipe_id.

    Возвращает:
    JsonResponse
        JSON-ответ с результатом операции. В случае успеха возвращает {'success': True}.
        Если рецепт с указанным recipe_id не найден, возвращает сообщение об ошибке с HTTP-статусом 404.
    """
    
    recipe_id = request.GET.get('recipe_id')

    try:
        recipe = Recipe.objects.select_for_update().get(id=recipe_id)
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)

    
    recipe_products = RecipeProduct.objects.select_for_update().filter(recipe=recipe)
    
        
    for recipe_product in recipe_products:
        product = recipe_product.product
        product.times_used += 1
        product.save()

    return JsonResponse({'success': True})


def show_recipes_without_product(request):
    """
    Отображает страницу с рецептами, где указанный продукт отсутствует или присутствует в количестве менее 10 грамм.

    Функция принимает один GET-параметр (product_id) и возвращает HTML страницу, на которой отображена таблица.
    В таблице перечислены идентификаторы и названия всех рецептов, в которых продукт с данным product_id
    отсутствует или присутствует в количестве менее 10 грамм. Это позволяет пользователям идентифицировать
    рецепты, которые соответствуют определенным критериям относительно использования продукта.

    Параметры:
    request: HttpRequest
        Запрос от пользователя. Ожидается, что в GET-параметрах будет указан product_id - идентификатор продукта.

    Возвращает:
    HttpResponse
        HTML страницу с таблицей рецептов, соответствующих заданным критериям.
    """
    
    product_id = request.GET.get('product_id')
    
    # Получаем все рецепты, где продукт отсутствует или его вес меньше 10 грамм
    recipes = Recipe.objects.exclude(
        recipeproduct__product_id=product_id,
        recipeproduct__weight__gte=10
    )

    return render(request, 'cook_book/recipes_without_product.html', {'recipes': recipes})