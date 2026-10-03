"""Implementação do Trabalho 1 de IPI."""
from pathlib import Path
import csv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
ORIG, OUT, FIG = ROOT / "originais", ROOT / "resultados", ROOT / "material_relatorio"

def _validate_image(image):
    arr = np.asarray(image)
    if arr.ndim not in (2, 3): raise ValueError("A imagem deve ser 2D ou 3D (RGB).")
    return arr

def _repeat2(image):
    image = _validate_image(image)
    return np.repeat(np.repeat(image, 2, axis=0), 2, axis=1)

def TAM2(image, factor):
    """Repete cada linha e coluna; factor é uma potência de 2 maior que 2."""
    image = _validate_image(image)
    if not isinstance(factor, (int, np.integer)) or factor < 2 or factor % 2:
        raise ValueError("factor deve ser inteiro, par e maior ou igual a 2")
    if factor & (factor - 1): raise ValueError("factor deve ser potência de 2")
    result = image.copy()
    for _ in range(int(np.log2(factor))): result = _repeat2(result)
    return result

def TAMM(image):
    """Aumenta por 2 usando médias horizontais, verticais e diagonais."""
    image = _validate_image(image); h, w = image.shape[:2]
    out = np.empty((2*h, 2*w) + image.shape[2:], dtype=np.float64)
    for r in range(h):
        for c in range(w):
            p = image[r, c].astype(np.float64)
            right = image[r, c+1] if c+1 < w else image[r, c]
            down = image[r+1, c] if r+1 < h else image[r, c]
            diag = image[min(r+1, h-1), min(c+1, w-1)]
            out[2*r, 2*c], out[2*r, 2*c+1] = p, (p + right) / 2
            out[2*r+1, 2*c] = (p + down) / 2
            out[2*r+1, 2*c+1] = (p + right + down + diag) / 4
    if np.issubdtype(image.dtype, np.integer):
        # MATLAB arredonda .5 para cima; np.rint usa empate para o par.
        return np.floor(out + 0.5).clip(0, np.iinfo(image.dtype).max).astype(image.dtype)
    return out.astype(image.dtype)

def SUPERRES(image1, image2):
    """Põe image1 em linhas/colunas ímpares e image2 em pares."""
    a, b = _validate_image(image1), _validate_image(image2)
    if a.shape != b.shape: raise ValueError("imagens devem ter as mesmas dimensões")
    out = np.zeros((2*a.shape[0], 2*a.shape[1]) + a.shape[2:], dtype=np.result_type(a,b))
    out[0::2, 0::2], out[1::2, 1::2] = a, b
    return out

def gamma_transform(image, gamma):
    return np.rint(np.clip((np.asarray(image).astype(float)/255) ** gamma, 0, 1)*255).astype(np.uint8)

def histogram_cdf(image):
    hist = np.bincount(np.asarray(image).ravel(), minlength=256)
    return hist, np.cumsum(hist) / np.asarray(image).size

def equalize_histogram(image):
    image = np.asarray(image).astype(np.uint8); hist, cdf = histogram_cdf(image)
    nz = np.flatnonzero(hist)
    if len(nz) == 0: return image.copy()
    c0 = cdf[nz[0]]
    lut = np.rint(np.clip((cdf-c0)/(1-c0), 0, 1)*255).astype(np.uint8) if c0 < 1 else np.zeros(256, dtype=np.uint8)
    return lut[image]

def save_image(array, path): Image.fromarray(np.asarray(array)).save(path)

def test_functions():
    a = np.array([[10,12],[5,7]], dtype=np.uint8)
    assert np.array_equal(_repeat2(a), [[10,10,12,12],[10,10,12,12],[5,5,7,7],[5,5,7,7]])
    assert np.array_equal(TAM2(a, 2), _repeat2(a))
    assert TAM2(a, 8).shape == (16, 16)
    assert np.array_equal(TAMM(a), [[10,11,12,12],[8,9,10,10],[5,6,7,7],[5,6,7,7]])
    s = SUPERRES(a, a+1); assert s.shape == (4,4) and np.array_equal(s[0::2,0::2],a) and np.array_equal(s[1::2,1::2],a+1)

def run_experiments():
    test_functions(); (OUT/'q1').mkdir(parents=True, exist_ok=True); (OUT/'q2').mkdir(parents=True, exist_ok=True); FIG.mkdir(exist_ok=True)
    (OUT/'q1'/'README.txt').write_text('FRUIT1 e FRUIT2 não foram fornecidas; funções validadas com matrizes artificiais.\n', encoding='utf-8')
    a=np.array([[10,12],[5,7]],dtype=np.uint8)
    (OUT/'q1'/'testes_matrizes.txt').write_text('TAM2(a,2):\n'+str(TAM2(a,2))+'\n\nTAMM(a):\n'+str(TAMM(a))+'\n\nSUPERRES(a,a+1):\n'+str(SUPERRES(a,a+1))+'\n\nTAM2(a,8) dimensao: '+str(TAM2(a,8).shape)+'\n',encoding='utf-8')
    rows=[]
    for name in ['car','crowd','university']:
        image=np.array(Image.open(ORIG/f'{name}.png').convert('L')); save_image(image,OUT/'q2'/f'{name}_original.png')
        for gamma in [0.4,0.7,1.4,2.2]:
            result=gamma_transform(image,gamma); save_image(result,OUT/'q2'/f'{name}_gamma_{gamma:.1f}.png'); rows.append([name,gamma,float(result.mean()),float(result.std())])
        eq=equalize_histogram(image); save_image(eq,OUT/'q2'/f'{name}_equalizada.png')
        if name=='car':
            h0,c0=histogram_cdf(image); h1,c1=histogram_cdf(eq); fig,ax=plt.subplots(2,2,figsize=(10,7))
            for a,data,title in zip(ax.flat,[h0,h1,c0,c1],['histograma original','histograma equalizado','CDF original','CDF equalizada']): a.plot(data,color='black'); a.set_title('Car: '+title); a.set_xlim(0,255); a.grid(alpha=.2)
            fig.tight_layout(); fig.savefig(FIG/'car_histogramas_cdfs.png',dpi=180); plt.close(fig)
    with open(FIG/'metricas_gamma.csv','w',newline='',encoding='utf-8') as f: csv.writer(f).writerows([['imagem','gamma','media','desvio_padrao'],*rows])
    for name in ['car','crowd','university']:
        image=np.array(Image.open(ORIG/f'{name}.png').convert('L')); fig,ax=plt.subplots(1,3,figsize=(12,4))
        for a,img,title in zip(ax,[gamma_transform(image,.7),gamma_transform(image,1.4),equalize_histogram(image)],['gamma=0.7','gamma=1.4','equalização']): a.imshow(img,cmap='gray',vmin=0,vmax=255); a.set_title(title); a.axis('off')
        fig.suptitle(name); fig.tight_layout(); fig.savefig(FIG/f'{name}_comparacao.png',dpi=180); plt.close(fig)
    best={'car':.7,'crowd':.4,'university':.4}
    for name,gamma in best.items():
        image=np.array(Image.open(ORIG/f'{name}.png').convert('L'))
        save_image(gamma_transform(image,gamma), OUT/'q2'/f'{name}_melhor_gamma_{gamma:.1f}.png')

if __name__ == '__main__': run_experiments(); print('Experimentos concluídos com sucesso.')
