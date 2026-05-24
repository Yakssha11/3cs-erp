from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import LayingFlock, LayingMortality
from datetime import date, timedelta

@login_required
def laying_flock_list(request):
    from erp_config.models import Building, Cause
    from master_data.models import Supplier
    flocks      = LayingFlock.objects.all().order_by('-Date')
    mortalities = LayingMortality.objects.all().order_by('-death_date')

    for flock in flocks:
        if flock.date_placed:
            flock.age_days = (date.today() - flock.date_placed).days
        else:
            flock.age_days = 0

    buildings = Building.objects.filter(type='Laying')
    causes    = Cause.objects.all()
    suppliers = Supplier.objects.all()

    return render(request, 'laying_flock/list.html', {
        'flocks':      flocks,
        'mortalities': mortalities,
        'buildings':   buildings,
        'causes':      causes,
        'suppliers':   suppliers,
    })

@login_required
def laying_flock_save(request):
    if request.method == 'POST':
        LayingFlock.objects.create(
            batch_name    = request.POST['batch_name'],
            building      = request.POST['building'],
            start_count   = request.POST['start_count'],
            current_count = request.POST['start_count'],
            date_placed   = request.POST['date_placed'],
            supplier      = request.POST.get('supplier', ''),
            status        = 'Active',
            notes         = request.POST.get('notes', '')
        )
        messages.success(request, f'Flock added successfully!')
    return redirect('laying_flock_list')

@login_required
def laying_flock_delete(request, pk):
    flock = get_object_or_404(LayingFlock, pk=pk)
    LayingMortality.objects.filter(flock=flock).delete()
    flock.delete()
    messages.success(request, 'Flock deleted!')
    return redirect('laying_flock_list')

@login_required
def laying_flock_update(request, pk):
    from erp_config.models import Building
    from master_data.models import Supplier
    flock = get_object_or_404(LayingFlock, pk=pk)
    if request.method == 'POST':
        flock.batch_name    = request.POST['batch_name']
        flock.building      = request.POST['building']
        flock.start_count   = request.POST['start_count']
        flock.current_count = request.POST['current_count']
        flock.date_placed   = request.POST['date_placed']
        flock.supplier      = request.POST.get('supplier', '')
        flock.status        = request.POST['status']
        flock.notes         = request.POST.get('notes', '')
        flock.save()
        messages.success(request, f'"{flock.batch_name}" updated!')
        return redirect('laying_flock_list')
    buildings = Building.objects.filter(type='Laying')
    suppliers = Supplier.objects.all()
    return render(request, 'laying_flock/edit.html', {
        'flock':     flock,
        'buildings': buildings,
        'suppliers': suppliers,
    })

@login_required
def laying_flock_transfer(request, pk):
    flock = get_object_or_404(LayingFlock, pk=pk)
    if flock.building == 'RTL Building 1':
        flock.building = 'RTL Building 2'
        flock.status   = 'Transferred'
        flock.save()
        messages.success(request, f'"{flock.batch_name}" transferred to RTL Building 2!')
    else:
        messages.error(request, 'This flock is already in RTL Building 2')
    return redirect('laying_flock_list')

@login_required
def laying_mortality_save(request):
    if request.method == 'POST':
        flock = get_object_or_404(LayingFlock, pk=request.POST['flock_id'])
        count = int(request.POST['count'])

        if count > flock.current_count:
            messages.error(request, f'Death count exceeds current flock count ({flock.current_count})')
            return redirect('laying_flock_list')

        LayingMortality.objects.create(
            flock       = flock,
            building    = request.POST['building'],
            death_date  = request.POST['death_date'],
            count       = count,
            cause       = request.POST.get('cause', ''),
            recorded_by = request.POST['recorded_by'],
            remarks     = request.POST.get('remarks', '')
        )
        flock.current_count -= count
        flock.save()
        messages.success(request, f'{count} deaths logged. Remaining: {flock.current_count}')
    return redirect('laying_flock_list')

@login_required
def laying_mortality_delete(request, pk):
    mortality = get_object_or_404(LayingMortality, pk=pk)
    flock     = mortality.flock
    flock.current_count += mortality.count
    flock.save()
    mortality.delete()
    messages.success(request, 'Record deleted and flock count restored!')
    return redirect('laying_flock_list')

@login_required
def laying_mortality_update(request, pk):
    from erp_config.models import Building, Cause
    mortality = get_object_or_404(LayingMortality, pk=pk)
    if request.method == 'POST':
        mortality.building    = request.POST['building']
        mortality.death_date  = request.POST['death_date']
        mortality.count       = request.POST['count']
        mortality.cause       = request.POST.get('cause', '')
        mortality.recorded_by = request.POST['recorded_by']
        mortality.remarks     = request.POST.get('remarks', '')
        mortality.save()
        messages.success(request, 'Mortality record updated!')
        return redirect('laying_flock_list')
    buildings = Building.objects.filter(type='Laying')
    causes    = Cause.objects.all()
    return render(request, 'laying_flock/mortality_edit.html', {
        'mortality': mortality,
        'buildings': buildings,
        'causes':    causes,
    })