from django import forms
from django.forms import ModelForm, TextInput, Form
from django.forms.utils import ErrorList

from administration_units.models import AdministrationUnit
from game_book.models import Game
from game_book_categories.models import Tag, PhysicalCategory, MentalCategory, LocationCategory, \
    ParticipantNumberCategory, ParticipantAgeCategory, GameLengthCategory, PreparationLengthCategory, \
    MaterialRequirementCategory, OrganizersNumberCategory


class FilterForm(Form):
    search_input = forms.CharField(required=False)
    order = forms.ChoiceField(choices=(
        ("-created_at", 'Nejnovější'),
        ("thumbs_up", 'Nejpopulárnější'),
        ("favourites", 'Nejoblíbenější'),
    ))

    only_my_games = forms.BooleanField(required=False)
    only_my_favourites = forms.BooleanField(required=False)
    only_watched_by_me = forms.BooleanField(required=False)
    is_original = forms.BooleanField(required=False)
    is_verified = forms.BooleanField(required=False)

    created_at__gte = forms.DateField(required=False, widget=TextInput(attrs={"type": "date"}))
    created_at__lte = forms.DateField(required=False, widget=TextInput(attrs={"type": "date"}))
    contributor = forms.CharField(required=False)
    administration_unit = forms.ModelChoiceField(queryset=AdministrationUnit.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(),
                                          required=False)
    physical_category = forms.ModelMultipleChoiceField(queryset=PhysicalCategory.objects.all(),
                                                       widget=forms.CheckboxSelectMultiple(), required=False)
    mental_category = forms.ModelMultipleChoiceField(queryset=MentalCategory.objects.all(),
                                                     widget=forms.CheckboxSelectMultiple(), required=False)
    location_category = forms.ModelMultipleChoiceField(queryset=LocationCategory.objects.all(),
                                                       widget=forms.CheckboxSelectMultiple(), required=False)
    participant_number_category = forms.ModelMultipleChoiceField(queryset=ParticipantNumberCategory.objects.all(),
                                                                 widget=forms.CheckboxSelectMultiple(), required=False)
    participant_age_category = forms.ModelMultipleChoiceField(queryset=ParticipantAgeCategory.objects.all(),
                                                              widget=forms.CheckboxSelectMultiple(), required=False)
    game_length_category = forms.ModelMultipleChoiceField(queryset=GameLengthCategory.objects.all(),
                                                          widget=forms.CheckboxSelectMultiple(), required=False)
    preparation_length_category = forms.ModelMultipleChoiceField(queryset=PreparationLengthCategory.objects.all(),
                                                                 widget=forms.CheckboxSelectMultiple(), required=False)
    material_requirement_category = forms.ModelMultipleChoiceField(queryset=MaterialRequirementCategory.objects.all(),
                                                                   widget=forms.CheckboxSelectMultiple(),
                                                                   required=False)
    organizers_number_category = forms.ModelMultipleChoiceField(queryset=OrganizersNumberCategory.objects.all(),
                                                                widget=forms.CheckboxSelectMultiple(), required=False)


class GameForm(ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)
        if not self.instance.contributor_id:
            self.fields.pop('contributor')
        else:
            self.fields['contributor'].choices = [(self.instance.contributor.id, self.instance.contributor)]
            self.fields['contributor'].disabled = True

    class Meta:
        model = Game
        fields = [
            "name",
            "contributor",
            "is_original",
            "origin",
            "administration_unit",
            "is_hidden",
            "is_verified",
            "tags",
            "physical_category",
            "physical_note",
            "mental_category",
            "mental_note",
            "location_category",
            "location_note",
            "participant_number_category",
            "participant_number_note",
            "participant_age_category",
            "participant_age_note",
            "game_length_category",
            "game_length_note",
            "preparation_length_category",
            "preparation_length_note",
            "material_requirement_category",
            "material_requirement_note",
            "organizers_number_category",
            "organizers_number_note",
            "short_description",
            "goal",
            "description",
            "motivation",
            "notes",
        ]
        widgets = {
            "is_hidden": forms.CheckboxInput(attrs={'disabled': True}),
            "is_verified": forms.CheckboxInput(attrs={'disabled': True}),
            "tags": forms.CheckboxSelectMultiple(),
            "physical_category": forms.RadioSelect(),
            "mental_category": forms.RadioSelect(),
            "location_category": forms.CheckboxSelectMultiple(),
            "participant_number_category": forms.CheckboxSelectMultiple(),
            "participant_age_category": forms.CheckboxSelectMultiple(),
            "game_length_category": forms.RadioSelect(),
            "preparation_length_category": forms.RadioSelect(),
            "organizers_number_category": forms.RadioSelect(),
            "material_requirement_category": forms.RadioSelect(),
            "origin": forms.Textarea(attrs={"rows": 2}),
            "physical_note": forms.Textarea(attrs={"rows": 2}),
            "mental_note": forms.Textarea(attrs={"rows": 2}),
            "location_note": forms.Textarea(attrs={"rows": 2}),
            "participant_number_note": forms.Textarea(attrs={"rows": 2}),
            "participant_age_note": forms.Textarea(attrs={"rows": 2}),
            "game_length_note": forms.Textarea(attrs={"rows": 2}),
            "preparation_length_note": forms.Textarea(attrs={"rows": 2}),
            "organizers_number_note": forms.Textarea(attrs={"rows": 2}),
            "material_requirement_note": forms.Textarea(attrs={"rows": 2}),
            "goal": forms.Textarea(attrs={"rows": 2}),
            "description": forms.Textarea(attrs={"rows": 2}),
            "motivation": forms.Textarea(attrs={"rows": 2}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }
