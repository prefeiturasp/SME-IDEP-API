from django.db import models


# # Create your models here.
class IdepAnosFinaisV1(models.Model):
    cod_esc = models.TextField(primary_key=True)
    nse = models.IntegerField(blank=True, null=True)
    icg = models.IntegerField(blank=True, null=True)
    number_2018 = models.TextField(db_column='2018', blank=True, null=True)
    number_2019 = models.TextField(db_column='2019', blank=True, null=True)
    number_2020 = models.TextField(db_column='2020', blank=True, null=True)
    number_2021 = models.TextField(db_column='2021', blank=True, null=True)
    number_2022 = models.TextField(db_column='2022', blank=True, null=True)
    number_2023 = models.TextField(db_column='2023', blank=True, null=True)


class IdepAnosIniciaisV1(models.Model):
    cod_esc = models.TextField(primary_key=True)
    nse = models.IntegerField(blank=True, null=True)
    icg = models.IntegerField(blank=True, null=True)
    number_2018 = models.TextField(db_column='2018', blank=True, null=True)
    number_2019 = models.TextField(db_column='2019', blank=True, null=True)
    number_2020 = models.TextField(db_column='2020', blank=True, null=True)
    number_2021 = models.TextField(db_column='2021', blank=True, null=True)
    number_2022 = models.TextField(db_column='2022', blank=True, null=True)
    number_2023 = models.TextField(db_column='2023', blank=True, null=True)


class IdepAnosIniciaisIndiceEscolas(models.Model):
    cod_esc = models.TextField(blank=True, null=True)
    cod_mec = models.TextField(blank=True, null=True)
    idep_2018 = models.TextField(blank=True, null=True)


class IdepAnosIniciaisMetasEscolas(models.Model):
    cod_esc = models.TextField(blank=True, null=True)
    cod_mec = models.TextField(blank=True, null=True)
    idep_2019 = models.TextField(blank=True, null=True)
    idep_2020 = models.TextField(blank=True, null=True)
    idep_2021 = models.TextField(blank=True, null=True)
    idep_2022 = models.TextField(blank=True, null=True)
    idep_2023 = models.TextField(blank=True, null=True)
    idep_2038 = models.TextField(blank=True, null=True)
