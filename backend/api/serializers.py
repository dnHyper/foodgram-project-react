from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipes,
                            Tag)
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from users.models import User


class FavoriteSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    recipe = SlugRelatedField(
        slug_field='recipe',
        queryset=Recipes.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ('author', 'recipe')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = IngredientsSerializer()
    name = serializers.CharField(required=False)
    measurement_unit = serializers.IntegerField(required=False)
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "name", "amount", "measurement_unit")

    def to_representation(self, instance):
        data = IngredientsSerializer(instance.ingredient).data
        data["amount"] = instance.amount
        return data


class FavoritedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    author = UserSerializer(
        many=False,
        read_only=True
    )
    ingredients = IngredientWriteSerializer(
        source='ingredientinrecipe_set',
        many=True,
        read_only=True
    )
    tags = TagsSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, recipe):
        user = self.context["request"].user
        if (not user.is_authenticated or
                not recipe.favorite.filter(author=user).last()):
            return False
        return True

    def get_is_in_shopping_cart(self, recipe):
        user = self.context["request"].user
        if (not user.is_authenticated or
                not recipe.cart.filter(author=user).last()):
            return False
        return True

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
            )
        model = Recipes


class RecipesSerializerCreate(serializers.ModelSerializer):
    """Сериализатор создания рецептов."""
    author = UserSerializer(
        many=False,
        read_only=True
    )
    ingredients = IngredientWriteSerializer(
        source='ingredientinrecipe_set',
        many=True,
        read_only=True
    )
    image = Base64ImageField()

    class Meta:
        fields = (
            'author',
            'name',
            'ingredients',
            'image',
            'text',
            'tags',
            'cooking_time'
            )
        model = Recipes

    def validate_name(self, name):
        if not name[0].isupper():
            raise serializers.ValidationError(
                'Название рецепта не может начинаться с маленькой буквы.'
            )
        is_exist = Recipes.objects.filter(
            author=self.context['request'].user,
            name=name
        ).exists()
        if is_exist and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы уже сохраняли рецепт с таким названием')
        return name

    def validate_text(self, text):
        if not text[0].isupper():
            raise serializers.ValidationError(
                'Описание рецепта не может начинаться с маленькой буквы.'
            )
        if len(text) < 10:
            raise serializers.ValidationError(
                'Рецепт меньше 10 символов? Серьёзно? :-)'
            )
        return text

    def validate(self, data):
        ingredients_data = self.initial_data.get('ingredients')

        if not ingredients_data:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент'
            )

        ingredients_list = []
        for ingredient in ingredients_data:
            ingredient_id = ingredient['id']
            try:
                Ingredient.objects.get(pk=ingredient_id)
                int(ingredient['amount'])
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f'Не найден ингредиент с id={ingredient_id}'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'Поле количество можно заполнять только числами'
                )
            # Ошибка при передаче данных от JS-фронта — проверка не работает.
            # if ingredient['amount'] <= 0:
            #     raise serializers.ValidationError(
            #         'Укажите вес/количество ингридиентов'
            #     )
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'Игридиенты не должны повторяться.'
                )
            ingredients_list.append(ingredient_id)
        return data

    def create(self, validated_data):
        ingredients_data = self.initial_data.get('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        for ingredient in ingredients_data:
            IngredientInRecipe(
                recipe=recipe,
                ingredient=Ingredient(id=ingredient['id']),
                amount=ingredient['amount']
            ).save()
        recipe.tags.set(tags)
        return recipe


class ActionsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
            )
        model = Recipes
