FROM python:3.12

SHELL ["/bin/sh", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools
RUN adduser --disabled-password currencyuser

WORKDIR /currency

COPY --chown=currency:currency . .

RUN pip install -r requirements.txt

USER currencyuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]