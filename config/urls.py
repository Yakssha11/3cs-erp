from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    from stock.models import Stock
    from flock.models import Flock, Mortality
    from finance.models import Finance
    from laying_flock.models import LayingFlock, LayingMortality
    from egg_production.models import EggProduction
    from laying_finance.models import LayingFinance
    from django.db.models import Sum, Avg
    from datetime import date

    today = date.today()

    # ── Growing KPIs ──────────────────────────────────────────
    total_chicks  = Flock.objects.aggregate(Sum('current_count'))['current_count__sum'] or 0
    today_deaths  = Mortality.objects.filter(death_date=today).aggregate(Sum('count'))['count__sum'] or 0
    total_expense = Finance.objects.filter(
                        expense_date__month=today.month,
                        expense_date__year=today.year
                    ).aggregate(Sum('amount'))['amount__sum'] or 0
    stock_items   = Stock.objects.count()
    low_stock     = Stock.objects.filter(quantity__lte=10).count()

    # ── Laying KPIs ───────────────────────────────────────────
    laying_hens      = LayingFlock.objects.aggregate(Sum('current_count'))['current_count__sum'] or 0
    eggs_today       = EggProduction.objects.filter(collection_date=today).aggregate(Sum('good_eggs'))['good_eggs__sum'] or 0
    avg_rate         = EggProduction.objects.aggregate(avg=Avg('production_rate'))['avg'] or 0
    avg_rate         = round(float(avg_rate), 2)
    total_revenue    = float(EggProduction.objects.aggregate(Sum('total_revenue'))['total_revenue__sum'] or 0)
    laying_expenses  = float(LayingFinance.objects.aggregate(Sum('amount'))['amount__sum'] or 0)
    net_profit       = total_revenue - laying_expenses

    return render(request, 'home.html', {
        # growing
        'total_chicks':  total_chicks,
        'today_deaths':  today_deaths,
        'total_expense': total_expense,
        'stock_items':   stock_items,
        'low_stock':     low_stock,
        # laying
        'laying_hens':    laying_hens,
        'eggs_today':     eggs_today,
        'avg_rate':       avg_rate,
        'total_revenue':  total_revenue,
        'laying_expenses': laying_expenses,
        'net_profit':     net_profit,
    })

@login_required
def analytics(request):
    from stock.models import Stock
    from flock.models import Flock, Mortality
    from finance.models import Finance
    from laying_flock.models import LayingFlock, LayingMortality
    from egg_production.models import EggProduction
    from laying_finance.models import LayingFinance
    from django.db.models import Sum, Avg
    from datetime import date, timedelta

    # ── GROWING KPIs ─────────────────────────────────────────
    total_chicks  = Flock.objects.aggregate(Sum('start_count'))['start_count__sum'] or 0
    alive         = Flock.objects.aggregate(Sum('current_count'))['current_count__sum'] or 0
    total_deaths  = Mortality.objects.aggregate(Sum('count'))['count__sum'] or 0
    total_expense = Finance.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    stock_items   = Stock.objects.count()
    death_rate    = round((total_deaths / total_chicks * 100), 2) if total_chicks > 0 else 0

    # ── GROWING mortality last 7 days ─────────────────────────
    mort_labels = []
    mort_data   = []
    for i in range(6, -1, -1):
        day   = date.today() - timedelta(days=i)
        count = Mortality.objects.filter(death_date=day).aggregate(Sum('count'))['count__sum'] or 0
        mort_labels.append(day.strftime('%m/%d'))
        mort_data.append(count)

    # ── GROWING expense by nature ─────────────────────────────
    exp_data   = Finance.objects.values('nature').annotate(total=Sum('amount')).order_by('-total')
    exp_labels = [e['nature'] for e in exp_data]
    exp_values = [float(e['total']) for e in exp_data]

    # ── GROWING GH comparison ─────────────────────────────────
    gh1_deaths = Mortality.objects.filter(growing_house='Growing House 1').aggregate(Sum('count'))['count__sum'] or 0
    gh2_deaths = Mortality.objects.filter(growing_house='Growing House 2').aggregate(Sum('count'))['count__sum'] or 0
    gh1_exp    = float(Finance.objects.filter(building='Growing House 1').aggregate(Sum('amount'))['amount__sum'] or 0)
    gh2_exp    = float(Finance.objects.filter(building='Growing House 2').aggregate(Sum('amount'))['amount__sum'] or 0)

    # ── GROWING stock levels ──────────────────────────────────
    stocks = Stock.objects.all().order_by('quantity')[:8]

    # ── LAYING KPIs ───────────────────────────────────────────
    laying_hens      = LayingFlock.objects.aggregate(Sum('current_count'))['current_count__sum'] or 0
    laying_deaths    = LayingMortality.objects.aggregate(Sum('count'))['count__sum'] or 0
    total_good_eggs  = EggProduction.objects.aggregate(Sum('good_eggs'))['good_eggs__sum'] or 0
    total_revenue    = float(EggProduction.objects.aggregate(Sum('total_revenue'))['total_revenue__sum'] or 0)
    laying_expenses  = float(LayingFinance.objects.aggregate(Sum('amount'))['amount__sum'] or 0)
    net_profit       = total_revenue - laying_expenses
    avg_rate         = EggProduction.objects.aggregate(
                        avg=Avg('production_rate')
                    )['avg'] or 0
    avg_rate         = round(float(avg_rate), 2)

    # ── LAYING egg production last 7 days ─────────────────────
    egg_labels = []
    egg_data   = []
    for i in range(6, -1, -1):
        day   = date.today() - timedelta(days=i)
        count = EggProduction.objects.filter(collection_date=day).aggregate(Sum('good_eggs'))['good_eggs__sum'] or 0
        egg_labels.append(day.strftime('%m/%d'))
        egg_data.append(count)

    # ── LAYING RTL1 vs RTL2 ───────────────────────────────────
    rtl1_eggs = EggProduction.objects.filter(building='RTL Building 1').aggregate(Sum('good_eggs'))['good_eggs__sum'] or 0
    rtl2_eggs = EggProduction.objects.filter(building='RTL Building 2').aggregate(Sum('good_eggs'))['good_eggs__sum'] or 0
    rtl1_exp  = float(LayingFinance.objects.filter(building='RTL Building 1').aggregate(Sum('amount'))['amount__sum'] or 0)
    rtl2_exp  = float(LayingFinance.objects.filter(building='RTL Building 2').aggregate(Sum('amount'))['amount__sum'] or 0)

    return render(request, 'analytics.html', {
        # growing
        'total_chicks':  total_chicks,
        'alive':         alive,
        'total_deaths':  total_deaths,
        'death_rate':    death_rate,
        'total_expense': total_expense,
        'stock_items':   stock_items,
        'mort_labels':   mort_labels,
        'mort_data':     mort_data,
        'exp_labels':    exp_labels,
        'exp_values':    exp_values,
        'gh1_deaths':    gh1_deaths,
        'gh2_deaths':    gh2_deaths,
        'gh1_exp':       gh1_exp,
        'gh2_exp':       gh2_exp,
        'stocks':        stocks,
        # laying
        'laying_hens':    laying_hens,
        'laying_deaths':  laying_deaths,
        'total_good_eggs': total_good_eggs,
        'total_revenue':  total_revenue,
        'laying_expenses': laying_expenses,
        'net_profit':     net_profit,
        'avg_rate':       avg_rate,
        'egg_labels':     egg_labels,
        'egg_data':       egg_data,
        'rtl1_eggs':      rtl1_eggs,
        'rtl2_eggs':      rtl2_eggs,
        'rtl1_exp':       rtl1_exp,
        'rtl2_exp':       rtl2_exp,
    })

urlpatterns = [
    path('admin/',       admin.site.urls),
    path('',             home,            name='home'),
    path('stock/',       include('stock.urls')),
    path('consumption/', include('consumption.urls')),
    path('flock/',       include('flock.urls')),
    path('finance/',     include('finance.urls')),
    path('analytics/',   analytics,       name='analytics'),
    path('login/',       auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',      auth_views.LogoutView.as_view(next_page='/login/'),        name='logout'),
    path('config/', include('erp_config.urls')),
    path('laying/flock/', include('laying_flock.urls')),
    path('laying/eggs/', include('egg_production.urls')),
    path('laying/finance/', include('laying_finance.urls')),
    path('laying/finance/', include('laying_finance.urls')),
    path('program/',        include('program.urls')),
    path('masterdata/',     include('master_data.urls')),
    path('sales/',          include('sales.urls')),
    path('chicken/',        include('chicken_production.urls')),
]