from django.db import connection
from django.shortcuts import render

# Create your views here.
from idep.models import IdepAnosIniciaisV1, IdepAnosFinaisV1
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd


class MetasAnosFinais(APIView):

    def get(self, request, codesc, format=None):
        query = IdepAnosFinaisV1.objects.filter(cod_esc=codesc)
        esc = pd.DataFrame(list(query.values()))
        listinha = []
        for index, row in esc.iterrows():
            didi = {}
            didi['cod_esc'] = row['cod_esc']
            didi['nse'] = row['nse']
            didi['icg'] = row['icg']
            didi['anos'] = [ano.split('_')[-1] for ano in list(row.index)[3:9]]
            try:
                didi['metas'] = [float(meta. replace(',', '.')) for meta in list(row[3:9].values)]
            except:
                didi['metas'] = 'Não há metas para essa escola'
            listinha.append(didi)
        return Response({'result': listinha})


class MetasAnosIniciais(APIView):

    def get(self, request, codesc, format=None):
        query = IdepAnosIniciaisV1.objects.filter(cod_esc=codesc)
        esc = pd.DataFrame(list(query.values()))
        listinha = []
        for index, row in esc.iterrows():
            didi = {}
            didi['cod_esc'] = row['cod_esc']
            didi['nse'] = row['nse']
            didi['icg'] = row['icg']
            didi['anos'] = [ano.split('_')[-1] for ano in list(row.index)[3:9]]
            try:
                didi['metas'] = [float(meta.replace(',', '.')) for meta in list(row[3:9].values)]
            except:
                didi['metas'] = 'Não há metas para essa escola'
            listinha.append(didi)
        return Response({'result': listinha})
