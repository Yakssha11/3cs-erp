from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Program, ProgramStep
from stock.models import Stock

@login_required
def program_growing(request):
    programs     = Program.objects.filter(type='Growing').prefetch_related('steps')
    stock_items  = Stock.objects.all().order_by('name')
    return render(request, 'program/growing.html', {
        'programs':    programs,
        'stock_items': stock_items,
    })

@login_required
def program_laying(request):
    programs     = Program.objects.filter(type='Laying').prefetch_related('steps')
    stock_items  = Stock.objects.all().order_by('name')
    return render(request, 'program/laying.html', {
        'programs':    programs,
        'stock_items': stock_items,
    })

@login_required
def program_save(request):
    if request.method == 'POST':
        Program.objects.create(
            name        = request.POST['name'],
            type        = request.POST['type'],
            description = request.POST.get('description', '')
        )
        messages.success(request, 'Program created!')
    return redirect(request.POST.get('next', 'program_growing'))

@login_required
def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)
    ptype   = program.type
    program.delete()
    messages.success(request, 'Program deleted!')
    if ptype == 'Laying':
        return redirect('program_laying')
    return redirect('program_growing')

@login_required
def step_save(request, program_pk):
    program = get_object_or_404(Program, pk=program_pk)
    if request.method == 'POST':
        ProgramStep.objects.create(
            program     = program,
            week        = request.POST['week'],
            day         = request.POST['day'],
            medicine    = request.POST['medicine'],
            dose_amount = request.POST['dose_amount'],
            dose_unit   = request.POST['dose_unit'],
            dose_per    = request.POST['dose_per'],
            method      = request.POST['method'],
            remarks     = request.POST.get('remarks', '')
        )
        messages.success(request, 'Step added!')
    if program.type == 'Laying':
        return redirect('program_laying')
    return redirect('program_growing')

@login_required
def step_delete(request, pk):
    step  = get_object_or_404(ProgramStep, pk=pk)
    ptype = step.program.type
    step.delete()
    messages.success(request, 'Step deleted!')
    if ptype == 'Laying':
        return redirect('program_laying')
    return redirect('program_growing')

@login_required
def view_growing(request):
    from flock.models import Flock
    from consumption.models import Consumption
    from erp_config.models import Building
    from django.db.models import Sum

    programs     = Program.objects.filter(type='Growing').prefetch_related('steps')
    total_chicks = Flock.objects.filter(status='Active').aggregate(
                    Sum('current_count'))['current_count__sum'] or 0

    growing_buildings = Building.objects.filter(type='Growing').values_list('name', flat=True)

    consumption_totals = {}
    consumptions = Consumption.objects.filter(
                    growing_house__in=growing_buildings
                   ).values('item_name').annotate(total=Sum('quantity'))
    for c in consumptions:
        consumption_totals[c['item_name']] = float(c['total'])

    program_summaries = []
    for program in programs:
        medicine_map = {}
        for step in program.steps.all():
            med = step.medicine
            if med not in medicine_map:
                medicine_map[med] = {
                    'medicine':    med,
                    'dose_amount': float(step.dose_amount),
                    'dose_unit':   step.dose_unit,
                    'dose_per':    step.dose_per,
                    'required':    float(step.dose_amount) * total_chicks,
                    'consumed':    consumption_totals.get(med, 0),
                }
            else:
                medicine_map[med]['required'] += float(step.dose_amount) * total_chicks

        for med in medicine_map.values():
            med['percentage'] = round(
                (med['consumed'] / med['required'] * 100), 1
            ) if med['required'] > 0 else 0

        program_summaries.append({
            'program':  program,
            'summary':  list(medicine_map.values()),
        })

    return render(request, 'program/view_growing.html', {
        'program_summaries': program_summaries,
        'total_chicks':      total_chicks,
    })

@login_required
def view_laying(request):
    from laying_flock.models import LayingFlock
    from consumption.models import Consumption
    from erp_config.models import Building
    from django.db.models import Sum

    programs     = Program.objects.filter(type='Laying').prefetch_related('steps')
    total_chicks = LayingFlock.objects.filter(status='Active').aggregate(
                    Sum('current_count'))['current_count__sum'] or 0

    laying_buildings = Building.objects.filter(type='Laying').values_list('name', flat=True)

    consumption_totals = {}
    consumptions = Consumption.objects.filter(
                    growing_house__in=laying_buildings
                   ).values('item_name').annotate(total=Sum('quantity'))
    for c in consumptions:
        consumption_totals[c['item_name']] = float(c['total'])

    program_summaries = []
    for program in programs:
        medicine_map = {}
        for step in program.steps.all():
            med = step.medicine
            if med not in medicine_map:
                medicine_map[med] = {
                    'medicine':    med,
                    'dose_amount': float(step.dose_amount),
                    'dose_unit':   step.dose_unit,
                    'dose_per':    step.dose_per,
                    'required':    float(step.dose_amount) * total_chicks,
                    'consumed':    consumption_totals.get(med, 0),
                }
            else:
                medicine_map[med]['required'] += float(step.dose_amount) * total_chicks

        for med in medicine_map.values():
            med['percentage'] = round(
                (med['consumed'] / med['required'] * 100), 1
            ) if med['required'] > 0 else 0

        program_summaries.append({
            'program': program,
            'summary': list(medicine_map.values()),
        })

    return render(request, 'program/view_laying.html', {
        'program_summaries': program_summaries,
        'total_chicks':      total_chicks,
    })