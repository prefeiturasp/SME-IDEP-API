FROM python:3.6

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/djangoapp/src

COPY Pipfile Pipfile.lock requirements.txt /opt/services/djangoapp/src/
WORKDIR /opt/services/djangoapp/src
RUN pip install pipenv && pipenv install --system && pip install -r requirements.txt

# Add requirements.txt to the image
# COPY requirements.txt /opt/services/djangoapp/src/requirements.txt
# RUN pip install -r requirements.txt

COPY . /opt/services/djangoapp/src/
#RUN ls -la indice_idep/indice_idep
RUN cd indice_idep && python manage.py collectstatic --no-input


EXPOSE 8000
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "indice_idep", "indice_idep.wsgi:application"]