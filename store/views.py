from django.shortcuts import render, redirect, get_object_or_404
from livestock.models import Livestock
from django.contrib.auth.decorators import login_required




@login_required
def livestock_buy_now(request, pk):
    livestock = get_object_or_404(Livestock, pk=pk)
    
    # هنا ممكن تضع أي عملية شراء فعلية، أو إعادة توجيه إلى صفحة تأكيد الشراء
    return render(request, 'store/buy_now_confirmation.html', {'livestock': livestock})

