# Trabalho 1 — Introdução ao Processamento de Imagens

**Aluno:** Luidgi Varela Carneiro — **Matrícula:** 231011669

## Resumo

Este trabalho implementa três operações de aumento e combinação de imagens:
repetição por fator dois (`TAM2`), interpolação por médias (`TAMM`) e inserção
de duas imagens em posições alternadas (`SUPERRES`). Também são comparados o
realce por correção power-law e a equalização de histograma nas imagens
`car.png`, `crowd.png` e `university.png`. Para a imagem do carro são
apresentados histogramas e funções de distribuição acumulada antes e depois
da equalização. Na Questão 1 são utilizadas duas fotografias próprias do
mesmo carrinho, obtidas de perspectivas ligeiramente diferentes.

## 1. Introdução

O objetivo é estudar operações básicas de processamento digital de imagens e
observar como diferentes estratégias alteram a distribuição e a aparência dos
níveis de cinza. Na expansão por repetição, cada amostra ocupa um bloco de
pixels, preservando valores mas produzindo bordas quadradas. Na expansão por
médias, as posições intermediárias são calculadas a partir dos vizinhos,
produzindo transições mais suaves. A correção power-law transforma cada nível
normalizado por `s = r^gamma`: valores de gamma menores que um tendem a
clarear a imagem, enquanto valores maiores que um tendem a escurecê-la. A
equalização usa a CDF do histograma para redistribuir os níveis e ampliar o
contraste global. A Seção 2 descreve a metodologia; a Seção 3 reúne os
resultados; e a Seção 4 apresenta as conclusões.

## 2. Metodologia

As funções da Questão 1 foram escritas com laços e indexação explícita. Em
`TAM2`, o fator é obtido por chamadas sucessivas ao aumento por dois; a
implementação aceita potências de dois, incluindo o fator oito solicitado.
`TAMM` mantém as amostras originais nas posições ímpares segundo a convenção
do MATLAB e calcula médias horizontais, verticais e de quatro vizinhos quando
existem; nas bordas, repete a amostra disponível. `SUPERRES` escreve a
primeira imagem nas posições linha/coluna ímpares e a segunda nas posições
pares. Matrizes artificiais verificam os valores do exemplo do enunciado.

Além dos testes artificiais, foram processadas duas fotografias RGB próprias
do mesmo objeto, ambas com 864×1536 pixels. As fotografias foram mantidas em
seus arquivos originais e não foram redimensionadas. A `SUPERRES` foi aplicada
diretamente, sem alinhamento geométrico adicional, para não alterar o
algoritmo solicitado.

Para a Questão 2, foram testados gamma `0.4`, `0.7`, `1.4` e `2.2` em cada
imagem. A equalização foi implementada pela CDF do histograma. Todas as
imagens geradas estão em `resultados/q2/`; as figuras selecionadas estão em
`material_relatorio/`.

## 3. Resultados

As dimensões originais são: `car` 600×338, `crowd` 800×600 e `university`
399×300. Os quatro resultados de gamma e o resultado equalizado de cada
imagem foram salvos individualmente. As comparações visuais estão em
`car_comparacao.png`, `crowd_comparacao.png` e `university_comparacao.png`.

Na Questão 1, `TAM2` fator 2, `TAMM` e `SUPERRES` produzem imagens de
1728×3072 pixels, enquanto `TAM2` fator 8 produz 6912×12288 pixels. A
repetição de `TAM2` preserva blocos de pixels e evidencia descontinuidades.
`TAMM` suaviza as transições com médias horizontal, vertical e diagonal. A
`SUPERRES` posiciona as duas fotos nas coordenadas especificadas, mas a
diferença de perspectiva provoca duplicação, deslocamento e padrões esparsos
visíveis na composição. Esses artefatos são esperados e não foram corrigidos
artificialmente. A figura `q1_comparacao.png` reúne os resultados principais.

Para cada imagem, gamma abaixo de um clareou a saída e gamma acima de um a
escureceu, como previsto pela transformação. As médias e desvios-padrão de
todas as saídas estão em `metricas_gamma.csv`, permitindo justificar a escolha
do melhor valor junto com a inspeção visual. Pela inspeção das quatro
alternativas, foram destacados como melhores compromissos de visibilidade os
valores gamma `0.7` para `car`, `0.4` para `crowd` e `0.4` para `university`;
as imagens correspondentes estão identificadas por `melhor_gamma`.
A equalização da imagem `car` é
documentada em `car_histogramas_cdfs.png`, que mostra a alteração da
distribuição e da CDF.

Em geral, a correção gamma é mais controlável quando o objetivo é clarear ou
escurecer uma cena, enquanto a equalização é apropriada quando se deseja
aumentar o contraste global. A escolha final depende da aparência desejada em
cada imagem e deve ser descrita com base nas figuras produzidas.

## 4. Conclusões

Os testes numéricos confirmaram o comportamento de repetição da `TAM2`, as
médias da `TAMM` e o posicionamento alternado da `SUPERRES`. A correção gamma
produziu mudanças previsíveis de brilho, enquanto a equalização alterou o
contraste com base no histograma.

As fotografias próprias permitiram concluir a Questão 1 visualmente. A
`TAM2` é simples e preserva os valores, mas produz blocos; `TAMM` fornece uma
aparência mais contínua; e `SUPERRES` demonstra a disposição dos pixels de
duas aquisições, embora seja sensível ao desalinhamento entre perspectivas.
