from admin_numeric_filter.admin import SliderNumericFilter
from admin_numeric_filter.forms import SliderNumericForm
from django.contrib.admin import ListFilter
from django.urls import reverse

from bis.models import *


def get_admin_edit_url(obj):
    url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.id])
    return mark_safe(f'<a href="{url}">{obj}</a>')


class YesNoFilter(admin.SimpleListFilter):
    query = None

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Ano'),
            ('no', 'Ne'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            queryset = queryset.filter(**self.query)
        if self.value() == 'no':
            queryset = queryset.exclude(**self.query)
        return queryset


class HasDonorFilter(YesNoFilter):
    title = 'Má přiřazeného dárce'
    parameter_name = 'has_donor'
    query = {'donor__isnull': False}


class ActiveQualificationFilter(YesNoFilter):
    title = 'Má aktivní kvalifikaci'
    parameter_name = 'active_qualification'
    query = {'qualifications__valid_till__gte': timezone.now().date()}


class ActiveMembershipFilter(YesNoFilter):
    title = 'Má aktivní členství'
    parameter_name = 'active_membership'
    query = {'memberships__year': timezone.now().year}


class IsChairmanFilter(YesNoFilter):
    title = 'Je předseda'
    parameter_name = 'is_chairman'
    query = {'chairman_of__isnull': False}


class IsViceChairmanFilter(YesNoFilter):
    title = 'Je místopředseda'
    parameter_name = 'is_vice_chairman'
    query = {'vice_chairman_of__isnull': False}


class IsManagerFilter(YesNoFilter):
    title = 'Je hospodář'
    parameter_name = 'is_manager'
    query = {'manager_of__isnull': False}


class IsBoardMemberFilter(YesNoFilter):
    title = 'Je člen představenstva'
    parameter_name = 'administration_units'
    query = {'administration_units__isnull': False}


class IsAdministrationUnitActiveFilter(YesNoFilter):
    title = 'Je článek aktivní'
    parameter_name = 'administration_unit_active'
    query = {'existed_till__isnull': True}


class RawSliderNumericFilter(ListFilter):
    parameter_name = None
    min_value = 0
    max_value = 100
    template = 'admin/filter_numeric_slider.html'

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.request = request

        if self.parameter_name + '_from' in params:
            value = params.pop(self.parameter_name + '_from')
            self.used_parameters[self.parameter_name + '_from'] = value

        if self.parameter_name + '_to' in params:
            value = params.pop(self.parameter_name + '_to')
            self.used_parameters[self.parameter_name + '_to'] = value

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.parameter_name + '_from', None)
        if value_from is not None and value_from != '':
            filters.update({self.parameter_name + '__gte': value_from})

        value_to = self.used_parameters.get(self.parameter_name + '_to', None)
        if value_to is not None and value_to != '':
            filters.update({self.parameter_name + '__lte': value_to})

        return queryset.filter(**filters)

    def expected_parameters(self):
        return [
            '{}_from'.format(self.parameter_name),
            '{}_to'.format(self.parameter_name),
        ]

    def has_output(self):
        return True

    def choices(self, changelist):
        return ({
                    'decimals': 0,
                    'step': 1,
                    'parameter_name': self.parameter_name,
                    'request': self.request,
                    'min': self.min_value,
                    'max': self.max_value,
                    'value_from': self.used_parameters.get(self.parameter_name + '_from', self.min_value),
                    'value_to': self.used_parameters.get(self.parameter_name + '_to', self.max_value),
                    'form': SliderNumericForm(name=self.parameter_name, data={
                        self.parameter_name + '_from': self.used_parameters.get(self.parameter_name + '_from',
                                                                                self.min_value),
                        self.parameter_name + '_to': self.used_parameters.get(self.parameter_name + '_to',
                                                                              self.max_value),
                    })
                },)


class MembershipsYearFilter(SliderNumericFilter):
    parameter_name = 'memberships__year'


class AgeFilter(RawSliderNumericFilter):
    title = 'Věk'
    parameter_name = 'age'

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.parameter_name + '_from', None)
        if value_from is not None and value_from != '':
            filters.update({'birthday__lt': now().date() - relativedelta(years=int(value_from))})

        value_to = self.used_parameters.get(self.parameter_name + '_to', None)
        if value_to is not None and value_to != '':
            filters.update({'birthday__gte': now().date() - relativedelta(years=int(value_to) + 1)})

        return queryset.filter(**filters)


class ReadOnlyMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EditableByAdminOnlyMixin:
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class EditableByOfficeMixin:
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_office_worker

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_office_worker

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_office_worker


class EditableByBoardMixin:
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_office_worker or request.user.is_board_member

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_office_worker or request.user.is_board_member

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_office_worker or request.user.is_board_member


class FilterQuerysetMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.can_see_all:
            return queryset

        queryset = self.model.filter_queryset(queryset, request.user)

        ordering = self.get_ordering(request)
        if ordering:
            queryset = queryset.order_by(*ordering)

        return queryset
