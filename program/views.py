from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Program, ProgramStep
from stock.models import Stock

@login_required
def program_growing(request):
    from erp_config.models import Unit
    programs    = Program.objects.filter(type='Growing').prefetch_related('steps')
    stock_items = Stock.objects.all().order_by('name')
    units       = Unit.objects.all()
    return render(request, 'program/growing.html', {
        'programs':    programs,
        'stock_items': stock_items,
        'units':       units,
    })

@login_required
def program_laying(request):
    from erp_config.models import Unit
    programs    = Program.objects.filter(type='Laying').prefetch_related('steps')
    stock_items = Stock.objects.all().order_by('name')
    units       = Unit.objects.all()
    return render(request, 'program/laying.html', {
        'programs':    programs,
        'stock_items': stock_items,
        'units':       units,
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
            program            = program,
            cycle              = request.POST.get('cycle', 1),
            week               = request.POST['week'],
            day                = request.POST['day'],
            medicine           = request.POST.get('medicine', ''),
            dose_amount        = request.POST.get('dose_amount') or None,
            dose_unit          = request.POST.get('dose_unit', ''),
            dose_per           = request.POST.get('dose_per', ''),
            method             = request.POST.get('method', ''),
            remarks            = request.POST.get('remarks', ''),
            feed_rate_per_bird = request.POST.get('feed_rate_per_bird') or None,
            feed_unit          = request.POST.get('feed_unit', ''),
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
def step_update(request, pk):
    step = get_object_or_404(ProgramStep, pk=pk)
    if request.method == 'POST':
        step.cycle              = request.POST.get('cycle', 1)
        step.week               = request.POST['week']
        step.day                = request.POST['day']
        step.medicine           = request.POST.get('medicine', '')
        step.dose_amount        = request.POST.get('dose_amount') or None
        step.dose_unit          = request.POST.get('dose_unit', '')
        step.dose_per           = request.POST.get('dose_per', '')
        step.method             = request.POST.get('method', '')
        step.remarks            = request.POST.get('remarks', '')
        step.feed_rate_per_bird = request.POST.get('feed_rate_per_bird') or None
        step.feed_unit          = request.POST.get('feed_unit', '')
        step.save()
        messages.success(request, 'Step updated!')
    if step.program.type == 'Laying':
        return redirect('program_laying')
    return redirect('program_growing')

@login_required
def export_program(request, pk):
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    from django.http import HttpResponse
    from flock.models import Flock
    from laying_flock.models import LayingFlock
    from django.db.models import Sum

    program = get_object_or_404(Program, pk=pk)

    # get population from active flock
    if program.type == 'Growing':
        total_birds = Flock.objects.filter(status='Active').aggregate(
            Sum('current_count'))['current_count__sum'] or 0
    else:
        total_birds = LayingFlock.objects.filter(status='Active').aggregate(
            Sum('current_count'))['current_count__sum'] or 0

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = program.name[:31]  # excel sheet name max 31 chars

    # ── styles ──────────────────────────────────────────
    header_font     = Font(bold=True, color='FFFFFF', size=10)
    subheader_font  = Font(bold=True, color='FFFFFF', size=10)
    center          = Alignment(horizontal='center', vertical='center')
    left            = Alignment(horizontal='left',   vertical='center')

    # column header colors (matching your Excel screenshot)
    blue_fill    = PatternFill(fill_type='solid', fgColor='2E75B6')
    purple_fill  = PatternFill(fill_type='solid', fgColor='7030A0')
    teal_fill    = PatternFill(fill_type='solid', fgColor='17A98A')
    orange_fill  = PatternFill(fill_type='solid', fgColor='C55A11')
    green_fill   = PatternFill(fill_type='solid', fgColor='375623')
    amber_fill   = PatternFill(fill_type='solid', fgColor='C9A227')

    # ── column headers (row 1) ───────────────────────────
    headers = [
        ('Cycle #',               blue_fill),
        ('Age Display',           blue_fill),
        ('Population',            blue_fill),
        ('Medicine Name',         purple_fill),
        ('UoM',                   purple_fill),
        ('Dosage Rate (per Bird)', purple_fill),
        ('Total Dosage',          purple_fill),
        ('Feed Rate (g/bird)',    orange_fill),
        ('Total Feed',            orange_fill),
        ('House Pen',             teal_fill),
        ('Remarks',               green_fill),
    ]

    for col, (header, fill) in enumerate(headers, 1):
        cell            = ws.cell(row=1, column=col, value=header)
        cell.font       = header_font
        cell.fill       = fill
        cell.alignment  = center

    # ── column widths ────────────────────────────────────
    col_widths = [10, 16, 12, 20, 8, 22, 14, 20, 12, 18, 20]
    for col, width in enumerate(col_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width

    # ── data rows ────────────────────────────────────────
    steps = program.steps.all()  # already ordered by cycle, week, day

    for row_num, step in enumerate(steps, 2):
        # age display logic
        if step.week == 0:
            age_display = f'Day {step.day}'
        else:
            age_display = f'Week {step.week}-Day {step.day}'

        # computed totals
        total_dosage = float(step.dose_amount) * total_birds if step.dose_amount else ''
        total_feed   = float(step.feed_rate_per_bird) * total_birds if step.feed_rate_per_bird else ''

        row_data = [
            step.cycle,
            age_display,
            total_birds,
            step.medicine or '',
            step.dose_unit or '',
            float(step.dose_amount) if step.dose_amount else '',
            total_dosage,
            float(step.feed_rate_per_bird) if step.feed_rate_per_bird else '',
            total_feed,
            '',   # house pen — blank on template, filled per batch
            step.remarks or '',
        ]

        for col, value in enumerate(row_data, 1):
            cell           = ws.cell(row=row_num, column=col, value=value)
            cell.alignment = left

        # alternate row shading for readability
        if row_num % 2 == 0:
            light_fill = PatternFill(fill_type='solid', fgColor='EBF3FB')
            for col in range(1, len(headers) + 1):
                ws.cell(row=row_num, column=col).fill = light_fill

    # freeze top row
    ws.freeze_panes = 'A2'

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{program.name}_{program.type}.xlsx"'
    wb.save(response)
    return response

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
            if not med:
                continue
            if med not in medicine_map:
                medicine_map[med] = {
                    'medicine':    med,
                    'dose_amount': float(step.dose_amount) if step.dose_amount else 0,
                    'dose_unit':   step.dose_unit,
                    'dose_per':    step.dose_per,
                    'required':    float(step.dose_amount) * total_chicks if step.dose_amount else 0,
                    'consumed':    consumption_totals.get(med, 0),
                }
            else:
                medicine_map[med]['required'] += float(step.dose_amount) * total_chicks if step.dose_amount else 0

        for med in medicine_map.values():
            med['percentage'] = round(
                (med['consumed'] / med['required'] * 100), 1
            ) if med['required'] > 0 else 0

        program_summaries.append({
            'program': program,
            'summary': list(medicine_map.values()),
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
            if not med:
                continue
            if med not in medicine_map:
                medicine_map[med] = {
                    'medicine':    med,
                    'dose_amount': float(step.dose_amount) if step.dose_amount else 0,
                    'dose_unit':   step.dose_unit,
                    'dose_per':    step.dose_per,
                    'required':    float(step.dose_amount) * total_chicks if step.dose_amount else 0,
                    'consumed':    consumption_totals.get(med, 0),
                }
            else:
                medicine_map[med]['required'] += float(step.dose_amount) * total_chicks if step.dose_amount else 0

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