#!/bin/bash
# 📚 Script para Acessar Documentação Rapidamente

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cat << 'EOF'

╔════════════════════════════════════════════════════════════╗
║                  📚 DOCUMENTAÇÃO DO PROJETO               ║
║                      ler_o_brasil                          ║
╚════════════════════════════════════════════════════════════╝

A documentação foi organizada centralizadamente na pasta 'docs/'

EOF

echo -e "${GREEN}📂 ESTRUTURA DE DOCUMENTAÇÃO:${NC}"
echo ""
echo "docs/"
echo "├── 📄 README.md (5.4K)                    ← Comece aqui!"
echo "├── 📄 ENV_SETUP.md (7.3K)                 ← Variáveis de ambiente"
echo "├── 📄 DOCKER_SETUP.md (3.4K)              ← Docker Compose"
echo "└── 📄 REFACTORING_SUMMARY.md (9.2K)      ← Detalhes da refatoração"
echo ""

echo -e "${BLUE}🔗 ARQUIVOS DE ÍNDICE NO ROOT:${NC}"
echo ""
echo "├── 📄 DOCUMENTATION.md                    ← Ponteiro para docs/"
echo "└── 📄 DOCS_STRUCTURE.md                   ← Mapa de documentação"
echo ""

echo -e "${YELLOW}🚀 COMO ACESSAR A DOCUMENTAÇÃO:${NC}"
echo ""
echo "1️⃣  Índice Principal:"
echo "    → docs/README.md"
echo ""
echo "2️⃣  Por Cenário:"
echo "    • Desenvolvimento local"
echo "      → docs/ENV_SETUP.md#local-development"
echo ""
echo "    • Docker Compose"
echo "      → docs/DOCKER_SETUP.md#quick-start-with-docker-compose"
echo ""
echo "    • Produção"
echo "      → docs/ENV_SETUP.md#production-deployment"
echo ""
echo "3️⃣  Referências Específicas:"
echo "    • Variáveis de ambiente"
echo "      → docs/ENV_SETUP.md#environment-variables-overview"
echo ""
echo "    • Troubleshooting"
echo "      → docs/ENV_SETUP.md#troubleshooting"
echo ""
echo "    • Detalhes técnicos"
echo "      → docs/REFACTORING_SUMMARY.md"
echo ""

echo -e "${GREEN}✅ DOCUMENTAÇÃO PRONTA PARA CONSULTA!${NC}"
echo ""
echo "Dica: Abra docs/README.md no seu editor favorito para começar!"
echo ""
EOF
