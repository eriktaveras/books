from django import forms
from .models import Book, DeweyCode

# Clases comunes de Tailwind para inputs y selects
INPUT_CLASSES = "w-full py-3 px-4 border border-black bg-white font-medium text-base focus:outline-none focus:border-dark-gray focus:shadow-sm transition-all duration-300 mb-0"
SELECT_CLASSES = "w-full py-3 px-4 border border-black bg-white font-medium text-base focus:outline-none focus:border-dark-gray focus:shadow-sm transition-all duration-300 mb-0 appearance-none"

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'publication_year', 
                 'isbn', 'dewey_code', 'location', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Título del libro'
            }),
            'author': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Autor del libro'
            }),
            'publisher': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Editorial'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Año de publicación',
                'min': '1800',
                'max': '2100'
            }),
            'isbn': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'ISBN'
            }),
            'dewey_code': forms.Select(attrs={
                'class': SELECT_CLASSES
            }),
            'location': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Ubicación en biblioteca'
            }),
            'status': forms.Select(attrs={
                'class': SELECT_CLASSES
            }, choices=[
                ('disponible', 'Disponible'),
                ('prestado', 'Prestado'),
                ('reservado', 'Reservado'),
                ('en reparación', 'En reparación'),
                ('extraviado', 'Extraviado')
            ]),
        }

class DeweyCodeForm(forms.ModelForm):
    class Meta:
        model = DeweyCode
        fields = ['code', 'description']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Código Dewey (ej: 001.12)'
            }),
            'description': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Descripción del código'
            }),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'w-full py-3 px-4 border border-black bg-white font-medium focus:outline-none focus:border-dark-gray focus:shadow-sm transition-all duration-200 mb-0',
            'placeholder': 'Buscar libros...'
        })
    )
    field = forms.ChoiceField(
        required=False,
        choices=[
            ('all', 'Todos los campos'),
            ('title', 'Título'),
            ('author', 'Autor'),
            ('isbn', 'ISBN'),
            ('dewey_code', 'Código Dewey'),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full py-3 px-4 border border-black bg-white font-medium focus:outline-none focus:border-dark-gray focus:shadow-sm transition-all duration-200 mb-0 appearance-none'
        })
    ) 