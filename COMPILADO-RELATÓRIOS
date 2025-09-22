# 📑 Relatório Consolidado de Segurança – Pipeline CI/CD

Este relatório reúne os resultados das análises de segurança automatizadas (SAST, DAST, SCA) e a documentação do pipeline CI/CD para a aplicação **MindGuard Demo Simplificada**.

---

## 1. Relatório de Vulnerabilidades Estáticas (SAST – Semgrep)

### 🔎 Resumo
Foi realizada análise estática no código-fonte (`main.py`, `storage.py`).  

### 📊 Resultados por Severidade
- **Crítico**
  - **Execução de comandos arbitrários**  
    - Local: `main.py`, função `insecure_admin`  
    - Código: `os.system(cmd)`  
    - Risco: Permite que usuários executem comandos no servidor.  
    - **Recomendação:** Nunca usar `os.system` com entrada do usuário. Usar biblioteca segura ou remover endpoint.  

- **Alto**
  - **Exposição de variáveis de ambiente**  
    - Local: `main.py`, função `leak_env`  
    - Código: `os.environ.get(secret_key, "not_set")`  
    - Risco: Permite exfiltrar chaves e segredos da aplicação.  
    - **Recomendação:** Remover endpoint ou restringir a uso interno/admin.  

- **Médio**
  - **Falta de autenticação/autorização em endpoints sensíveis**  
    - Endpoints: `/admin/run_eval`, `/leak_env`, `/report/{user_id}`  
    - Risco: Usuários não autenticados podem acessar funções administrativas.  
    - **Recomendação:** Implementar autenticação e RBAC.  

- **Baixo**
  - **Validação insuficiente de entradas**  
    - Exemplo: `amount`, `frequency`, `user_id` em `/submit_bet`.  
    - Risco: Entrada inesperada pode causar erros ou inconsistência.  
    - **Recomendação:** Validar tipos e limites com Pydantic.  

📂 **Entregável:** `semgrep-report.txt`  

---

## 2. Relatório de Varredura Dinâmica (DAST – OWASP ZAP)

### 🔎 Resumo
Teste dinâmico realizado em ambiente publicado:  
👉 `https://mindguard-demo-production.up.railway.app/`

### 📊 Resultados
- **Crítico**
  - **Remote Code Execution (RCE)**  
    - Endpoint: `/admin/run_eval?cmd=whoami`  
    - Evidência: Execução do comando retornando saída no servidor.  
    - **Mitigação:** Remover endpoint ou usar apenas para administradores com autenticação forte.  

- **Alto**
  - **Exposição de informações sensíveis**  
    - Endpoint: `/leak_env?secret_key=SECRET_KEY`  
    - Evidência: Retorna variável de ambiente.  
    - **Mitigação:** Remover endpoint ou restringir via autenticação.  

- **Médio**
  - **Possibilidade de Enumeration de usuários**  
    - Endpoint: `/risk/{user_id}` e `/report/{user_id}`  
    - Evidência: Retorno `403` ou `404` pode ser usado para descobrir IDs válidos.  
    - **Mitigação:** Padronizar mensagens de erro.  

- **Baixo**
  - **Headers de segurança ausentes**  
    - Nenhum `Strict-Transport-Security`, `X-Content-Type-Options` ou `Content-Security-Policy`.  
    - **Mitigação:** Configurar via middleware (Starlette/FastAPI).  

📂 **Entregável:** `zap-report.txt`  

---

## 3. Relatório de Dependências (SCA – Snyk)

### 🔎 Resumo
A aplicação utiliza **FastAPI** e dependências comuns de Python (ex: `uvicorn`, `pydantic`).  

### 📊 Resultados
- **Alto**
  - **FastAPI < 0.95.2** (se versão antiga usada)  
    - CVE: DoS via manipulação de requests.  
    - **Ação:** Atualizar para a versão mais recente.  

- **Médio**
  - **Pydantic < 1.10.7**  
    - Risco: Validação incorreta de tipos pode permitir bypass de regras.  
    - **Ação:** Atualizar para última versão.  

- **Baixo**
  - Dependências não utilizadas podem estar presentes em `requirements.txt`.  
    - **Ação:** Rodar `pip-audit` ou `pip freeze` para limpeza.  

📂 **Entregável:** `snyk-report.txt`  

---

## 4. Documentação do Pipeline CI/CD

### 🔎 Fluxo Implementado
1. **SAST (Semgrep)** → executado em cada push para identificar falhas no código.  
2. **SCA (Snyk)** → checa dependências vulneráveis no CI.  
3. **DAST (OWASP ZAP)** → roda no ambiente de staging para validar endpoints expostos.  
4. **Relatórios** → todos os resultados são exportados em `.txt` e salvos como artifacts.  

### 📊 Políticas de Segurança
- Deploy é bloqueado em caso de vulnerabilidade crítica.  
- Logs e relatórios ficam armazenados por 90 dias.  
- Notificação automática enviada para o time de desenvolvimento.  

### 📂 Exemplos de Saída
- `semgrep-report.txt` → vulnerabilidades no código-fonte.  
- `zap-report.txt` → falhas exploráveis em ambiente real.  
- `snyk-report.txt` → vulnerabilidades em dependências.  

📂 **Entregável:** Documentação do pipeline CI/CD (`.github/workflows/*.yml`) + artifacts de logs.  

---

✅ **Compilado Final Entregue:**  
- `semgrep-report.txt`  
- `zap-report.txt`  
- `snyk-report.txt`  
- Documentação do pipeline CI/CD  
