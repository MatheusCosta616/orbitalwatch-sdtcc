# 🛰️ OrbitalWatch · Monitoramento Ambiental Satelital

> FIAP · Global Solution 2026 · Engenharia de Software 4º Ano  
> Disciplina: Secure DevOps Tools & Cloud Computing (SDTCC)

---

## 👥 Integrantes

| Nome | RM |
|------|-----|
| [Caíque Walter Silva] | RM-550693 |
| [Guilherme Nobre Bernardo] | RM-98604 |
| [Guilherme Monteiro Espim] | RM-99499 |
| [João Paulo Fonseca Zamperlini] | RM-99279 |
| [Matheus José de Lima Costa] | RM-551157 |

---

## 🌍 Problema & Solução

**Problema:** Queimadas e desmatamento avançam em regiões remotas do Brasil sem monitoramento adequado em tempo real, dificultando respostas rápidas de órgãos ambientais e de defesa civil.

**Solução:** OrbitalWatch é uma plataforma web que consome dados satelitais da NASA (FIRMS — Fire Information for Resource Management System) via satélite VIIRS, exibindo focos de calor ativos no Brasil em um dashboard interativo com mapa e alertas em tempo real.

**ODS Conectado:** ODS 13 — Ação Climática  
**Conexão Espacial:** Dados do satélite Suomi NPP (VIIRS) da NASA, com resolução de 375m.

---

## 🏗️ Arquitetura da Solução

```
[NASA FIRMS API] ──► [FastAPI Backend] ──► [Azure App Service]
                            │                       │
                     [Endpoints REST]      [Application Insights]
                            │                       │
                     [HTML Dashboard]        [Alert Rules]
                     [Leaflet.js Map]
```

**Stack:**
- Backend: Python 3.11 + FastAPI + Uvicorn
- Frontend: HTML/CSS/JS + Leaflet.js (mapas)
- Cloud: Microsoft Azure App Service
- CI/CD: GitHub Actions
- Segurança: Azure Key Vault + GitHub Secrets
- Monitoramento: Azure Application Insights

---

## ☁️ Infraestrutura Azure

| Recurso | Nome | Finalidade |
|---------|------|-----------|
| Resource Group | `rg-orbitalwatch` | Agrupamento de recursos |
| App Service Plan | `asp-orbitalwatch` | Plano de execução (Free F1) |
| App Service | `orbitalwatch-app` | Hospedagem da aplicação |
| Key Vault | `kv-orbitalwatch` | Armazenamento seguro de secrets |
| Application Insights | `ai-orbitalwatch` | Monitoramento e logs |

**URL da aplicação:** `https://orbitalwatch-app.azurewebsites.net`

---

## 🔐 Segurança (DevSecOps)

Secrets armazenados no **GitHub Secrets** (nunca no código):
- `AZURE_CREDENTIALS` — credenciais de service principal do Azure
- `AZURE_APP_NAME` — nome do App Service

Secrets armazenados no **Azure Key Vault** (`kv-orbitalwatch`):
- `nasa-api-key` — chave de acesso à NASA FIRMS API

**IAM:** Role assignment `Contributor` atribuído ao service principal da aplicação no Resource Group.

---

## 🚀 Pipeline CI/CD

O deploy é automatizado via **GitHub Actions** (`.github/workflows/deploy.yml`).

**Trigger:** `git push` na branch `main`

**Fluxo:**
```
push → checkout → setup Python → instalar deps → testar → login Azure → deploy App Service
```

Para demonstrar os 2 deploys obrigatórios, realize 2 commits distintos na branch `main`.

---

## 📊 Monitoramento

- **Application Insights:** ativo, monitorando requests, erros e performance
- **Alert Rule:** configurada para disparar quando o HTTP 5xx rate > 5% por 5 minutos
- **Log Stream:** utilizado durante os testes para validar execução em tempo real

---

## ▶️ Como Executar Localmente

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/orbitalwatch.git
cd orbitalwatch

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar
uvicorn main:app --reload --port 8000

# Acessar
# Dashboard: http://localhost:8000
# API Docs:  http://localhost:8000/docs
# Health:    http://localhost:8000/health
```

---

## 🔌 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Dashboard principal |
| GET | `/health` | Health check da aplicação |
| GET | `/api/fires` | Focos de calor ativos no Brasil (NASA FIRMS) |
| GET | `/api/stats` | Estatísticas gerais da plataforma |
| GET | `/docs` | Documentação Swagger da API |

<!--deploy1-->
