from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from .views.category import (
    category_create,
    category_delete,
    category_edit,
    category_list,
)


@hooks.register("register_admin_urls")
def register_category_url():
    return [
        path("categories/", category_list, name="category-list"),
        path("categories/new/", category_create, name="category-create"),
        path("categories/<int:category_id>/edit/", category_edit, name="category-edit"),
        path(
            "categories/<int:category_id>/delete/",
            category_delete,
            name="category-delete",
        ),
    ]


@hooks.register("register_admin_menu_item")
def register_category_menu_item():
    return MenuItem("Categorias", reverse("category-list"), icon_name="list-ul")
