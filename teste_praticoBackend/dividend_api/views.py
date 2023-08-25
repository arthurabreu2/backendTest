from django.http import JsonResponse
from django.db.models import Sum
from .models import Dividend


# Função para retornar os dados de dividendos com os parametros na url
def dividend_summary(request):
    symbol = request.GET.get('symbol')
    year = request.GET.get('year')

    if not symbol or not year:
        return JsonResponse({'error': 'Parâmetros obrigatórios não fornecidos.'}, status=400)

    try:
        year = int(year)
    except ValueError:
        return JsonResponse({'error': 'O ano deve ser um valor numérico.'}, status=400)

    dividends_summary = Dividend.objects.filter(symbol=symbol, date__year=year) \
                        .values('date__year') \
                        .annotate(total_dividends=Sum('amount'))

    # PARA ACESSAR A API
    # http://127.0.0.1:8000/api/dividend-summary-by-year/?symbol=PETR4.SA&year=2023


    return JsonResponse(list(dividends_summary), safe=False)
