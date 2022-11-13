from django.shortcuts import render
import copy

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    }
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество 1,
#     'ингредиент2': количество 2,
#   }
# }


def recipy_listing(request):
    context = {
        'all_recipies': DATA
    }
    return render(request, 'calculator/list.html', context)


def recipy_helper(request, recipy_name):
    servings = request.GET.get("servings")
    copy_data = copy.deepcopy(DATA)
    needed_recipy = copy_data.get(recipy_name)
    if servings is not None:
        servings = int(servings)
    else:
        servings = 1
    for ingredient, amount in needed_recipy.items():
        needed_recipy[ingredient] = servings * amount
    context = {
        'recipe': {
            recipy_name: needed_recipy
        }
    }
    return render(request, 'calculator/index.html', context)

