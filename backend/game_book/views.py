from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DetailView

from game_book.forms import GameForm
from game_book.models import Game, GameFile

pages = {"pages": {"game_book": "Programy", "new_game": "Vytvořit nový"}}


class GameBookView(TemplateView):
    template_name = "game_book/game_book.html"
    extra_context = {"page": "game_book", **pages}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Game.objects.all()
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