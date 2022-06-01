from django.http import HttpResponseRedirect
from django.urls import reverse
from nested_admin.nested import NestedModelAdmin

from bis.admin_helpers import FilterQuerysetMixin
from event.models import *
from other.models import DuplicateUser


@admin.register(DuplicateUser)
class DuplicateUserAdmin(FilterQuerysetMixin, NestedModelAdmin):
    change_form_template = 'bis/duplicate_user_change_form.html'

    model = DuplicateUser
    list_display = 'user', 'other', 'get_user_info', 'get_other_info'
    raw_id_fields = 'user', 'other'

    list_select_related = 'user__address', 'other__address'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('user__emails', 'other__emails')

    def get_readonly_fields(self, request, obj=None):
        if obj: return 'get_user_info', 'get_other_info'
        return ()

    def get_info(self, user):
        emails = ", ".join(str(email) for email in user.emails.all())
        return mark_safe(
            f"{user}<br>Nar: {user.birthday}<br>Adr: {getattr(user, 'address', '')}<br>E-maily: {emails}<br>Tel: {user.phone}")

    @admin.display(description='Primární uživatel')
    def get_user_info(self, obj):
        return self.get_info(obj.user)

    @admin.display(description='Duplicitní uživatel')
    def get_other_info(self, obj):
        return self.get_info(obj.other)

    def response_change(self, request, obj):
        if "_merge_users" in request.POST or "_merge_users_rev" in request.POST:
            if "_merge_users" in request.POST:
                obj.user.merge_with(obj.other)
            else:
                obj.other.merge_with(obj.user)
            return HttpResponseRedirect(reverse('admin:other_duplicateuser_changelist'))

        return super().response_change(request, obj)

    def render_change_form(self, request, context, obj=None, *args, **kwargs):
        if obj: context['merge_disabled'] = not obj.can_be_merged_by(request.user)
        return super().render_change_form(request, context, obj, *args, **kwargs)