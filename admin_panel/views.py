from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from users.models import CustomUser, SellerRequest
from livestock.models import Livestock
from django.contrib import messages

@staff_member_required
def dashboard_view(request):
    total_sellers = CustomUser.objects.filter(role='seller').count()
    total_buyers = CustomUser.objects.filter(role='buyer').count()
    total_products = Livestock.objects.count()

    context = {
        'total_sellers': total_sellers,
        'total_buyers': total_buyers,
        'total_products': total_products,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@staff_member_required
def seller_list_view(request):
    sellers = CustomUser.objects.filter(role='seller', is_active=True)
    total_sellers = sellers.count()
    total_buyers = CustomUser.objects.filter(role='buyer').count()
    total_products = Livestock.objects.count()

    return render(request, 'admin_panel/sellers_list.html', {
        'sellers': sellers,
        'total_sellers': total_sellers,
        'total_buyers': total_buyers,
        'total_products': total_products,
        'active_tab': 'active'
    })

@staff_member_required
def suspended_sellers_view(request):
    # البائعين المعلقين مؤقتًا (لا يزالون بائعين، لكن حسابهم غير نشط)
    suspended_sellers = CustomUser.objects.filter(role='seller', is_active=False)
    # المستخدمين الذين تمت إزالة عضويتهم كبائعين (كانوا بائعين ولكن الآن زبائن)
    removed_sellers = CustomUser.objects.filter(role='buyer', was_seller=True, is_active=True)

    total_sellers = CustomUser.objects.filter(role='seller').count()
    total_suspended_sellers = suspended_sellers.count()
    total_removed_sellers = removed_sellers.count()
    total_buyers = CustomUser.objects.filter(role='buyer').count()
    total_products = Livestock.objects.count()

    return render(request, 'admin_panel/suspended_sellers.html', {
        'suspended_sellers': suspended_sellers,
        'removed_sellers': removed_sellers,
        'total_sellers': total_sellers,
        'total_suspended_sellers': total_suspended_sellers,
        'total_removed_sellers': total_removed_sellers,
        'total_buyers': total_buyers,
        'total_products': total_products,
        'active_tab': 'suspended'
    })

@staff_member_required
def toggle_seller_status(request, seller_id):
    seller = get_object_or_404(CustomUser, id=seller_id)
    if seller.role == 'seller':
        seller.is_active = not seller.is_active
        seller.save()
        status = "مفعل" if seller.is_active else "معلق"
        messages.success(request, f'تم تغيير حالة البائع {seller.username} إلى {status}.')
    return redirect('admin_suspended_sellers')

@staff_member_required
def restore_seller_status(request, seller_id):
    user = get_object_or_404(CustomUser, id=seller_id)
    if user.role == 'buyer' and user.was_seller:
        user.role = 'seller'
        user.is_active = True
        user.was_seller = False  # إعادة تفعيل عضويته كبائع
        user.save()
        messages.success(request, f'تمت إعادة العضوية للبائع {user.username} بنجاح.')
    else:
        messages.error(request, 'هذا المستخدم ليس مؤهلاً لإعادة العضوية.')
    
    return redirect('admin_suspended_sellers')

@staff_member_required
def reactivate_seller_status(request, seller_id):
    user = get_object_or_404(CustomUser, id=seller_id)
    if user.role == 'seller' and not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, f'تم فك التعليق للبائع {user.username} بنجاح.')
    else:
        messages.error(request, 'هذا المستخدم ليس معلقاً أو ليس مؤهلاً.')
    
    return redirect('admin_suspended_sellers')

@staff_member_required
def remove_seller_status(request, seller_id):
    user = get_object_or_404(CustomUser, id=seller_id)
    if user.role == 'seller':
        user.role = 'buyer'
        user.was_seller = True  # ✅ حفظ أنه كان بائعًا
        user.is_active = True  # يبقى نشطًا كزبون
        user.save()
        messages.success(request, f'تمت إزالة عضوية البائع {user.username} وتحويله إلى زبون.')
    return redirect('admin_sellers')

@staff_member_required
def pending_sellers_view(request):
    pending_sellers = SellerRequest.objects.filter(is_reviewed=False)
    total_sellers = CustomUser.objects.filter(role='seller').count()
    total_buyers = CustomUser.objects.filter(role='buyer').count()
    total_products = Livestock.objects.count()

    return render(request, 'admin_panel/pending_sellers.html', {
        'pending_sellers': pending_sellers,
        'total_sellers': total_sellers,
        'total_buyers': total_buyers,
        'total_products': total_products,
    })

@staff_member_required
def seller_requests_view(request):
    requests = SellerRequest.objects.filter(is_reviewed=False)
    total_sellers = CustomUser.objects.filter(role='seller').count()
    total_buyers = CustomUser.objects.filter(role='buyer').count()
    total_products = Livestock.objects.count()

    return render(request, 'admin_panel/seller_requests.html', {
        'requests': requests,
        'total_sellers': total_sellers,
        'total_buyers': total_buyers,
        'total_products': total_products,
    })

@staff_member_required
def approve_seller_request(request, request_id):
    seller_request = get_object_or_404(SellerRequest, id=request_id)
    user = seller_request.user
    user.role = 'seller'
    user.is_active = True
    user.was_seller = False  # ✅ تأكيد أن المستخدم أصبح بائعًا مرة أخرى
    user.save()

    seller_request.is_reviewed = True
    seller_request.save()

    messages.success(request, f'تمت الموافقة على طلب البائع {user.username} بنجاح.')
    return redirect('admin_seller_requests')
