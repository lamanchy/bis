from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.forms import inlineformset_factory
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView

from game_book.forms import GameForm, FilterForm
from game_book.models import Game, GameFile

pages = {"pages": {"game_book": "Programy", "new_game": "Vytvořit nový"}}


class GameBookView(TemplateView):
    template_name = "game_book/game_book.html"
    extra_context = {"page": "game_book", **pages}
    form_class = FilterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = Game.objects.all()
        context["form"] = form = FilterForm(self.request.GET)
        setattr(form, 'hide_validation_classes', True)

        if form.is_valid():
            data = form.cleaned_data
            for field, value in data.items():
                if not value:
                    pass
                elif field == 'order':
                    games = games.order_by(data['order'])  # todo order by other fields
                elif field == 'search_input':
                    games = games.annotate(
                        search=SearchVector('name', 'origin', 'short_description', 'goal', 'description', 'motivation',
                                            'notes'),
                    ).filter(search=value)
                elif field.endswith('category') or field == 'tags':
                    games = games.filter(**{f"{field}__in": value})
                elif field == 'only_my_games':
                    games = games.filter(contributor=self.request.user)
                elif field == 'only_my_favourites':
                    games = games.filter(favourites=self.request.user)
                elif field == 'only_watched_by_me':
                    games = games.filter(watchers=self.request.user)
                elif field == 'contributor':
                    games = games.filter(contributor___str__icontains=value)
                else:
                    games = games.filter(**{field: value})

        context["games"] = games
        return context


GameFileFormSet = inlineformset_factory(Game, GameFile, fields=['file'])


class FormsetHandlingMixin:
    formset_class = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('formset', self.formset_class(instance=self.object))
        return context

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # when not ok, return form response
        if response.status_code != 302:
            return response

        formset = self.formset_class(request.POST, request.FILES, instance=self.object)
        if formset.is_valid():
            formset.save()
            messages.info(request, "Úspěšně uloženo")
            return response

        return self.render_to_response(self.get_context_data(formset=formset))


class NewGameView(LoginRequiredMixin, FormsetHandlingMixin, CreateView):
    model = Game
    form_class = GameForm
    formset_class = GameFileFormSet
    extra_context = {"page": "new_game", **pages}

    def form_valid(self, form):
        form.instance.contributor = self.request.user
        return super().form_valid(form)


class EditGameView(LoginRequiredMixin, FormsetHandlingMixin, UpdateView):
    model = Game
    form_class = GameForm
    formset_class = GameFileFormSet
    extra_context = {**pages}


class GameView(DetailView):
    model = Game
    extra_context = {**pages}
