from django.shortcuts import render


def example_view(request):
    return render(request, 'garpix_cloudpayments/index.html')
