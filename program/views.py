from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Program, ProgramStep
from stock.models import Stock

@login_required
def program_growing(request):
    from erp_config.models import Unit
    from master_data.models import Material
    programs  = Program.objects.filter(type='Growing').prefetch_related('steps')
    materials = Material.objects.all().order_by('name')
    units     = Unit.objects.all()
    return render(request, 'program/growing.html', {
        'programs':  programs,
        'materials': materials,
        'units':     units,
    })

@login_required
def program_laying(request):
    from erp_config.models import Unit
    from master_data.models import Material
    programs  = Program.objects.filter(type='Laying').prefetch_related('steps')
    materials = Material.objects.all().order_by('name')
    units     = Unit.objects.all()
    return render(request, 'program/laying.html', {
        'programs':  programs,
        'materials': materials,
        'units':     units,
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
            date               = request.POST.get('date') or None,
            medicine           = request.POST.get('medicine', ''),
            dose_amount        = request.POST.get('dose_amount') or None,
            dose_unit          = request.POST.get('dose_unit', ''),
            dose_per           = request.POST.get('dose_per', ''),
            method             = request.POST.get('method', ''),
            remarks            = request.POST.get('remarks', ''),
            feed               = request.POST.get('feed', ''),
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
        step.date               = request.POST.get('date') or None
        step.medicine           = request.POST.get('medicine', '')
        step.dose_amount        = request.POST.get('dose_amount') or None
        step.dose_unit          = request.POST.get('dose_unit', '')
        step.dose_per           = request.POST.get('dose_per', '')
        step.method             = request.POST.get('method', '')
        step.remarks            = request.POST.get('remarks', '')
        step.feed               = request.POST.get('feed', '')
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
    from master_data.models import Material
    from flock.models import Flock
    from laying_flock.models import LayingFlock
    from django.db.models import Sum

    program = get_object_or_404(Program, pk=pk)

    if program.type == 'Growing':
        total_birds = Flock.objects.filter(status='Active').aggregate(
            Sum('current_count'))['current_count__sum'] or 0
    else:
        total_birds = LayingFlock.objects.filter(status='Active').aggregate(
            Sum('current_count'))['current_count__sum'] or 0

    material_map = {m.item_id: m.name for m in Material.objects.all()}

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = program.name[:31]

    header_font = Font(bold=True, color='FFFFFF', size=10)
    center      = Alignment(horizontal='center', vertical='center')
    left        = Alignment(horizontal='left',   vertical='center')

    blue_fill   = PatternFill(fill_type='solid', fgColor='2E75B6')
    purple_fill = PatternFill(fill_type='solid', fgColor='7030A0')
    orange_fill = PatternFill(fill_type='solid', fgColor='C55A11')
    green_fill  = PatternFill(fill_type='solid', fgColor='375623')

    # col[0..13] — must match import indices exactly
    headers = [
        ('Cycle #',                blue_fill),    # 0
        ('Age Display',            blue_fill),    # 1
        ('Date',                   blue_fill),    # 2  new
        ('Population',             blue_fill),    # 2
        ('Medicine Name',          purple_fill),  # 3  display only
        ('Medicine Item ID',       purple_fill),  # 4  used by import
        ('UoM',                    purple_fill),  # 5
        ('Dosage Rate (per Bird)', purple_fill),  # 6
        ('Total Dosage',           purple_fill),  # 7  computed, skip on import
        ('Feed Name',              orange_fill),  # 8  display only
        ('Feed Item ID',           orange_fill),  # 9  used by import
        ('Feed Rate (per Bird)',   orange_fill),  # 10
        ('Total Feed',             orange_fill),  # 11 computed, skip on import
        ('Feed Unit',              orange_fill),  # 12
        ('Remarks',                green_fill),   # 13
    ]

    for col, (header, fill) in enumerate(headers, 1):
        cell           = ws.cell(row=1, column=col, value=header)
        cell.font      = header_font
        cell.fill      = fill
        cell.alignment = center

    col_widths = [10, 16, 14, 12, 22, 16, 8, 22, 14, 22, 16, 20, 14, 12, 20]
    for col, width in enumerate(col_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width

    for row_num, step in enumerate(program.steps.all(), 2):
        age_display   = f'Day {step.day}' if step.week == 0 else f'Week {step.week}-Day {step.day}'
        medicine_name = material_map.get(step.medicine, step.medicine)
        feed_name     = material_map.get(step.feed, step.feed)
        total_dosage  = float(step.dose_amount) * total_birds if step.dose_amount else ''
        total_feed    = float(step.feed_rate_per_bird) * total_birds if step.feed_rate_per_bird else ''

        row_data = [
            step.cycle,
            age_display,
            str(step.date) if step.date else '',                             # 2
            total_birds,
            medicine_name,
            step.medicine or '',
            step.dose_unit or '',
            float(step.dose_amount) if step.dose_amount else '',
            total_dosage,
            feed_name,
            step.feed or '',
            float(step.feed_rate_per_bird) if step.feed_rate_per_bird else '',
            total_feed,
            step.feed_unit or '',
            step.remarks or '',
        ]

        for col, value in enumerate(row_data, 1):
            cell           = ws.cell(row=row_num, column=col, value=value)
            cell.alignment = left

        if row_num % 2 == 0:
            light_fill = PatternFill(fill_type='solid', fgColor='EBF3FB')
            for col in range(1, len(headers) + 1):
                ws.cell(row=row_num, column=col).fill = light_fill

    ws.freeze_panes = 'A2'

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{program.name}_{program.type}.xlsx"'
    wb.save(response)
    return response

@login_required
def import_program(request, pk):
    import openpyxl
    from master_data.models import Material

    program = get_object_or_404(Program, pk=pk)

    if request.method == 'POST' and request.FILES.get('excel_file'):
        file = request.FILES['excel_file']
        wb   = openpyxl.load_workbook(file)
        ws   = wb.active

        valid_ids = set(Material.objects.values_list('item_id', flat=True))

        program.steps.all().delete()

        imported = 0
        errors   = []

        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):
                continue

            try:
                cycle       = row[0]
                age_display = str(row[1]).strip() if row[1] not in (None, '') else ''
                date        = row[2]  # Date — new
                # row[3] = Population — skip
                # row[4] = Medicine Name (display) — skip
                medicine_id = str(row[5]).strip() if row[5] not in (None, '') else ''
                dose_unit   = str(row[6]).strip() if row[6] not in (None, '') else ''
                dose_amount = row[7]
                # row[8] = Total Dosage — skip
                # row[9] = Feed Name (display) — skip
                feed_id     = str(row[10]).strip() if row[10] not in (None, '') else ''
                feed_rate   = row[11]
                # row[12] = Total Feed — skip
                feed_unit   = str(row[13]).strip() if row[13] not in (None, '') else ''
                remarks     = str(row[14]).strip() if row[14] not in (None, '') else ''

                # validate item IDs
                if medicine_id and medicine_id not in valid_ids:
                    errors.append(f'Row {row_num}: Medicine "{medicine_id}" not found in materials — skipped')
                    continue
                if feed_id and feed_id not in valid_ids:
                    errors.append(f'Row {row_num}: Feed "{feed_id}" not found in materials — skipped')
                    continue

                # parse age display → week + day
                week = 0
                day  = 1
                if age_display.startswith('Week'):
                    parts = age_display.replace('Week ', '').split('-Day ')
                    week  = int(parts[0].strip())
                    day   = int(parts[1].strip())
                elif age_display.startswith('Day'):
                    day  = int(age_display.replace('Day ', '').strip())
                    week = 0

                ProgramStep.objects.create(
                    program            = program,
                    cycle              = int(cycle) if cycle else 1,
                    week               = week,
                    day                = day,
                    date               = date if date not in (None, '') else None,
                    medicine           = medicine_id,
                    dose_amount        = dose_amount if dose_amount not in (None, '') else None,
                    dose_unit          = dose_unit,
                    dose_per           = 'chick',
                    method             = '',
                    remarks            = remarks,
                    feed               = feed_id,
                    feed_rate_per_bird = feed_rate if feed_rate not in (None, '') else None,
                    feed_unit          = feed_unit,
                )
                imported += 1

            except Exception as e:
                errors.append(f'Row {row_num}: {str(e)}')

        if errors:
            messages.warning(request, f'Imported {imported} steps with {len(errors)} errors: {"; ".join(errors[:3])}')
        else:
            messages.success(request, f'Successfully imported {imported} steps!')

    if program.type == 'Laying':
        return redirect('program_laying')
    return redirect('program_growing')

@login_required
def view_growing(request):
    from flock.models import Flock
    from consumption.models import Consumption
    from erp_config.models import Building
    from master_data.models import Material
    from django.db.models import Sum

    programs     = Program.objects.filter(type='Growing').prefetch_related('steps')
    total_chicks = Flock.objects.filter(status='Active').aggregate(
                    Sum('current_count'))['current_count__sum'] or 0

    growing_buildings = Building.objects.filter(type='Growing').values_list('name', flat=True)
    material_map      = {m.item_id: m.name for m in Material.objects.all()}

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
            med_name = material_map.get(med, med)
            if med not in medicine_map:
                medicine_map[med] = {
                    'medicine':    med_name,
                    'dose_amount': float(step.dose_amount) if step.dose_amount else 0,
                    'dose_unit':   step.dose_unit,
                    'dose_per':    step.dose_per,
                    'required':    float(step.dose_amount) * total_chicks if step.dose_amount else 0,
                    'consumed':    consumption_totals.get(med_name, 0),
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
    from master_data.models import Material
    from django.db.models import Sum

    programs     = Program.objects.filter(type='Laying').prefetch_related('steps')
    total_chicks = LayingFlock.objects.filter(status='Active').aggregate(
                    Sum('current_count'))['current_count__sum'] or 0

    laying_buildings = Building.objects.filter(type='Laying').values_list('name', flat=True)
    material_map     = {m.item_id: m.name for m in Material.objects.all()}

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
            med_name = material_map.get(med, med)
            if med not in medicine_map:
                medicine_map[med] = {
                    'medicine':    med_name,
                    'dose_amount': float(step.dose_amount) if step.dose_amount else 0,
                    'dose_unit':   step.dose_unit,
                    'dose_per':    step.dose_per,
                    'required':    float(step.dose_amount) * total_chicks if step.dose_amount else 0,
                    'consumed':    consumption_totals.get(med_name, 0),
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