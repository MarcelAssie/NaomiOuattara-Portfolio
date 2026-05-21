from django import forms
from .models import Category, Project, ProjectMedia


INPUT_CLASS = (
    "w-full bg-white border-2 border-ink rounded-2xl px-5 py-4 "
    "text-sm outline-none focus:bg-lime focus:ring-0 "
    "shadow-[3px_3px_0_#111]"
)

TEXTAREA_CLASS = (
    "w-full bg-white border-2 border-ink rounded-2xl px-5 py-4 "
    "text-sm outline-none focus:bg-lime focus:ring-0 "
    "shadow-[3px_3px_0_#111] min-h-[180px]"
)

SELECT_CLASS = (
    "w-full bg-white border-2 border-ink rounded-2xl px-5 py-4 "
    "text-sm outline-none focus:bg-lime focus:ring-0 "
    "shadow-[3px_3px_0_#111]"
)

FILE_CLASS = (
    "w-full text-sm font-semibold file:mr-4 file:rounded-full "
    "file:border-2 file:border-ink file:bg-paper file:px-5 file:py-3 "
    "file:text-xs file:uppercase file:font-bold hover:file:bg-coral"
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        labels = {"name": "Nom de la catégorie"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class": INPUT_CLASS,
            "placeholder": "Ex : Affiche, Packaging, Web design..."
        })


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title", "category", "description", "details",
            "year", "client", "thumbnail", "cover_image",
            "order", "is_featured",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({
            "class": INPUT_CLASS,
            "placeholder": "Ex : Identité visuelle — Maison Nova"
        })

        self.fields["category"].widget.attrs.update({
            "class": SELECT_CLASS
        })

        self.fields["description"].widget.attrs.update({
            "class": TEXTAREA_CLASS,
            "placeholder": "Résumé court du projet..."
        })

        self.fields["details"].widget.attrs.update({
            "class": TEXTAREA_CLASS,
            "placeholder": "Explique le contexte, l’intention, les choix graphiques..."
        })

        self.fields["year"].widget.attrs.update({
            "class": INPUT_CLASS
        })

        self.fields["client"].widget.attrs.update({
            "class": INPUT_CLASS,
            "placeholder": "Ex : Projet étudiant, client fictif, association..."
        })

        self.fields["thumbnail"].widget.attrs.update({
            "class": FILE_CLASS
        })

        self.fields["cover_image"].widget.attrs.update({
            "class": FILE_CLASS
        })

        self.fields["order"].widget.attrs.update({
            "class": INPUT_CLASS
        })

        self.fields["is_featured"].widget.attrs.update({
            "class": "w-6 h-6 accent-coral"
        })


class ProjectMediaForm(forms.ModelForm):
    class Meta:
        model = ProjectMedia
        fields = ["media_type", "file", "caption", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["media_type"].widget.attrs.update({
            "class": SELECT_CLASS
        })

        self.fields["file"].widget.attrs.update({
            "class": FILE_CLASS
        })

        self.fields["caption"].widget.attrs.update({
            "class": INPUT_CLASS,
            "placeholder": "Ex : Détail typographique, affiche finale..."
        })

        self.fields["order"].widget.attrs.update({
            "class": INPUT_CLASS
        })


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        if hasattr(files, "getlist"):
            return files.getlist(name)
        return super().value_from_datadict(data, files, name)


class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]

        return result


class MultipleProjectMediaForm(forms.Form):
    media_type = forms.ChoiceField(
        choices=ProjectMedia.MEDIA_TYPE_CHOICES,
        label="Type des médias"
    )

    files = MultipleFileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        label="Fichiers",
        required=True
    )

    caption = forms.CharField(
        max_length=255,
        required=False,
        label="Légende commune"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["media_type"].widget.attrs.update({"class": SELECT_CLASS})
        self.fields["files"].widget.attrs.update({"class": FILE_CLASS})
        self.fields["caption"].widget.attrs.update({
            "class": INPUT_CLASS,
            "placeholder": "Ex : Photos personnalisées"
        })
