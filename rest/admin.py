# -*- coding: utf-8 -*-
from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

from .models import Node


def set_authorized(modeladmin, request, queryset):
    queryset.update(authorized=True)
set_authorized.short_description = _("Set selected nodes as authorized")


def set_unauthorized(modeladmin, request, queryset):
    queryset.update(authorized=False)
set_unauthorized.short_description = _("Set selected nodes as unauthorized")


class AuthorizedListFilter(admin.SimpleListFilter):
    """Filters the query, so it shows only authorized or unauthorized nodes"""
    title = _("authorized")

    parameter_name = 'authorized'

    def lookups(self, request, model_admin):
        return (
            ('true', _("is authorized")),
            ('false', _("is unauthorized")),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(authorized=True)
        elif self.value() == 'false':
            return queryset.filter(authorized=False)


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_filter = (AuthorizedListFilter, )
    list_display = ('ipaddr', 'token', 'authorized')
    search_fields = ['ipaddr', 'version']
    actions = [set_authorized, set_unauthorized, ]
