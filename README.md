# 🐉 RPG Combat Manager

Uma aplicação web para gerenciar combates de D&D 5ª edição. Importe personagens e inimigos de uma planilha Excel, controle a iniciativa e acompanhe a saúde e condições de cada combatente em tempo real.

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

## ✨ Características

- 📊 **Upload de Excel** - Importe personagens e inimigos diretamente de uma planilha formatada
- 🎲 **Iniciativa Automática** - Cálculo automático de iniciativa dos combatentes
- ❤️ **Rastreamento de HP** - Acompanhe a vida de cada personagem em tempo real
- 🏠 **Grid de Combate** - Visualização da posição dos combatentes no campo de batalha
- 🛡️ **Condições D&D** - Suporte para 22 condições de D&D 5e (agarrado, amedrontado, envenenado, etc.)
- 🎨 **Temas Personalizáveis** - Customize as cores e aparência da interface

## 🚀 Instalação

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd RPG_app
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No macOS/Linux
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Uso

Execute a aplicação:
```bash
streamlit run RPG_app.py
```

A aplicação abrirá no seu navegador padrão em `http://localhost:8501`.

### Preparando a Planilha Excel

Prepare um arquivo Excel com duas abas:
- **Personagens** - Lista dos jogadores
- **Inimigos** - Lista dos inimigos do encontro

Cada linha deve conter: Nome, Classe de Armadura (CA), Pontos de Vida (HP), Modificador de Iniciativa.

> **Dica:** Use o template fornecido no Google Sheets (link disponível na aplicação) para garantir o formato correto.

## 📁 Estrutura do Projeto

```
RPG_app/
├── RPG_app.py                 # Arquivo principal da aplicação
├── requirements.txt           # Dependências do projeto
├── README.md                  # Esta documentação
├── .gitignore                 # Arquivos ignorados pelo Git
├── components/                # Componentes da interface
│   ├── upload.py             # Gerenciamento de uploads Excel
│   ├── combate_ui.py         # Interface principal de combate
│   ├── grid_combate.py       # Visualização do grid de batalha
│   └── sidebar.py            # Barra lateral de controles
├── logic/                     # Lógica de jogo
│   ├── iniciativa.py         # Cálculo de iniciativa
│   ├── ordem.py              # Ordem de turno
│   └── hp.py                 # Gerenciamento de HP
├── data/                      # Dados da aplicação
│   └── condicoes.py          # Definições das condições D&D
└── styles/                    # Personalização visual
    └── css.py                # Temas e estilos CSS
```

## 📋 Dependências Principais

- **streamlit** - Framework para construção da web app
- **pandas** - Manipulação e análise de dados
- **numpy** - Computação numérica
- **openpyxl** - Leitura de arquivos Excel
- **matplotlib** - Visualizações e gráficos
- **scipy** - Computação científica

Veja `requirements.txt` para a lista completa.

## 🤝 Contribuições

Sinta-se livre para enviar pull requests com melhorias, correções de bugs ou novas features!

## 📝 Licença

Este projeto está disponível sob licença MIT.

---

**Criado com ❤️ para mestres de D&D**
