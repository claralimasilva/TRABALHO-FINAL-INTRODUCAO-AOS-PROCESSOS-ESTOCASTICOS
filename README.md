# Trabalho 1 — Modelo de Ising com MCMC

Simulação do modelo de Ising em grade 2D com algoritmo de Metropolis-Hastings, estimação da energia média por Monte Carlo e relatório em LaTeX.

**Disciplina:** Introdução aos Processos Estocásticos  

---

## Estrutura do projeto

```
.
├── trabalho.py          # Simulação MCMC e geração das figuras
├── relatorio.tex        # Relatório (fonte LaTeX)
├── relatorio.pdf        # Relatório compilado
├── requirements.txt     # Dependências Python
├── figuras/             # Figuras geradas pela simulação
│   ├── grade_T0_5.png
│   ├── grade_T2_0.png
│   └── energia_vs_T.png
└── README.md
```

---

## Requisitos

- Python 3.10+
- LaTeX (`pdflatex`) — apenas para compilar o relatório

---

## Instalação

```bash
cd "TRABALHO IPE"
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

---

## Executar a simulação

```bash
source .venv/bin/activate
python trabalho.py
```

O script:

1. Gera as grades de exemplo em **T = 0,5** e **T = 2,0**
2. Estima ⟨E⟩ para 20 temperaturas entre **0,1** e **1,9** (5 cadeias independentes por temperatura)
3. Salva as figuras em `figuras/`
4. Imprime o progresso no terminal (temperatura, cadeias e médias)

> **Atenção:** a simulação completa pode levar bastante tempo (vários minutos), principalmente na etapa de energia média após salvar as grades.

---

## Compilar o relatório

Após rodar a simulação (para atualizar as figuras):

```bash
pdflatex relatorio.tex
```

O PDF final será `relatorio.pdf` (máx. 6 páginas, fonte 12, espaçamento 1,5).

---

## Parâmetros principais

Editáveis no início de `trabalho.py`:

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| `N` | 40 | Tamanho da grade (n × n) |
| `K_B` | 1 | Constante de Boltzmann (β = 1/T) |
| `EQUIL_SWEEPS` | 2000 | Sweeps de equilíbrio |
| `PROD_SWEEPS` | 5000 | Sweeps de produção |
| `SAMPLE_INTERVAL` | 10 | Intervalo entre amostras de energia |
| `N_CHAINS` | 5 | Cadeias independentes por temperatura |
| `GRID_SYMBOL_STYLE` | `"arrows"` | Visualização: `"arrows"` (↑/↓) ou `"letters"` (C/B) |

---

## Modelo

- Spins σᵢ ∈ {+1, −1} em grade n × n com **borda periódica**
- Energia: \(E(\sigma) = \sum_{\langle i,j\rangle} \sigma_i \sigma_j\)
- Distribuição de equilíbrio: \(p_\beta(\sigma) \propto e^{-\beta E(\sigma)}\), com β = 1/T

Em baixa temperatura, vizinhos tendem a ficar **antiparalelos** (padrão tipo tabuleiro). Em alta temperatura, a configuração fica mais desordenada.

---

## Saídas

| Arquivo | Conteúdo |
|---------|----------|
| `figuras/grade_T0_5.png` | Configuração em T = 0,5 |
| `figuras/grade_T2_0.png` | Configuração em T = 2,0 |
| `figuras/energia_vs_T.png` | Gráfico ⟨E⟩ × T para T ∈ (0, 2) |
| `relatorio.pdf` | Relatório para entrega |

---