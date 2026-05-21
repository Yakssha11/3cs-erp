from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EggPriceConfig
from datetime import date

@login_required
def config_view(request):
    # get current price
    current_price = EggPriceConfig.objects.first()
    price_history = EggPriceConfig.objects.all().order_by('-effective_date')

    return render(request, 'erp_config/config.html', {
        'current_price': current_price,
        'price_history': price_history,
    })

@login_required
def config_save(request):
    if request.method == 'POST':
        price = request.POST.get('price_per_egg')
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

    return redirect('config')
