from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Модель ингридиентов для рецептов."""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        "Название ингридиента",
        max_length=150,
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=50,
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
        "Тэг",
        max_length=150,
    )
    color = models.CharField(
        "Единица измерения",
        max_length=50,
    )
    slug = models.SlugField(
        "Слаг",
        max_length=50,
        unique=True,
    )


class Recipes(models.Model):
    """Модель таблицы списка рецептов."""
    name = models.CharField(
        "Название рецепта",
        max_length=200,
    )
    image = models.TextField(
        "Изображение",
        blank=True,
        null=True,
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name="Ингридиенты",
        through='IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Ингридиенты"
    )
    text = models.TextField(
        "Описание рецепта",
        blank=True,
        null=True,
    )
    cooking_time = models.IntegerField(
        "Время приготовления (в минутах)",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        "Дата публикации рецепта",
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientInRecipe(models.Model):
    """Модель количества необходимых продуктов."""
    recipe = models.ForeignKey(
        to=Recipes,
        verbose_name="Рецепт",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        verbose_name="Ингридиент",
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        "Количество ингридиентов",
        default=1,
    )

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


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
        verbose_name="Рецепт",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.author}: {self.recipe}"


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
        verbose_name="Рецепт",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.author}: {self.recipe}"
