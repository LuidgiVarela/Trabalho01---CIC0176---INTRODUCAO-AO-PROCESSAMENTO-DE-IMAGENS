# Trabalho 1 — Introdução ao Processamento de Imagens

**Aluno:** Luidgi Varela Carneiro  
**Matrícula:** 231011669

Implementação em Python das funções `TAM2`, `TAMM` e `SUPERRES`, além dos
experimentos de correção gamma e equalização de histograma.

Na Questão 1 são usadas duas fotografias próprias do mesmo carrinho,
`originais/foto_carro_1.jpg` e `originais/foto_carro_2.jpg`, ambas RGB e com
864×1536 pixels. As fotos foram preservadas sem redimensionamento. Como foram
tiradas de perspectivas ligeiramente diferentes, a saída de `SUPERRES` pode
apresentar desalinhamentos e artefatos, mantidos para respeitar o algoritmo do
enunciado.

Dependências: Python 3, `numpy`, `Pillow` e `matplotlib`.

```powershell
python src/trabalho1.py
python src/gerar_relatorio_pdf.py
```

As imagens originais estão em `originais/`; os resultados individuais estão
em `resultados/`; e as figuras/métricas selecionadas para o relatório estão em
`material_relatorio/`.

O relatório em Markdown está em `material_relatorio/relatorio_trabalho1.md` e
o PDF em formato de duas colunas está em `material_relatorio/relatorio_ieee.pdf`.

O ZIP fornecido continha somente `car.png`, `crowd.png` e `university.png`.
`FRUIT1` e `FRUIT2`, exigidas para os resultados visuais da Questão 1, não
foram fornecidas. As funções foram implementadas e validadas com matrizes
artificiais; os resultados com essas duas frutas dependem do envio dos arquivos.
