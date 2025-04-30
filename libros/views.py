from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from .models import Book, DeweyCode
from .forms import BookForm, DeweyCodeForm, SearchForm

def index(request):
    # Get statistics for the index page
    book_count = Book.objects.count()
    dewey_count = DeweyCode.objects.count()
    
    # Buscar libros disponibles con búsqueda insensible a mayúsculas/minúsculas
    # y considerando múltiples posibles valores para "disponible"
    available_count = Book.objects.filter(
        Q(status__iexact='disponible') | 
        Q(status__iexact='disponibles') |
        Q(status__iexact='available')
    ).count()
    
    stats = {
        'book_count': book_count,
        'dewey_count': dewey_count,
        'updated_date': timezone.now().strftime('%Y')
    }
    
    # Calculate availability percentage if there are books
    if book_count > 0:
        availability_percentage = round((available_count / book_count) * 100)
        stats['available_count'] = f"{availability_percentage}%"
    else:
        stats['available_count'] = "0%"
    
    return render(request, 'libros/index.html', stats)

def book_list(request):
    form = SearchForm(request.GET)
    # Solo cargar la vista, no los datos
    return render(request, 'libros/book_list.html', {
        'form': form,
    })

def book_api(request):
    # Parámetros de DataTables
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    
    # Consulta inicial
    queryset = Book.objects.all()
    total = queryset.count()
    
    # Filtrar según término de búsqueda
    if search_value:
        queryset = queryset.filter(
            Q(title__icontains=search_value) |
            Q(author__icontains=search_value) |
            Q(isbn__icontains=search_value) |
            Q(dewey_code__code__icontains=search_value) |
            Q(dewey_code__description__icontains=search_value)
        )
    
    filtered_total = queryset.count()
    
    # Ordenar
    order_column = request.GET.get('order[0][column]', '0')
    order_dir = request.GET.get('order[0][dir]', 'asc')
    
    column_mappings = {
        '0': 'title',
        '1': 'author',
        '2': 'dewey_code__code',
        '3': 'status'
    }
    
    order_column = column_mappings.get(order_column, 'title')
    if order_dir == 'desc':
        order_column = f'-{order_column}'
    
    queryset = queryset.order_by(order_column)
    
    # Paginar resultados
    queryset = queryset[start:start + length]
    
    # Formatear datos para DataTables
    data = []
    for book in queryset:
        data.append({
            'title': book.title,
            'author': book.author,
            'dewey_code': book.dewey_code.code if book.dewey_code else "-",
            'status': book.status,
            'url': reverse('book_detail', args=[book.pk])
        })
    
    # Preparar respuesta
    response = {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': filtered_total,
        'data': data
    }
    
    return JsonResponse(response)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'libros/book_detail.html', {'book': book})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'libros/book_form.html', {
        'form': form,
        'title': 'Agregar Libro'
    })

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'libros/book_form.html', {
        'form': form,
        'title': 'Editar Libro',
        'book': book
    })

def dewey_list(request):
    # Solo cargar la vista, no los datos
    return render(request, 'libros/dewey_list.html')

def dewey_api(request):
    # Parámetros de DataTables
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    
    # Consulta inicial
    queryset = DeweyCode.objects.all()
    total = queryset.count()
    
    # Filtrar según término de búsqueda
    if search_value:
        queryset = queryset.filter(
            Q(code__icontains=search_value) |
            Q(description__icontains=search_value)
        )
    
    filtered_total = queryset.count()
    
    # Ordenar
    order_column = request.GET.get('order[0][column]', '0')
    order_dir = request.GET.get('order[0][dir]', 'asc')
    
    column_mappings = {
        '0': 'code',
        '1': 'description'
    }
    
    order_column = column_mappings.get(order_column, 'code')
    if order_dir == 'desc':
        order_column = f'-{order_column}'
    
    queryset = queryset.order_by(order_column)
    
    # Paginar resultados
    queryset = queryset[start:start + length]
    
    # Formatear datos para DataTables
    data = []
    for dewey in queryset:
        data.append({
            'code': dewey.code,
            'description': dewey.description,
            'url': reverse('dewey_update', args=[dewey.pk])
        })
    
    # Preparar respuesta
    response = {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': filtered_total,
        'data': data
    }
    
    return JsonResponse(response)

def dewey_create(request):
    if request.method == 'POST':
        form = DeweyCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dewey_list')
    else:
        form = DeweyCodeForm()
    
    return render(request, 'libros/dewey_form.html', {
        'form': form,
        'title': 'Agregar Código Dewey'
    })

def dewey_update(request, pk):
    dewey = get_object_or_404(DeweyCode, pk=pk)
    
    if request.method == 'POST':
        form = DeweyCodeForm(request.POST, instance=dewey)
        if form.is_valid():
            form.save()
            return redirect('dewey_list')
    else:
        form = DeweyCodeForm(instance=dewey)
    
    return render(request, 'libros/dewey_form.html', {
        'form': form,
        'title': 'Editar Código Dewey',
        'dewey': dewey
    })

def search_suggestions_api(request):
    query = request.GET.get('query', '')
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Get book suggestions
    book_suggestions = Book.objects.filter(
        Q(title__icontains=query) | 
        Q(author__icontains=query) |
        Q(isbn__icontains=query)
    ).values('title', 'author', 'pk')[:5]  # Limit to 5 results
    
    # Get category suggestions
    category_suggestions = DeweyCode.objects.filter(
        Q(code__icontains=query) | 
        Q(description__icontains=query)
    ).values('code', 'description', 'pk')[:3]  # Limit to 3 results
    
    # Format data for response
    formatted_books = [
        {
            'type': 'book',
            'title': book['title'],
            'author': book['author'],
            'url': reverse('book_detail', args=[book['pk']])
        } for book in book_suggestions
    ]
    
    formatted_categories = [
        {
            'type': 'category',
            'code': category['code'],
            'description': category['description'],
            'url': reverse('book_list') + f"?field=dewey_code&query={category['code']}"
        } for category in category_suggestions
    ]
    
    # Combined results
    suggestions = formatted_books + formatted_categories
    
    return JsonResponse({'suggestions': suggestions})
