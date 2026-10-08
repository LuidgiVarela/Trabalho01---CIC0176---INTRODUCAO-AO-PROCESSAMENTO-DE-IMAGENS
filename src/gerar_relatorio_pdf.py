"""Gera uma versão PDF curta, em duas colunas, do relatório final."""
from pathlib import Path
import textwrap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.image import imread

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'material_relatorio'
PDF = FIG / 'relatorio_ieee.pdf'

def text_column(fig, text, x, y=0.92, width=48, fontsize=8.7, line=0.017):
    lines=[]
    for para in text.split('\n'):
        lines.extend(textwrap.wrap(para, width=width) or [''])
        lines.append('')
    for item in lines:
        fig.text(x, y, item, ha='left', va='top', fontsize=fontsize, family='serif')
        y -= line

def header(fig, section):
    fig.text(.5, .965, 'TRABALHO 1 — INTRODUÇÃO AO PROCESSAMENTO DE IMAGENS', ha='center', fontsize=12, weight='bold')
    fig.text(.5, .942, 'Luidgi Varela Carneiro — Matrícula 231011669', ha='center', fontsize=9)
    fig.text(.5, .022, f'Processamento Digital de Imagens — {section}', ha='center', fontsize=7, color='0.35')

def page_text(pdf, section, left, right):
    fig=plt.figure(figsize=(8.27,11.69)); header(fig, section)
    text_column(fig,left,.08,y=.90); text_column(fig,right,.53,y=.90)
    pdf.savefig(fig); plt.close(fig)

def page_figure(pdf, section, path, caption, left, right):
    fig=plt.figure(figsize=(8.27,11.69)); header(fig, section)
    ax=fig.add_axes((.08,.49,.84,.38)); ax.imshow(imread(path)); ax.axis('off')
    fig.text(.5,.46,caption,ha='center',va='top',fontsize=8,wrap=True)
    text_column(fig,left,.08,y=.40,width=48,fontsize=8.4,line=.016)
    text_column(fig,right,.53,y=.40,width=48,fontsize=8.4,line=.016)
    pdf.savefig(fig); plt.close(fig)

with PdfPages(PDF) as pdf:
    page_text(pdf,'Resumo e Introdução',
        '''RESUMO\nEste trabalho implementa TAM2, TAMM e SUPERRES para aumento e combinação de imagens. Na Questão 1 foram usadas duas fotografias próprias do mesmo carrinho, em perspectivas ligeiramente diferentes. Na Questão 2 foram comparadas correção power-law e equalização de histograma nas imagens car, crowd e university.\n\n1. INTRODUÇÃO\nO objetivo é estudar operações básicas de processamento digital de imagens e observar como diferentes estratégias alteram valores, suavidade e contraste. Na expansão por repetição, cada amostra ocupa um bloco de pixels. Na expansão por médias, as posições intermediárias são calculadas a partir dos vizinhos. A correção power-law usa s=r^gamma; gamma menor que um tende a clarear e gamma maior que um tende a escurecer. A equalização redistribui níveis por meio da CDF do histograma.''',
        '''A TAM2 evidencia o efeito de replicação de amostras. A TAMM produz transições mais contínuas, enquanto SUPERRES insere duas aquisições em posições alternadas. Como as fotos da Questão 1 não são perfeitamente alinhadas, a composição pode exibir artefatos; esses efeitos são parte da análise, não foram removidos por registro geométrico.\n\nO restante do relatório apresenta a metodologia, os resultados das duas questões e as conclusões obtidas a partir das imagens realmente processadas.''')
    page_figure(pdf,'Questão 1 — Métodos',FIG/'q1_comparacao.png','Figura 1. Fotografias próprias e resultados de TAM2, TAMM e SUPERRES.',
        '''2. METODOLOGIA\nAs fotografias RGB foram preservadas com 864×1536 pixels. TAM2 foi implementada por chamadas sucessivas ao aumento por dois e executada com fatores 2 e 8. TAMM escreve os pixels originais em posições alternadas e calcula médias horizontais, verticais e diagonais; nas bordas, usa a amostra disponível. SUPERRES escreve a primeira fotografia em linhas e colunas ímpares e a segunda em linhas e colunas pares, conforme a convenção do MATLAB.''',
        '''3. RESULTADOS — QUESTÃO 1\nTAM2 fator 2, TAMM e SUPERRES geraram 1728×3072 pixels. TAM2 fator 8 gerou 6912×12288 pixels. TAM2 preservou os valores, mas produziu blocos visíveis. TAMM suavizou as transições e reduziu a aparência de blocos. SUPERRES demonstrou a posição alternada dos pixels, porém a diferença de ponto de vista causou duplicações, deslocamentos e uma composição esparsa. Os artefatos são coerentes com a ausência de alinhamento entre as fotografias.''')
    page_figure(pdf,'Questão 2 — Realce',FIG/'crowd_comparacao.png','Figura 2. Comparação de gamma e equalização na imagem crowd.',
        '''Foram testados gamma 0.4, 0.7, 1.4 e 2.2 para cada imagem. Os arquivos individuais foram preservados em resultados/q2. Pela inspeção visual, foram destacados gamma 0.7 para car, 0.4 para crowd e 0.4 para university, por oferecerem melhor visibilidade entre as alternativas testadas.\n\nA equalização foi implementada usando o histograma acumulado, sem ocultar o algoritmo em uma função pronta.''',
        '''A correção gamma é adequada quando se deseja controlar o brilho global. Em cenas escuras, valores menores que um revelaram mais detalhes. A equalização ampliou o contraste global, mas também pode exagerar diferenças e ruído. Por isso, a melhor técnica depende da imagem: gamma oferece controle tonal direto; equalização é mais forte quando o histograma ocupa uma faixa estreita.''')
    page_figure(pdf,'Questão 2 — Histogramas, CDF e Conclusões',FIG/'car_histogramas_cdfs.png','Figura 3. Histogramas e CDF da imagem car antes e depois da equalização.',
        '''Na imagem car, a equalização redistribuiu os níveis de cinza e tornou a CDF mais espalhada no intervalo disponível. As três imagens foram equalizadas e os quatro valores de gamma foram executados, permitindo comparar tanto aparência quanto média e desvio-padrão em metricas_gamma.csv.\n\n4. CONCLUSÕES\nOs testes numéricos confirmaram a repetição da TAM2, as médias da TAMM e o posicionamento de SUPERRES.''',
        '''Na Questão 1, TAM2 foi a alternativa mais simples, TAMM apresentou aparência mais contínua e SUPERRES evidenciou a sensibilidade a diferenças de perspectiva. Na Questão 2, gamma permitiu ajustes controlados de brilho, enquanto a equalização produziu maior alteração de contraste. Todas as conclusões foram baseadas nos resultados salvos durante a execução.\n\nOs arquivos fonte, imagens originais, resultados e figuras estão organizados no repositório.''')
print(f'PDF gerado em {PDF}')
