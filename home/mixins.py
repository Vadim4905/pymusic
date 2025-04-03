from django.contrib.auth.mixins import UserPassesTestMixin
from home import forms

class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None  # List of group names

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        if self.group_required is None:
            return True

        if isinstance(self.group_required, str):
            groups = [self.group_required]
        else:
            groups = self.group_required

        return self.request.user.groups.filter(name__in=groups).exists() or self.request.user.is_superuser


class PlaylistContextFormMixin():
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['playlist_form'] = forms.PLaylistForm
        return context