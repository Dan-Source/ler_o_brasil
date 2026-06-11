# Factory Boy - Guia de Uso

Este projeto utiliza [Factory Boy](https://factoryboy.readthedocs.io/) junto com [Wagtail Factories](https://github.com/wagtail/wagtail-factories) para criar dados de teste e popular o banco de dados de desenvolvimento.

## O que foi implementado

### Factories Disponíveis

1. **UserFactory** (`user.factories`)
   - Cria usuários com senhas hasheadas
   - Traits: `staff`, `superuser`

2. **CategoryFactory** (`home.factories`)
   - Cria categorias com slugs únicos

3. **BlogPostFactory** (`home.factories`)
   - Cria posts de blog com categorias e imagens
   - Trait: `published` (publica o post automaticamente)

4. **AuthorPageFactory** (`home.factories`)
   - Cria páginas de autores

5. **BookPageFactory** (`home.factories`)
   - Cria páginas de livros com autores associados
   - ManyToMany com AuthorPage

6. **EventIndexPageFactory** (`home.factories`)
   - Cria página índice de eventos (singleton)

7. **EventPageFactory** (`home.factories`)
   - Cria páginas de eventos com livros associados
   - Respeita hierarquia (child de EventIndexPage)

## Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Popular o Banco de Dados

Use o management command para popular o banco com dados de teste:

```bash
# Com valores padrão (5 users, 10 categories, 20 blogposts, etc.)
python manage.py populate_database

# Com valores customizados
python manage.py populate_database --users 10 --categories 20 --blogposts 50

# Criar um superusuário
python manage.py populate_database --superuser

# Publicar todos os blog posts
python manage.py populate_database --published
```

### 3. Usar em Testes

```python
from home.factories import BlogPostFactory, CategoryFactory
from user.factories import UserFactory

class MyTestCase(TestCase):
    def test_something(self):
        # Criar um usuário
        user = UserFactory.create()

        # Criar uma categoria
        category = CategoryFactory.create(name='Literatura')

        # Criar um blog post publicado
        blog_post = BlogPostFactory.create(
            title='Meu Post',
            category=category,
            published=True
        )

        # Criar múltiplos objetos
        categories = CategoryFactory.create_batch(5)
```

### 4. Usar no Django Shell

```python
python manage.py shell

>>> from home.factories import *
>>> from user.factories import UserFactory

# Criar um usuário admin
>>> admin = UserFactory.create(username='admin', superuser=True)

# Criar 10 categorias
>>> categories = CategoryFactory.create_batch(10)

# Criar um blog post publicado
>>> post = BlogPostFactory.create(published=True)

# Criar um livro com autores específicos
>>> author1 = AuthorPageFactory.create()
>>> author2 = AuthorPageFactory.create()
>>> book = BookPageFactory.create(authors=[author1, author2])

# Criar eventos
>>> event = EventPageFactory.create()
```

## Traits Disponíveis

### UserFactory
- `staff=True` - Cria usuário com permissões de staff
- `superuser=True` - Cria superusuário

### BlogPostFactory
- `published=True` - Publica o post automaticamente

## Características Especiais

### Dados em Português
As factories usam `Faker` com locale `pt_BR` para gerar dados realistas em português.

### Hierarquia de Páginas Wagtail
As factories de páginas Wagtail (BlogPost, AuthorPage, BookPage, EventPage) automaticamente:
- Adicionam a página à árvore do Wagtail
- Atribuem um owner (User)
- Respeitam hierarquias parent-child (EventPage sob EventIndexPage)

### Relacionamentos ManyToMany
- **BookPage**: Cria automaticamente 1-3 autores
- **EventPage**: Cria automaticamente 1-5 livros

### Imagens
As factories que usam imagens (BlogPost, BookPage) criam automaticamente imagens de teste 1x1 pixel usando `wagtail_factories.ImageFactory`.

## Testes

Execute os testes para verificar que as factories estão funcionando:

```bash
# Todos os testes
python manage.py test

# Apenas testes de factories
python manage.py test home.test_factories
python manage.py test user.tests

# Apenas testes de um modelo
python manage.py test home.tests.BlogPostTests
```

## Senha Padrão

Todos os usuários criados pelas factories têm a senha: **testpass123**

## Troubleshooting

### Erro: "Table doesn't exist"
Execute as migrations primeiro:
```bash
python manage.py migrate
```

### Erro: "Parent page not found"
Certifique-se que existe uma página root no Wagtail. Execute:
```bash
python manage.py shell
>>> from wagtail.models import Page
>>> Page.get_first_root_node()
```

### Performance Lenta
Se criar muitos objetos estiver lento, considere desabilitar signals temporariamente ou usar `.build()` em vez de `.create()` onde possível.

## Referências

- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [Wagtail Factories Documentation](https://github.com/wagtail/wagtail-factories)
- [Faker Documentation](https://faker.readthedocs.io/)
