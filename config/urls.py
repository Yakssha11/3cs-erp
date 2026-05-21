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
    from django.db.models import Sum
    from datetime import date

    total_chicks  = Flock.objects.aggregate(Sum('current_count'))['current_count__sum'] or 0
    today_deaths  = Mortality.objects.filter(death_date=date.today()).aggregate(Sum('count'))['count__sum'] or 0
    total_expense = Finance.objects.filter(
                        expense_date__month=date.today().month,
                        expense_date__year=date.today().year
                    ).aggregate(Sum('amount'))['amount__sum'] or 0
    stock_items   = Stock.objects.count()
    low_stock     = Stock.objects.filter(quantity__lte=10).count()

    return render(request, 'home.html', {
        'total_chicks':  total_chicks,
        'today_deaths':  today_deaths,
        'total_expense': total_expense,
        'stock_items':   stock_items,
        'low_stock':     low_stock,
    })

@login_required
def analytics(request):
    from stock.models import Stock
    from consumption.models import Consumption
    from flock.models import Flock, Mortality
    from finance.models import Finance
    from django.db.models import Sum
    from datetime import date, timedelta

    # ── KPIs ─────────────────────────────────────────────────
    total_chicks  = Flock.objects.aggregate(Sum('start_count'))['start_count__sum'] or 0
    alive         = Flock.objects.aggregate(Sum('current_count'))['current_count__sum'] or 0
    total_deaths  = Mortality.objects.aggregate(Sum('count'))['count__sum'] or 0
    total_expense = Finance.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    stock_items   = Stock.objects.count()
    death_rate    = round((total_deaths / total_chicks * 100), 2) if total_chicks > 0 else 0

    # ── mortality last 7 days ─────────────────────────────────
    mort_labels = []
    mort_data   = []
    for i in range(6, -1, -1):
        day   = date.today() - timedelta(days=i)
        count = Mortality.objects.filter(death_date=day).aggregate(Sum('count'))['count__sum'] or 0
        mort_labels.append(day.strftime('%m/%d'))
        mort_data.append(count)

    # ── expense by nature ─────────────────────────────────────
    exp_data   = Finance.objects.values('nature').annotate(total=Sum('amount')).order_by('-total')
    exp_labels = [e['nature'] for e in exp_data]
    exp_values = [float(e['total']) for e in exp_data]

    # ── GH1 vs GH2 ───────────────────────────────────────────
    gh1_deaths = Mortality.objects.filter(growing_house='Growing House 1').aggregate(Sum('count'))['count__sum'] or 0
    gh2_deaths = Mortality.objects.filter(growing_house='Growing House 2').aggregate(Sum('count'))['count__sum'] or 0
    gh1_exp    = float(Finance.objects.filter(building='Growing House 1').aggregate(Sum('amount'))['amount__sum'] or 0)
    gh2_exp    = float(Finance.objects.filter(building='Growing House 2').aggregate(Sum('amount'))['amount__sum'] or 0)

    # ── stock levels ──────────────────────────────────────────
    stocks = Stock.objects.all().order_by('quantity')[:8]

    return render(request, 'analytics.html', {
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
    path('logout/',      auth_views.LogoutView.as_view(next_page='login'),         name='logout'),
]