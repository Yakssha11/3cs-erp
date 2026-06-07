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