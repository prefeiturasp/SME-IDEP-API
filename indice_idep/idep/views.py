# Create your views here.
import pandas as pd
from idep.models import IdepAnosIniciaisV1, IdepAnosFinaisV1, IdepAnosIniciaisMetasEscolas, \
    IdepAnosIniciaisIndiceEscolas
from rest_framework.response import Response
from rest_framework.views import APIView


class MetasAnosFinais(APIView):

    def get(self, request, codesc, format=None):
        """
        Função que retorna informações do indice e Meta dos Anos Finais
        da escola selecionada
        :param request: Requisição da chamada da função
        :param codesc: Parametro da URL contendo o codigo da escola
        :return: JSON com informações do indice e das metas da escola selecionada
        """
        query = IdepAnosFinaisV1.objects.filter(cod_esc=codesc)
        esc = pd.DataFrame(list(query.values()))
        if len(esc) == 0:
            return Response({'result': {'erro': 'nenhuma escola encontrada'}})
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
        """
        Função que retorna informações do indice e Meta dos Anos Iniciais
        da escola selecionada
        :param request: Requisição da chamada da função
        :param codesc: Parametro da URL contendo o codigo da escola
        :return: JSON com informações do indice e das metas da escola selecionada
        """

        query = IdepAnosIniciaisV1.objects.filter(cod_esc=codesc)
        esc = pd.DataFrame(list(query.values()))
        if len(esc) == 0:
            return Response({'result': {'erro': 'nenhuma escola encontrada'}})
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


class HistogramaIndicesIDEPAnoFinal(APIView):

    def get(self, request, codesc, format=None):
        """
        Função que retorna os indices dos Anos Finais de todas as escolas
        com os mesmos parametros da escola selecionada
        :param request:Requisição da chamada da função
        :param codesc:Parametro da URL contendo o codigo da escola
        :return: JSON com os indices das outras escolas de mesmo perfil
        e da escola selecionada
        """
        query = IdepAnosFinaisV1.objects.all()
        esc = pd.DataFrame(list(query.values()))
        esc.set_index('cod_esc', inplace=True)

        sel_esc = esc[esc.index == codesc]
        if len(sel_esc) == 0:
            return Response({'result': {'erro': 'nenhuma escola encontrada'}})
        sel_esc_nse = sel_esc.at[codesc, 'nse']
        sel_esc_icg = sel_esc.at[codesc, 'icg']
        sel_esc_indice = float(sel_esc.at[codesc, 'number_2018'].replace(',', '.'))

        esc_mesmo_parametros = esc[(esc['nse'] == sel_esc_nse) & (esc['icg'] == sel_esc_icg)]
        indices = [float(meta.replace(',', '.')) for meta in list(esc_mesmo_parametros['number_2018'])]

        return Response({'result': {'indices': indices, 'indice_da_escola': sel_esc_indice}})


class HistogramaIndicesIDEPAnoInicial(APIView):

    def get(self, request, codesc, format=None):
        """
        Função que retorna os indices dos Anos Iniciais de todas as escolas
        com os mesmos parametros da escola selecionada
        :param request:Requisição da chamada da função
        :param codesc:Parametro da URL contendo o codigo da escola
        :return: JSON com os indices das outras escolas de mesmo perfil
        e da escola selecionada
        """
        query = IdepAnosIniciaisV1.objects.all()
        esc = pd.DataFrame(list(query.values()))
        esc.set_index('cod_esc', inplace=True)

        sel_esc = esc[esc.index == codesc]
        if len(sel_esc) == 0:
            return Response({'result': {'erro': 'nenhuma escola encontrada'}})
        sel_esc_nse = sel_esc.at[codesc, 'nse']
        sel_esc_icg = sel_esc.at[codesc, 'icg']
        sel_esc_indice = float(sel_esc.at[codesc, 'number_2018'].replace(',', '.'))

        esc_mesmo_parametros = esc[(esc['nse'] == sel_esc_nse) & (esc['icg'] == sel_esc_icg)]
        indices = [float(meta.replace(',', '.')) for meta in list(esc_mesmo_parametros['number_2018'])]
        codesc_mesmo_indice = list(esc_mesmo_parametros.index)

        return Response({'result': {'indices': indices, 'indice_da_escola': sel_esc_indice,
                                    'escolas_mesmo_indice': codesc_mesmo_indice}})

####################### Beta Functions
