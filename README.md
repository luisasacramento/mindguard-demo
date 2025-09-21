# MindGuard Demo 🧠🎰

Um projetinho **FastAPI + ML** para demonstrar CI/CD com segurança (SAST, DAST, SCA).

## 🚀 Como rodar

```bash
git clone <repo>
cd mindguard_demo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python create_model.py
uvicorn app.main:app --reload --port 8000
