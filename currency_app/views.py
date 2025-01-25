import os
from datetime import datetime
from urllib.parse import quote

import pytz
import requests
from django.conf import settings
from django.http import Http404, FileResponse
from django.shortcuts import render
from .forms import CurrencyExchangeForm, CountryTimeForm
from .models import CurrencyExchange, CountryTimeModel


def exchange(request):
    response = requests.get('https://v6.exchangerate-api.com/v6/82a28926bd74fb7522fcee99/latest/USD').json()
    currencies = response.get("conversion_rates", {})
    currency_choices = [(currency, currency) for currency in currencies.keys()]
    form = CurrencyExchangeForm()
    form.fields['from_currency'].choices = currency_choices
    form.fields['to_currency'].choices = currency_choices

    if request.method == "POST":
        form = CurrencyExchangeForm(request.POST)
        form.fields['from_currency'].choices = currency_choices
        form.fields['to_currency'].choices = currency_choices

        if form.is_valid():
            amount = float(form.cleaned_data['amount'])
            from_currency_rate = currencies.get(form.cleaned_data['from_currency'], 1)
            to_currency_rate = currencies.get(form.cleaned_data['to_currency'], 1)
            converted = round((to_currency_rate / from_currency_rate) * amount, 2)
            change = CurrencyExchange.objects.create(
                amount=amount,
                from_currency=from_currency_rate,
                to_currency=to_currency_rate,
                converted=converted)
            change.save()
            return render(request, 'currency/exchange.html', {
                'form': form,
                'converted': converted
            })

    return render(request, 'currency/exchange.html', {'form': form})


def country_time(request):
    form = CountryTimeForm()
    timezones = pytz.all_timezones

    if request.method == "POST":
        form = CountryTimeForm(request.POST)

        if form.is_valid():
            continent_country = form.cleaned_data['country']

            if continent_country in timezones:
                response = requests.get(
                    f"https://timeapi.io/api/time/current/zone?timeZone={quote(continent_country)}"
                ).json()

                current_time = response.get("dateTime")
                if current_time:
                    parsed_time = datetime.fromisoformat(current_time)
                    formatted_time = parsed_time.strftime("%d %B %Y, %H:%M:%S")
                    time_save = CountryTimeModel.objects.create(
                        country=continent_country,
                        country_time=formatted_time
                    )
                    time_save.save()

                    return render(request, 'currency/timezone.html', {
                        'form': form,
                        'current_time': formatted_time,
                    })

    return render(request, 'currency/timezone.html', {
        'form': form,
    })


def home(request):
    return render(request, 'currency/index.html')


def download_file(request, games_data):
    file_path = os.path.join(settings.MEDIA_ROOT, 'files', games_data)

    if os.path.exists(file_path):
        try:
            response = FileResponse(open(file_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(games_data)}"'
            return response
        except Exception as e:
            print(f"Error {e}")
            raise Http404(f"Error {e}")
    else:
        raise Http404(f"File not found: {file_path}")