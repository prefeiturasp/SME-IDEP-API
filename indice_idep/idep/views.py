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
                didi['metas'] = [float(meta.replace(',', '.')) for meta in list(row[3:9].values)]
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


class HistogramaIndicesIDEPAnoInicial(APIView):

    def get(self, request, codesc, format=None):
        query = IdepAnosIniciaisV1.objects.all()
        esc = pd.DataFrame(list(query.values()))
        esc.set_index('cod_esc', inplace=True)

        sel_esc = esc[esc.index == codesc]
        sel_esc_nse = sel_esc.at[codesc, 'nse']
        sel_esc_icg = sel_esc.at[codesc, 'icg']
        sel_esc_indice = float(sel_esc.at[codesc, 'number_2018'].replace(',', '.'))

        esc_mesmo_parametros = esc[(esc['nse'] == sel_esc_nse) & (esc['icg'] == sel_esc_icg)]
        indices = [float(meta.replace(',', '.')) for meta in list(esc_mesmo_parametros['number_2018'])]

        return Response({'result': {'indices': indices, 'indice_da_escola': sel_esc_indice}})


class HistogramaIndicesIDEPAnoFinal(APIView):

    def get(self, request, codesc, format=None):
        query = IdepAnosFinaisV1.objects.all()
        esc = pd.DataFrame(list(query.values()))
        esc.set_index('cod_esc', inplace=True)

        sel_esc = esc[esc.index == codesc]
        sel_esc_nse = sel_esc.at[codesc, 'nse']
        sel_esc_icg = sel_esc.at[codesc, 'icg']
        sel_esc_indice = float(sel_esc.at[codesc, 'number_2018'].replace(',', '.'))

        esc_mesmo_parametros = esc[(esc['nse'] == sel_esc_nse) & (esc['icg'] == sel_esc_icg)]
        indices = [float(meta.replace(',', '.')) for meta in list(esc_mesmo_parametros['number_2018'])]

        return Response({'result': {'indices': indices, 'indice_da_escola': sel_esc_indice}})
