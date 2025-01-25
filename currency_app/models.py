from django.db import models


class CurrencyExchange(models.Model):
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Amount',
        null=True,
        blank=True
    )

    from_currency = models.CharField(
        verbose_name='From Currency',
        blank=True
    )

    to_currency = models.CharField(
        verbose_name='To Currency',
        blank=True
    )

    converted = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Converted',
        blank=True
    )

    def __str__(self):
        return f"{self.amount} {self.from_currency} to {self.to_currency}"

    class Meta:
        verbose_name = "Currency Exchange"
        verbose_name_plural = "Currency Exchanges"


class CountryTimeModel(models.Model):
    country = models.TextField(
        blank=True,
        verbose_name='Continent/Country'
    )

    country_time = models.TextField(
        blank=True,
        verbose_name='CountryTime'
    )

    def __str__(self):
        return f"{self.country}, {self.country_time}"


class Game(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        default='Untitled',
        db_index=True
    )

    description = models.TextField(
        verbose_name='Description',
        default='No description',
        blank=True
    )

    genres = models.CharField(
        max_length=255,
        verbose_name='Genres',
        default='No genres',
        blank=True
    )

    release_time = models.CharField(
        max_length=50,
        verbose_name='Release Time',
        default='No release time',
        blank=True
    )

    image = models.URLField(
        verbose_name='Image',
        default='No image',
        blank=True
    )

    platforms = models.CharField(
        max_length=255,
        verbose_name='Platforms',
        default='No platforms',
        blank=True
    )

    developers = models.CharField(
        max_length=255,
        verbose_name='Developers',
        default='No developers',
        blank=True
    )
