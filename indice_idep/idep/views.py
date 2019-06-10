# Create your views here.
import pandas as pd
from escolas.models import Escolas
from idep.models import IdepAnosIniciaisV1, IdepAnosFinaisV1, IdepAnosIniciaisMetasEscolas, \
    IdepAnosIniciaisIndiceEscolas, IdepAnosIniciaisParametrosEscolas, IdepAnosFinaisMetasEscolas, \
    IdepAnosFinaisIndiceEscolas, IdepAnosFinaisParametrosEscolas
from rest_framework.response import Response
from rest_framework.views import APIView


def eol_cod_norm(cod_esc):
    tamanho = len(str(cod_esc))
    tamanho_faltante = 6 - tamanho
    return tamanho_faltante * '0' + str(cod_esc)


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
        codesc_mesmo_indice = list(esc_mesmo_parametros.index)

        try:
            escolas = Escolas.objects.filter(codesc__in=codesc_mesmo_indice)
            escolas_df = pd.DataFrame(list(escolas.values()))
            dres_count = escolas_df['dre'].value_counts()
            dres_count = dres_count.to_frame()

            lista_esc = list()
            for index, row in dres_count.iterrows():
                lista_esc.append((index, row['dre']))
        except:
            lista_esc = list()

        return Response({'result': {'indices': indices, 'indice_da_escola': sel_esc_indice,
                                    'dre_count': lista_esc}})


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

        try:
            escolas = Escolas.objects.filter(codesc__in=codesc_mesmo_indice)
            escolas_df = pd.DataFrame(list(escolas.values()))
            dres_count = escolas_df['dre'].value_counts()
            dres_count = dres_count.to_frame()

            lista_esc = list()
            for index, row in dres_count.iterrows():
                lista_esc.append((index, row['dre']))
        except:
            lista_esc = list()

        return Response({'result': {'indices': indices, 'indice_da_escola': sel_esc_indice,
                                    'dre_count': lista_esc}})


####################### Beta Functions


class BarChartView(APIView):

    def get(self, request, codesc, format=None):
        """
        Função que retorna informações do indice e Meta dos Anos Iniciais
        da escola selecionada
        :param request: Requisição da chamada da função
        :param codesc: Parametro da URL contendo o codigo da escola
        :return: JSON com informações do indice e das metas da escola selecionada
        """

        query_metas_inicial = IdepAnosIniciaisMetasEscolas.objects.filter(cod_esc=codesc)
        query_indices_inicial = IdepAnosIniciaisIndiceEscolas.objects.filter(cod_esc=codesc)
        query_parametros_inicial = IdepAnosIniciaisParametrosEscolas.objects.filter(cod_esc=int(codesc))

        esc_metas_inicial = pd.DataFrame(list(query_metas_inicial.values()))
        esc_indices_inicial = pd.DataFrame(list(query_indices_inicial.values()))
        esc_parametros_inicial = pd.DataFrame(list(query_parametros_inicial.values()))

        query_metas_final = IdepAnosFinaisMetasEscolas.objects.filter(cod_esc=codesc)
        query_indices_final = IdepAnosFinaisIndiceEscolas.objects.filter(cod_esc=codesc)
        query_parametros_final = IdepAnosFinaisParametrosEscolas.objects.filter(cod_esc=int(codesc))

        esc_metas_final = pd.DataFrame(list(query_metas_final.values()))
        esc_indices_final = pd.DataFrame(list(query_indices_final.values()))
        esc_parametros_final = pd.DataFrame(list(query_parametros_final.values()))

        if len(esc_metas_inicial) == 0 or len(esc_indices_inicial) == 0 or len(esc_parametros_inicial) == 0:
            return Response({'result': {'erro': 'nenhuma escola encontrada'}})

        # Ano Inicial
        metas_inicial = {}
        for index, row in esc_metas_inicial.iterrows():
            cod_esc_str = row['cod_esc']

            metas_inicial['anos'] = [ano.split('_')[-1] for ano in list(row.index)[3:]]
            try:
                metas_inicial['metas'] = [float(meta.replace(',', '.')) for meta in list(row[3:].values)]
            except:
                metas_inicial['metas'] = 'Não há metas para essa escola'

        indices_inicial = {}
        for index, row in esc_indices_inicial.iterrows():
            indices_inicial['anos'] = [ano.split('_')[-1] for ano in list(row.index)[3:]]
            try:
                indices_inicial['indices'] = [float(meta.replace(',', '.')) for meta in list(row[3:].values)]
            except:
                indices_inicial['indices'] = 'Não há metas para essa escola'

        parametros_inicial = {}
        for index, row in esc_parametros_inicial.iterrows():
            parametros_inicial['nse'] = row['nse']
            parametros_inicial['icg'] = row['icg']

        # Ano Final

        metas_finais = {}
        for index, row in esc_metas_final.iterrows():
            cod_esc_str = row['cod_esc']

            metas_finais['anos'] = [ano.split('_')[-1] for ano in list(row.index)[3:]]
            try:
                metas_finais['metas'] = [float(meta.replace(',', '.')) for meta in list(row[3:].values)]
            except:
                metas_finais['metas'] = 'Não há metas para essa escola'

        indices_finais = {}
        for index, row in esc_indices_final.iterrows():
            indices_finais['anos'] = [ano.split('_')[-1] for ano in list(row.index)[2:]]
            try:
                indices_finais['indices'] = [float(meta.replace(',', '.')) for meta in list(row[2:].values)]
            except:
                indices_finais['indices'] = 'Não há metas para essa escola'

        parametros_finais = {}
        for index, row in esc_parametros_final.iterrows():
            parametros_finais['nse'] = row['nse']
            parametros_finais['icg'] = row['icg']

        return Response(
            {'result': {'cod_esc': cod_esc_str,
                        'ano_inicial': {'metas': metas_inicial, 'indices': indices_inicial,
                                        'parametros': parametros_inicial},

                        'ano_final': {'metas': metas_finais, 'indices': indices_finais,
                                      'parametros': parametros_finais}}})


class HistogramaIndicesIDEPAnoInicialV2(APIView):

    def get(self, request, codesc, format=None):
        """
        Função que retorna os indices dos Anos Iniciais de todas as escolas
        com os mesmos parametros da escola selecionada
        :param request:Requisição da chamada da função
        :param codesc:Parametro da URL contendo o codigo da escola
        :return: JSON com os indices das outras escolas de mesmo perfil
        e da escola selecionada
        """
        query_indices_inicial = IdepAnosIniciaisIndiceEscolas.objects.all()
        query_parametros_inicial = IdepAnosIniciaisParametrosEscolas.objects.all()

        esc_indices_inicial = pd.DataFrame(list(query_indices_inicial.values()))
        esc_parametros_inicial = pd.DataFrame(list(query_parametros_inicial.values()))

        esc_indices_inicial.set_index('cod_esc', inplace=True)
        esc_parametros_inicial.set_index('cod_esc', inplace=True)

        sel_esc_indices_inicial = esc_indices_inicial[esc_indices_inicial.index == codesc]
        sel_esc_parametros_inicial = esc_parametros_inicial[esc_parametros_inicial.index == str(int(codesc))]

        if len(sel_esc_indices_inicial) == 0 or len(sel_esc_parametros_inicial) == 0:
            return Response({'result': {'erro': 'nenhuma escola encontrada'}})

        sel_esc_nse = sel_esc_parametros_inicial.at[str(int(codesc)), 'nse']
        sel_esc_icg = sel_esc_parametros_inicial.at[str(int(codesc)), 'icg']
        sel_esc_indice = float(sel_esc_indices_inicial.at[codesc, 'idep_2018'].replace(',', '.'))

        esc_mesmo_parametros = esc_parametros_inicial[
            (esc_parametros_inicial['nse'] == sel_esc_nse) & (esc_parametros_inicial['icg'] == sel_esc_icg)]

        codesc_mesmo_indice = [eol_cod_norm(cod) for cod in list(esc_mesmo_parametros.index)]
        esc_indice_mesmo_parametro = esc_indices_inicial[esc_indices_inicial.index.isin(codesc_mesmo_indice)]

        indices = [float(meta.replace(',', '.')) for meta in list(esc_indice_mesmo_parametro['idep_2018']) if
                   meta != '#VALOR!']
        try:
            escolas = Escolas.objects.filter(codesc__in=codesc_mesmo_indice)
            escolas_df = pd.DataFrame(list(escolas.values()))
            dres_count = escolas_df['dre'].value_counts()
            dres_count = dres_count.to_frame()

            lista_esc = list()
            for index, row in dres_count.iterrows():
                lista_esc.append((index, row['dre']))
        except:
            lista_esc = list()

        return Response({'result': {'indices': indices, 'indice_da_escola': sel_esc_indice,
                                    'dre_count': lista_esc}})


class HistogramaIndicesIDEPAnoFinalV2(APIView):

    def get(self, request, codesc, format=None):
        """
        Função que retorna os indices dos Anos Finais de todas as escolas
        com os mesmos parametros da escola selecionada
        :param request:Requisição da chamada da função
        :param codesc:Parametro da URL contendo o codigo da escola
        :return: JSON com os indices das outras escolas de mesmo perfil
        e da escola selecionada
        """
        query_indices_final = IdepAnosFinaisIndiceEscolas.objects.all()
        query_parametros_final = IdepAnosFinaisParametrosEscolas.objects.all()

        esc_indices_final = pd.DataFrame(list(query_indices_final.values()))
        esc_parametros_final = pd.DataFrame(list(query_parametros_final.values()))

        esc_indices_final.set_index('cod_esc', inplace=True)
        esc_parametros_final.set_index('cod_esc', inplace=True)

        sel_esc_indices_final = esc_indices_final[esc_indices_final.index == codesc]
        sel_esc_parametros_final = esc_parametros_final[esc_parametros_final.index == str(int(codesc))]

        if len(sel_esc_indices_final) == 0 or len(sel_esc_parametros_final) == 0:
            return Response({'result': {'erro': 'nenhuma escola encontrada'}})

        sel_esc_nse = sel_esc_parametros_final.at[str(int(codesc)), 'nse']
        sel_esc_icg = sel_esc_parametros_final.at[str(int(codesc)), 'icg']
        sel_esc_indice = float(sel_esc_indices_final.at[codesc, 'idep_2018'].replace(',', '.'))

        esc_mesmo_parametros = esc_parametros_final[
            (esc_parametros_final['nse'] == sel_esc_nse) & (esc_parametros_final['icg'] == sel_esc_icg)]

        codesc_mesmo_indice = [eol_cod_norm(cod) for cod in list(esc_mesmo_parametros.index)]
        esc_indice_mesmo_parametro = esc_indices_final[esc_indices_final.index.isin(codesc_mesmo_indice)]

        indices = [float(meta.replace(',', '.')) for meta in list(esc_indice_mesmo_parametro['idep_2018']) if
                   meta != '#VALOR!']
        try:
            escolas = Escolas.objects.filter(codesc__in=codesc_mesmo_indice)
            escolas_df = pd.DataFrame(list(escolas.values()))
            dres_count = escolas_df['dre'].value_counts()
            dres_count = dres_count.to_frame()

            lista_esc = list()
            for index, row in dres_count.iterrows():
                lista_esc.append((index, row['dre']))
        except:
            lista_esc = list()

        return Response({'result': {'indices': indices, 'indice_da_escola': sel_esc_indice,
                                    'dre_count': lista_esc}})
