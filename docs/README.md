# 📚 Documentação do Projeto - ler_o_brasil

Bem-vindo à documentação centralizada do projeto. Aqui você encontrará guias, tutoriais e referências para entender e trabalhar com o projeto.

## 📋 Índice de Documentação

### 🔧 Configuração de Ambiente

**[ENV_SETUP.md](ENV_SETUP.md)** - Guia Completo de Variáveis de Ambiente
- Overview da refatoração de variáveis de ambiente
- Referência completa de todas as variáveis disponíveis
- Instruções de uso para desenvolvimento local
- Instruções de uso para Docker
- Instruções de implantação em produção
- Guia de multi-ambiente
- Troubleshooting e notas de segurança

### 🐳 Docker Compose

**[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Guia de Setup Docker
- Quick start com Docker Compose
- Instruções passo a passo
- Comandos úteis
- Configuração e persistência de banco de dados
- Troubleshooting específico para Docker
- Informações sobre deployment em produção

### 📝 Refatoração

**[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Resumo da Refatoração
- Objetivo da refatoração
- Detalhes de todas as mudanças realizadas
- Antes e depois de cada arquivo modificado
- Mapeamento de variáveis de ambiente oldName → newName
- Diagrama de como funciona o sistema agora
- Guia de testes para validar o setup
- Breaking changes e próximos passos

## 🎯 Guia Rápido

### Para Desenvolvimento Local

1. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

2. Verifique o arquivo `.env` na raiz do projeto (já configurado com padrões de desenvolvimento)

3. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

4. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

Consulte [ENV_SETUP.md](ENV_SETUP.md#local-development) para mais detalhes.

### Para Docker

1. Verifique se `.env` existe na raiz do projeto

2. Inicie os serviços:
   ```bash
   docker-compose up
   ```

3. Em outro terminal, execute migrações (se necessário):
   ```bash
   docker-compose exec web python manage.py migrate
   ```

Consulte [DOCKER_SETUP.md](DOCKER_SETUP.md#quick-start-with-docker-compose) para mais detalhes.

### Para Produção

1. Copie o template de exemplos:
   ```bash
   cp .envsample .env.production
   ```

2. Configure todas as variáveis para produção

3. Implante usando suas variáveis de ambiente

Consulte [ENV_SETUP.md](ENV_SETUP.md#production-deployment) para mais detalhes.

## 🔑 Variáveis Mais Importantes

| Variável | Propósito | Desenvolvimento | Produção |
|----------|-----------|-----------------|----------|
| `DJANGO_SETTINGS_MODULE` | Módulo de settings Django | `ler_o_brasil.settings.dev` | `ler_o_brasil.settings.production` |
| `DJANGO_DEBUG` | Modo debug | `true` | `false` |
| `DATABASE_HOST` | Host do banco de dados | `db` (docker) ou `localhost` | seu-host-produção |
| `DJANGO_SECRET_KEY` | Chave secreta Django | dev-key | DEVE SER GERADA |
| `SECURE_SSL_REDIRECT` | Redirecionar para HTTPS | `false` | `true` |
| `DJANGO_DEFAULT_ADMIN_USERNAME` | Username do admin padrão | `admin` | configurado no deploy |
| `DJANGO_DEFAULT_ADMIN_EMAIL` | Email do admin padrão | `admin@example.com` | configurado no deploy |
| `DJANGO_DEFAULT_ADMIN_PASSWORD` | Senha do admin padrão | `testpass123` | configurado no deploy |
| `DJANGO_DEFAULT_ADMIN_COUNTRY` | País do admin padrão | `Brasil` | configurado no deploy |

Veja [ENV_SETUP.md#environment-variables-overview](ENV_SETUP.md#environment-variables-overview) para referência completa.

## 🆘 Troubleshooting Rápido

### Variáveis de ambiente não estão sendo carregadas
- Verifique se `.env` existe na raiz do projeto
- Verifique o formato: `CHAVE=valor` (uma por linha, sem espaços)
- Para Docker, reconstrua os containers: `docker-compose down && docker-compose up --build`

Veja [ENV_SETUP.md#troubleshooting](ENV_SETUP.md#troubleshooting) para mais problemas.

## 📞 Estrutura de Arquivos Chave

```
ler_o_brasil/
├── docs/                          # 📚 Esta pasta - Documentação
│   ├── README.md                  # Você está aqui
│   ├── ENV_SETUP.md              # Guia de variáveis de ambiente
│   ├── DOCKER_SETUP.md           # Guia do Docker
│   └── REFACTORING_SUMMARY.md    # Resumo da refatoração
│
├── ler_o_brasil/settings/
│   ├── base.py                   # ⚙️ Carrrega .env aqui
│   ├── dev.py                    # 💻 Configurações desenvolvimento
│   └── production.py             # 🏭 Configurações produção
│
├── .env                          # 🔐 Variáveis de ambiente (desenvolvimento)
├── .envsample                    # 📋 Template para produção
└── docker-compose.yml            # 🐳 Configuração Docker
```

## 🔒 Segurança

⚠️ **IMPORTANTE**:
- Nunca commita o arquivo `.env` para o repositório
- Use `.envsample` como template para novos deployments
- Sempre gere uma nova `DJANGO_SECRET_KEY` para produção
- Nunca coloque secrets hardcoded em código-fonte

Veja [ENV_SETUP.md#security-notes](ENV_SETUP.md#security-notes) para mais informações.

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📖 Referências Externas

- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Django Settings](https://docs.djangoproject.com/en/5.2/topics/settings/)
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)

## 🚀 Próximos Passos

1. **Familiarize-se** com as variáveis de ambiente em [ENV_SETUP.md](ENV_SETUP.md)
2. **Configure** seu ambiente (local ou Docker)
3. **Teste** rodando a aplicação
4. **Consulte** os guias de troubleshooting se necessário

---

**Última atualização**: Fevereiro 2026
**Versão do Django**: 5.2+
**Versão do Wagtail**: 7.2+
