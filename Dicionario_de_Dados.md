# Dicionário: Dataset Espectral NIR-SORT Pré-Processado

## 1. Visão Geral da Base de Dados

O conjunto de dados é oriundo de espectroscopia de refletância/absorbância difusa no infravermelho próximo (NIR), empregada na identificação e triagem automatizada de materiais têxteis pós-consumo para reciclagem circular.

Cada amostra consiste em um espectro de alta resolução amostrado entre os números de onda $4000{,}0\text{ cm}^{-1}$ e $8000{,}0\text{ cm}^{-1}$, submetido ao processo de **Spectral Binning** (agrupamento espectral em 16 bandas regulares de $250{,}0\text{ cm}^{-1}$) e normalizado para refletir a proporção relativa de absorção óptica.

---

## 2. Dicionário Consolidado de Atributos

| Nome da Variável | Tipo de Dado | Domínio | Unidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **`Fibra`** | Categórico (Nominal) | 6 classes textuais | Adimensional | **Variável-Alvo:** Tipo de fibra têxtil 100% pura da amostra. |
| **`Bin_01`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $4000{,}0\text{ a }4250{,}0\text{ cm}^{-1}$ ($2352{,}9\text{ a }2500{,}0\text{ nm}$). |
| **`Bin_02`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $4250{,}0\text{ a }4500{,}0\text{ cm}^{-1}$ ($2222{,}2\text{ a }2352{,}9\text{ nm}$). |
| **`Bin_03`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $4500{,}0\text{ a }4750{,}0\text{ cm}^{-1}$ ($2105{,}3\text{ a }2222{,}2\text{ nm}$). |
| **`Bin_04`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $4750{,}0\text{ a }5000{,}0\text{ cm}^{-1}$ ($2000{,}0\text{ a }2105{,}3\text{ nm}$). |
| **`Bin_05`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $5000{,}0\text{ a }5250{,}0\text{ cm}^{-1}$ ($1904{,}8\text{ a }2000{,}0\text{ nm}$). |
| **`Bin_06`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $5250{,}0\text{ a }5500{,}0\text{ cm}^{-1}$ ($1818{,}2\text{ a }1904{,}8\text{ nm}$). |
| **`Bin_07`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $5500{,}0\text{ a }5750{,}0\text{ cm}^{-1}$ ($1739{,}1\text{ a }1818{,}2\text{ nm}$). |
| **`Bin_08`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $5750{,}0\text{ a }6000{,}0\text{ cm}^{-1}$ ($1666{,}7\text{ a }1739{,}1\text{ nm}$). |
| **`Bin_09`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $6000{,}0\text{ a }6250{,}0\text{ cm}^{-1}$ ($1600{,}0\text{ a }1666{,}7\text{ nm}$). |
| **`Bin_10`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $6250{,}0\text{ a }6500{,}0\text{ cm}^{-1}$ ($1538{,}5\text{ a }1600{,}0\text{ nm}$). |
| **`Bin_11`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $6500{,}0\text{ a }6750{,}0\text{ cm}^{-1}$ ($1481{,}5\text{ a }1538{,}5\text{ nm}$). |
| **`Bin_12`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $6750{,}0\text{ a }7000{,}0\text{ cm}^{-1}$ ($1428{,}6\text{ a }1481{,}5\text{ nm}$). |
| **`Bin_13`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $7000{,}0\text{ a }7250{,}0\text{ cm}^{-1}$ ($1379{,}3\text{ a }1428{,}6\text{ nm}$). |
| **`Bin_14`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $7250{,}0\text{ a }7500{,}0\text{ cm}^{-1}$ ($1333{,}3\text{ a }1379{,}3\text{ nm}$). |
| **`Bin_15`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $7500{,}0\text{ a }7750{,}0\text{ cm}^{-1}$ ($1290{,}3\text{ a }1333{,}3\text{ nm}$). |
| **`Bin_16`** | Numérico Contínuo | $[0, 1]$ (Normalizado) | Absorbância relativa | Absorção óptica média no intervalo de $7750{,}0\text{ a }8000{,}0\text{ cm}^{-1}$ ($1250{,}0\text{ a }1290{,}3\text{ nm}$). |

---

## 3. Detalhamento da Variável-Alvo (`Fibra`)

A variável categórica `Fibra` representa as 6 classes de tecidos 100% puros catalogados no experimento:

| Classe (`Fibra`) | Código Original | Amostras ($N$) | Percentual ($\%$) | Natureza do Material |
| :--- | :---: | :---: | :---: | :--- |
| **Cotton** | `a` | 247 | 55,5% | Fibra natural de origem vegetal (algodão). |
| **Nylon** | `c` | 84 | 18,9% | Fibra sintética (poliamida). |
| **Polyester** | `b` | 51 | 11,5% | Fibra sintética (poliéster). |
| **Rayon** | `g` | 28 | 6,3% | Fibra artificial de base celulósica regenerada. |
| **Wool** | `i` | 28 | 6,3% | Fibra natural de origem animal (lã). |
| **Polyacrylic** | `d` | 7 | 1,6% | Fibra sintética (poliacrílico). |
| **Total** | — | **445** | **100,0%** | — |
