import base64
import io
import urllib

import matplotlib.pyplot as plt
import matplotlib as mpl

from model import get_dados_sum


def map_coluna(label):
    return {
        'etnia': 'Etnia',
        'genero': 'Gênero',
        'escola_origem': 'Escola de Origem',
        'renda': 'Renda Familiar',
        'cidade': 'Cidade',
        'estado': 'Estado',
        'faixa_etaria': 'Faixa Etária',
        'matricula_situacao': 'Situação de Matrícula'
    }.get(label)


def get_formatted_label(label):
    if label.lower() in ['f', 'm']:
        if label.lower() == 'f':
            return 'Feminino'
        else:
            return 'Masculino'
    else:
        return label


def index(tipo):
    dados_sum = get_dados_sum(tipo=tipo)
    selected_coluna = map_coluna(label=tipo)
    labels = [get_formatted_label(dado[0]) for dado in dados_sum]
    data_sizes = [dado[1] for dado in dados_sum]
    total = 0
    for item in data_sizes:
        total += item

    porcentagem = []
    for item in data_sizes:
        porcentagem.append(round((item / total) * 100, 2))

    porcentagem_grafico = []
    label_grafico = []
    outros = 0
    for index, item in enumerate(porcentagem):
        if item < 5:
            outros += item
        else:
            label_grafico.append(labels[index])
            porcentagem_grafico.append(item)
    if outros > 0:
        porcentagem_grafico.append(outros)
        label_grafico.append('Outros')

    # Gráfico de pizza
    mpl.style.use('seaborn-v0_8-muted')
    sizes = porcentagem_grafico
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=label_grafico, autopct='%1.1f%%',
            # definir o angulo do gráfico
            shadow=False, startangle=90)
    ax1.axis('equal')

    # Converte para imagem
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    listas = []
    for i in range(len(labels)):
        listas.append({
            'label': labels[i],
            'contador': data_sizes[i],
            'porcentagem': porcentagem[i]
        })
    if len(labels) <= 4:

        context = {
            'data': uri,
            'len': True, 'label': labels,
            'column': selected_coluna,
            'contador': data_sizes, 'porcentagem': porcentagem,
            'listas': listas
        }
    else:
        context = {
            'data': uri, 'len': False,
            'label': labels, 'column': selected_coluna,
            'contador': data_sizes,
            'porcentagem': porcentagem, 'listas': listas}

    return context
