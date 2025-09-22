# MindGuard Demo 🧠🎰
Os Relátórios estão em Arquivos MD aqui na branch principal


Um projetinho **FastAPI** para demonstrar CI/CD com segurança (SAST, DAST, SCA).

## 🚀 Como rodar

```bash
git clone <repo>
cd mindguard_demo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python create_model.py
uvicorn app.main:app --reload --port 8000

# MindGuard Demo Simplificada

Esta é uma versão simplificada do projeto **MindGuard**, sem Machine Learning, mas com vulnerabilidades propositalmente incluídas para testes de segurança (SAST, DAST e SCA).

## Instalação

1. Criar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

