from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EggPriceConfig, Building, Category, Unit, Cause, SalesTarget, ChickenPriceConfig

@login_required
def config_view(request):
    current_price = EggPriceConfig.objects.first()
    price_history = EggPriceConfig.objects.all().order_by('-effective_date')
    buildings     = Building.objects.all()
    categories    = Category.objects.all()
    units         = Unit.objects.all()
    causes        = Cause.objects.all()
    targets       = SalesTarget.objects.all()
    current_chicken_price = ChickenPriceConfig.objects.first()
    chicken_price_history = ChickenPriceConfig.objects.all().order_by('-effective_date')

    return render(request, 'erp_config/config.html', {
        'current_price':        current_price,
        'price_history':        price_history,
        'buildings':            buildings,
        'categories':           categories,
        'units':                units,
        'causes':               causes,
        'targets':              targets,
        'current_chicken_price': current_chicken_price,
        'chicken_price_history': chicken_price_history,
        'active_tab':           request.GET.get('tab', 'price'),
    })

@login_required
def config_save(request):
    if request.method == 'POST':
        price    = request.POST.get('price_per_egg')
        eff_date = request.POST.get('effective_date')
        try:
            EggPriceConfig.objects.create(
                price_per_egg  = price,
                effective_date = eff_date,
                set_by         = request.user.username
            )
            messages.success(request, f'Egg price set to ₱{price} effective {eff_date}!')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return redirect('/config/?tab=price')

# ── Buildings ─────────────────────────────────────────────
@login_required
def building_save(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        type = request.POST.get('type', '')
        if name:
            Building.objects.create(name=name, type=type)
            messages.success(request, f'Building "{name}" added!')
        else:
            messages.error(request, 'Building name is required.')
    return redirect('/config/?tab=buildings')

@login_required
def building_delete(request, pk):
    building = get_object_or_404(Building, pk=pk)
    building.delete()
    messages.success(request, f'Building "{building.name}" deleted!')
    return redirect('/config/?tab=buildings')

# ── Categories ────────────────────────────────────────────
@login_required
def category_save(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.get_or_create(name=name)
            messages.success(request, f'Category "{name}" added!')
        else:
            messages.error(request, 'Category name is required.')
    return redirect('/config/?tab=categories')

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, f'Category "{category.name}" deleted!')
    return redirect('/config/?tab=categories')

# ── Units ─────────────────────────────────────────────────
@login_required
def unit_save(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Unit.objects.get_or_create(name=name)
            messages.success(request, f'Unit "{name}" added!')
        else:
            messages.error(request, 'Unit name is required.')
    return redirect('/config/?tab=units')

@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    messages.success(request, f'Unit "{unit.name}" deleted!')
    return redirect('/config/?tab=units')

# ── Causes ────────────────────────────────────────────────
@login_required
def cause_save(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Cause.objects.get_or_create(name=name)
            messages.success(request, f'Cause "{name}" added!')
        else:
            messages.error(request, 'Cause name is required.')
    return redirect('/config/?tab=causes')

@login_required
def cause_delete(request, pk):
    cause = get_object_or_404(Cause, pk=pk)
    cause.delete()
    messages.success(request, f'Cause "{cause.name}" deleted!')
    return redirect('/config/?tab=causes')

# ── Sales Targets ─────────────────────────────────────────
@login_required
def target_save(request):
    if request.method == 'POST':
        type         = request.POST.get('type', '')
        building     = request.POST.get('building', '').strip()
        target       = request.POST.get('target_revenue', '')
        period_start = request.POST.get('period_start', '')
        period_end   = request.POST.get('period_end', '')

        if target and period_start and period_end:
            # for Growing — building is blank (combined)
            if type == 'Growing':
                building = ''

            SalesTarget.objects.create(
                building       = building,
                type           = type,
                target_revenue = target,
                period_start   = period_start,
                period_end     = period_end,
                set_by         = request.user.username
            )
            label = 'Growing (All Houses)' if type == 'Growing' else building
            messages.success(request, f'Target for {label} saved!')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return redirect('/config/?tab=targets')

@login_required
def target_delete(request, pk):
    target = get_object_or_404(SalesTarget, pk=pk)
    target.delete()
    messages.success(request, f'Target for {target.building} deleted!')
    return redirect('/config/?tab=targets')

@login_required
def chicken_price_save(request):
    if request.method == 'POST':
        ChickenPriceConfig.objects.create(
            price_chicken  = request.POST['price_chicken'],
            effective_date = request.POST['effective_date'],
            set_by         = request.user.username
        )
        messages.success(request, 'Chicken price updated!')
    return redirect('/config/?tab=chicken_price')