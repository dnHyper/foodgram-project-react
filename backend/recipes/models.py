from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингридиентов для рецептов."""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        'Название ингридиента',
        max_length=150,
        unique=True,
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=150,
        validators=(
            MinValueValidator(1, 'Минимальная единица измерения'),
            MaxValueValidator(9999, 'Максимальная единица измерения')
        ),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тэгов рецептов."""
    name = models.CharField(
        'Тэг',
        max_length=150,
        unique=True
    )
    color = models.CharField(
        'Единица измерения',
        max_length=50,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'slug'),
                name='unique_tag',
            ),
        )

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель таблицы списка рецептов."""
    name = models.CharField(
        'Название рецепта',
        max_length=200,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
        null=True,
        blank=True
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ингридиенты',
        through='IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes',
    )
    text = models.TextField(
        'Описание рецепта',
        blank=True,
        null=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        blank=True,
        null=True,
        validators=(
            MinValueValidator(1, 'Минимальное время приготовления'),
            MaxValueValidator(240, 'Максимальное время приготовления')
        ),
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        'Дата публикации рецепта',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_recipes',
            ),
        )

    def display_tag(self):
        return ', '.join(tags.name for tags in self.tags.all()[:3])

    display_tag.short_description = 'Тэг'


class IngredientInRecipe(models.Model):
    """Модель количества необходимых продуктов."""
    recipe = models.ForeignKey(
        to=Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        verbose_name='Ингридиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        'Количество ингридиентов',
        default=1,
        validators=(
            MinValueValidator(0, 'Минимум'),
        )
    )

    class Meta:
        ordering = ('ingredient',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.ingredient.name} {self.recipe.name}'


class Favorite(models.Model):
    """Модель избранных рецептов."""
    author = models.ForeignKey(
        User,
        verbose_name='Подписался',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='favorite',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'recipe'),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        return f'{self.author.username}: {self.recipe.name}'


class Cart(models.Model):
    """Модель корзины."""
    author = models.ForeignKey(
        User,
        verbose_name='Подписался',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='cart',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'recipe'),
                name='unique_cart',
            ),
        )

    def __str__(self):
        return f'{self.author.username}: {self.recipe.name}'
