from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.viewsets import ReadOnlyModelViewSet

from home.form import CategoryForm
from home.models.category import Category
from home.serializers.category import CategorySerializer


def category_list(request):
    categories = Category.objects.annotate(posts_count=Count("blog_posts")).order_by(
        "name"
    )
    return render(
        request,
        "home/category_list.html",
        {
            "categories": categories,
            "title": "Categorias",
        },
    )


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria criada com sucesso.")
            return redirect("category-list")
    else:
        form = CategoryForm()

    return render(
        request,
        "home/category_form.html",
        {
            "form": form,
            "title": "Nova categoria",
            "submit_label": "Salvar",
            "back_url": "category-list",
        },
    )


def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso.")
            return redirect("category-list")
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "home/category_form.html",
        {
            "form": form,
            "title": "Editar categoria",
            "submit_label": "Atualizar",
            "category": category,
            "back_url": "category-list",
        },
    )


def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if category.blog_posts.exists():
        messages.error(
            request,
            "Não é possível excluir esta categoria porque ela está associada a um artigo.",
        )
        return redirect("category-list")

    if request.method == "POST":
        category.delete()
        messages.success(request, "Categoria excluída com sucesso.")
        return redirect("category-list")

    return render(
        request,
        "home/category_confirm_delete.html",
        {
            "category": category,
            "title": "Excluir categoria",
            "back_url": "category-list",
        },
    )


class CategoryViewSet(ReadOnlyModelViewSet):
    """ViewSet for viewing categories."""

    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.all()
