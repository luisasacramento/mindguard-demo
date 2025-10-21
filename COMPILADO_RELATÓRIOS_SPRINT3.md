# 📑 Relatório Consolidado de Segurança – Pipeline CI/CD

Este relatório reúne os resultados das análises de segurança automatizadas (SAST, DAST, SCA) e a documentação do pipeline CI/CD para a aplicação **MindGuard Demo Simplificada**.

---

## 1. Relatório de Vulnerabilidades Estáticas (SAST – Semgrep)

### 🔎 Resumo
## 📑 1. SAST – Análise Estática de Código

**Entregável:** Relatório automatizado gerado pelo pipeline CI com as vulnerabilidades encontradas, classificadas por severidade e com recomendações de correção.  

**Arquivos analisados:** `main.py`, `storage.py`  

### Resultados

| Severidade | Localização      | Vulnerabilidade | Evidência / Detalhes | Sugestão de correção |
|------------|------------------|-----------------|----------------------|-----------------------|
| 🔴 Crítica | `main.py` (linha 54) | Execução remota de código (RCE) via `os.system` | Função `/admin/run_eval?cmd=` permite execução arbitrária | Remover `os.system`; usar `subprocess` apenas com whitelist |
| 🟠 Alta    | `main.py` (linha 62) | Exposição de variáveis de ambiente | Endpoint `/leak_env` retorna valores de `os.environ` | Nunca expor variáveis de ambiente; usar vault seguro |
| 🟡 Média   | `main.py` (funções `report`, `leak_env`, `admin`) | Falta de autenticação/autorização | Endpoints sensíveis não requerem credenciais | Implementar autenticação e RBAC |
| 🟢 Baixa   | `submit_bet` e `give_consent` | Falta de validação de entrada | Inputs `amount`, `frequency` e `user_id` não validados | Utilizar **Pydantic Models** para validação |


📂 **Entregável:** `semgrep-report.txt`  

---

## 2. Relatório de Varredura Dinâmica (DAST – OWASP ZAP)

**Ambiente analisado:** `https://mindguard-demo-production.up.railway.app/`

### Resultados

| Severidade | Endpoint | Vulnerabilidade | Payload usado | Evidência | Sugestão de correção |
|------------|----------|-----------------|---------------|-----------|-----------------------|
| 🔴 Crítica | `/admin/run_eval` | Execução remota de código (RCE) | `?cmd=whoami` | Resposta retornou execução do comando no servidor | Remover endpoint ou restringir com autenticação forte |
| 🟠 Alta    | `/leak_env` | Vazamento de informações sensíveis | `?secret_key=SECRET_KEY` | Resposta retornou valor da variável de ambiente | Nunca expor dados de `os.environ` em respostas |
| 🟡 Média   | `/risk/{user_id}` e `/report/{user_id}` | Enumeração de usuários | Teste com IDs existentes/inexistentes | Retorno diferente (`403` vs `404`) | Usar mensagens genéricas para erros de autorização |
| 🟢 Baixa   | Todas as respostas HTTP | Ausência de cabeçalhos de segurança | N/A | Falta de HSTS, CSP e X-Content-Type-Options | Adicionar middleware para headers de segurança |   

📂 **Entregável:** `zap-report.txt`  

---

## 3. Relatório de Dependências (SCA – Snyk)

## 📦 SCA – Análise de Componentes de Terceiros

### Entregável: Relatório de dependências com riscos associados, sugestões de atualização e plano de ação para substituição ou correção.

**Arquivo analisado:** `requirements.txt`

### Resultados

| Severidade | Pacote    | Versão atual | Problema identificado | Sugestão de atualização |
|------------|-----------|--------------|------------------------|--------------------------|
| 🔴 Alta    | fastapi   | 0.95.0       | Vulnerável a DoS por requisições malformadas; CVEs conhecidos em versões < 0.95.2 | Atualizar para `>=0.100.x` |
| 🟠 Média   | pandas    | 1.5.3        | Vulnerabilidades leves de parsing e potenciais problemas de segurança em leitura de arquivos | Atualizar para `>=2.0.0` |
| 🟢 Baixa   | uvicorn   | 0.23.0       | Nenhum CVE crítico, mas versão não é a mais recente | Atualizar para `>=0.25.0` |

### Plano de ação
1. Atualizar o `requirements.txt` para as versões seguras sugeridas.  
2. Rodar novamente os testes automatizados de integração após upgrade.  
3. Implementar monitoramento contínuo de dependências no pipeline (`snyk test --all-projects`).  

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
