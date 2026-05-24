from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Stock
from datetime import date
import random
import string
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from django.http import HttpResponse

def generate_item_id():
    nums    = ''.join([str(random.randint(0,9)) for _ in range(3)])
    letter  = random.choice(string.ascii_uppercase)
    return f"{nums}-{letter}"

@login_required
def stock_list(request):
    from erp_config.models import Category, Unit, Building
    stock_all  = Stock.objects.all().order_by('-date')
    paginator  = Paginator(stock_all, 10)
    page       = request.GET.get('page')
    stocks     = paginator.get_page(page)
    categories = Category.objects.all()
    units      = Unit.objects.all()
    buildings  = Building.objects.filter(type='Growing')
    return render(request, 'stock/list.html', {
        'stocks':     stocks,
        'categories': categories,
        'units':      units,
        'buildings':  buildings,
    })

@login_required
def stock_save(request):
    if request.method == 'POST':
        item_id       = request.POST['item_id']
        name          = request.POST['name']
        price         = request.POST['price']
        quantity      = request.POST['quantity']
        category      = request.POST['category']
        growing_house = request.POST.get('growing_house', '')
        unit          = request.POST.get('unit', '')

        if Stock.objects.filter(item_id=item_id).exists():
            messages.error(request, 'Item ID already exists!')
            return redirect('stock_list')

        Stock.objects.create(
            item_id=item_id, name=name,
            price=price, quantity=quantity,
            category=category, growing_house=growing_house,
            unit=unit
        )
        messages.success(request, f'Stock item "{name}" saved successfully!')
    return redirect('stock_list')

@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    messages.success(request, 'Stock item deleted!')
    return redirect('stock_list')

@login_required
def generate_id(request):
    from django.http import JsonResponse
    item_id = generate_item_id()
    while Stock.objects.filter(item_id=item_id).exists():
        item_id = generate_item_id()
    return JsonResponse({'item_id': item_id})

@login_required
def stock_update(request, pk):
    from erp_config.models import Category, Unit, Building
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        stock.item_id       = request.POST['item_id']
        stock.name          = request.POST['name']
        stock.price         = request.POST['price']
        stock.quantity      = request.POST['quantity']
        stock.category      = request.POST['category']
        stock.growing_house = request.POST.get('growing_house', '')
        stock.unit          = request.POST.get('unit', '')
        stock.save()
        messages.success(request, f'"{stock.name}" updated successfully!')
        return redirect('stock_list')
    categories = Category.objects.all()
    units      = Unit.objects.all()
    buildings  = Building.objects.filter(type='Growing')
    return render(request, 'stock/edit.html', {
        'stock':      stock,
        'categories': categories,
        'units':      units,
        'buildings':  buildings,
    })

@login_required
def export_stock(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Stock'

    header_font = Font(bold=True, color='FFFFFF')
    header_fill = PatternFill(fill_type='solid', fgColor='196E78')

    headers = ['Item ID', 'Name', 'Price', 'Quantity', 'Category',
               'Growing House', 'Unit', 'Date']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')

    for row, stock in enumerate(Stock.objects.all().order_by('-date'), 2):
        ws.cell(row=row, column=1, value=stock.item_id)
        ws.cell(row=row, column=2, value=stock.name)
        ws.cell(row=row, column=3, value=float(stock.price))
        ws.cell(row=row, column=4, value=stock.quantity)
        ws.cell(row=row, column=5, value=stock.category)
        ws.cell(row=row, column=6, value=stock.growing_house)
        ws.cell(row=row, column=7, value=stock.unit)
        ws.cell(row=row, column=8, value=str(stock.date))

    for col, width in enumerate([15, 25, 12, 12, 20, 18, 10, 22], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="stocks_{date.today()}.xlsx"'
    wb.save(response)
    return response