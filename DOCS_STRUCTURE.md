# 📁 Estrutura de Documentação Organizada

## 📍 Localização Atual

A documentação foi centralizada na pasta **`docs/`** para facilitar consultas futuras e manutenção.

### Estrutura de Pastas

```
ler_o_brasil/
│
├── 📂 docs/                          ← 📚 DOCUMENTAÇÃO CENTRALIZADA
│   ├── 📄 README.md                  ← Comece aqui! Índice principal
│   ├── 📄 ENV_SETUP.md              ← Guia de variáveis de ambiente
│   ├── 📄 DOCKER_SETUP.md           ← Guia do Docker Compose
│   └── 📄 REFACTORING_SUMMARY.md    ← Resumo da refatoração
│
├── 📄 DOCUMENTATION.md               ← Ponteiro para docs/
├── 📄 FACTORIES_GUIDE.md             ← Documentação de factories
│
├── 📂 ler_o_brasil/                 ← Código do Django
│   ├── 📂 settings/
│   │   ├── base.py                  ← Carrega .env aqui
│   │   ├── dev.py
│   │   └── production.py
│   └── ...
│
├── 📄 .env                           ← Variáveis de ambiente (desenvolvimento)
├── 📄 .envsample                     ← Template para produção
└── 📄 docker-compose.yml             ← Configuração Docker
```

## 🗂️ Mapa de Documentação

### Pasta `docs/`

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| **README.md** | 📖 | **📚 ÍNDICE PRINCIPAL** - Comece sempre aqui |
| **ENV_SETUP.md** | 🔧 | Referência completa de variáveis de ambiente |
| **DOCKER_SETUP.md** | 🐳 | Guia prático do Docker Compose |
| **REFACTORING_SUMMARY.md** | 📝 | Documentação técnica da refatoração |

### Root do Projeto

| Arquivo | Propósito |
|---------|----------|
| **DOCUMENTATION.md** | Ponteiro para a pasta `docs/` |
| **FACTORIES_GUIDE.md** | Guia de factories (documentação anterior) |

## 🎯 Como Usar Esta Documentação

### 📚 Primeira Leitura
1. Leia: **[docs/README.md](docs/README.md)**
2. Escolha seu cenário (Development, Docker, Production)

### 🔧 Para Configurar Variáveis de Ambiente
→ **[docs/ENV_SETUP.md](docs/ENV_SETUP.md)**

### 🐳 Para Usar Docker
→ **[docs/DOCKER_SETUP.md](docs/DOCKER_SETUP.md)**

### 📝 Para Entender a Refatoração
→ **[docs/REFACTORING_SUMMARY.md](docs/REFACTORING_SUMMARY.md)**

## 🚀 Quick Links

| Tarefa | Link |
|--------|------|
| **Começar agora** | [docs/README.md](docs/README.md) |
| **Setup local** | [docs/ENV_SETUP.md#local-development](docs/ENV_SETUP.md#local-development) |
| **Setup Docker** | [docs/DOCKER_SETUP.md#quick-start-with-docker-compose](docs/DOCKER_SETUP.md#quick-start-with-docker-compose) |
| **Setup produção** | [docs/ENV_SETUP.md#production-deployment](docs/ENV_SETUP.md#production-deployment) |
| **Troubleshooting** | [docs/ENV_SETUP.md#troubleshooting](docs/ENV_SETUP.md#troubleshooting) |
| **Variáveis de ambiente** | [docs/ENV_SETUP.md#environment-variables-overview](docs/ENV_SETUP.md#environment-variables-overview) |

## ✅ Checklist de Documentação

- ✅ Documentação centralizada em `docs/`
- ✅ README principal criado (`docs/README.md`)
- ✅ Guia de variáveis de ambiente (`docs/ENV_SETUP.md`)
- ✅ Guia do Docker (`docs/DOCKER_SETUP.md`)
- ✅ Resumo da refatoração (`docs/REFACTORING_SUMMARY.md`)
- ✅ Ponteiro no root (`DOCUMENTATION.md`)
- ✅ Arquivos originais atualizados com redirecionamento

## 📖 Convenção de Nomes

Os arquivos Markdown seguem a convenção:
- **`README.md`** - Índice e guia de início rápido
- **`*_SETUP.md`** - Guias de configuração
- **`*_GUIDE.md`** - Guias educacionais
- **`*_SUMMARY.md`** - Resumos técnicos

## 🔐 Notas Importantes

⚠️ **Segurança**:
- O arquivo `.env` NÃO é versionado (está em `.gitignore`)
- Use `.envsample` como template
- Leia: [docs/ENV_SETUP.md#security-notes](docs/ENV_SETUP.md#security-notes)

## 📞 Arquivo para Consulta Futura

Esta documentação foi organizada para ser facilmente consultada no futuro:
- 📍 **Localizada em**: `docs/` (pasta dedicada)
- 📚 **Organizada por**: Type de conteúdo (Setup, Guide, Summary)
- 🔗 **Interligada**: Todos os arquivos se referenciam
- 📖 **Com índice**: `docs/README.md` serve como hub central

---

**Última atualização**: Fevereiro 2026
**Próxima revisão recomendada**: Quando houver mudanças significativas no setup
