# GUIA AZURE — OrbitalWatch
# Execute esses comandos no Azure Cloud Shell (portal.azure.com → ícone >_)
# Substitua SEU_NOME por algo único (ex: orbitalwatch-joao)

# ─────────────────────────────────────────
# PASSO 1 · Criar Resource Group
# ─────────────────────────────────────────
az group create \
  --name rg-orbitalwatch \
  --location brazilsouth

# ─────────────────────────────────────────
# PASSO 2 · Criar App Service Plan (Free)
# ─────────────────────────────────────────
az appservice plan create \
  --name asp-orbitalwatch \
  --resource-group rg-orbitalwatch \
  --sku FREE \
  --is-linux

# ─────────────────────────────────────────
# PASSO 3 · Criar a Web App
# (mude "orbitalwatch-SEUNOME" para algo único)
# ─────────────────────────────────────────
az webapp create \
  --name orbitalwatch-SEUNOME \
  --resource-group rg-orbitalwatch \
  --plan asp-orbitalwatch \
  --runtime "PYTHON:3.11"

# Configurar startup command
az webapp config set \
  --name orbitalwatch-SEUNOME \
  --resource-group rg-orbitalwatch \
  --startup-file "uvicorn main:app --host 0.0.0.0 --port 8000"

# ─────────────────────────────────────────
# PASSO 4 · Criar Key Vault
# ─────────────────────────────────────────
az keyvault create \
  --name kv-orbital-SEUNOME \
  --resource-group rg-orbitalwatch \
  --location brazilsouth

# Adicionar secret da NASA API
az keyvault secret set \
  --vault-name kv-orbital-SEUNOME \
  --name "nasa-api-key" \
  --value "DEMO_KEY"

# ─────────────────────────────────────────
# PASSO 5 · Criar Service Principal para CI/CD
# (guarde o JSON que aparecer — vai no GitHub Secrets)
# ─────────────────────────────────────────
az ad sp create-for-rbac \
  --name "sp-orbitalwatch-github" \
  --role contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-orbitalwatch \
  --sdk-auth

# ─────────────────────────────────────────
# PASSO 6 · Ativar Application Insights
# (no portal Azure: App Service → Application Insights → Ligar)
# Ou via CLI:
# ─────────────────────────────────────────
az monitor app-insights component create \
  --app ai-orbitalwatch \
  --location brazilsouth \
  --resource-group rg-orbitalwatch

# ─────────────────────────────────────────
# APÓS CRIAR O SERVICE PRINCIPAL:
# Vá em github.com → seu repo → Settings → Secrets → Actions
# Crie os secrets:
#   AZURE_CREDENTIALS  → cole o JSON inteiro do passo 5
#   AZURE_APP_NAME     → orbitalwatch-SEUNOME
# ─────────────────────────────────────────
