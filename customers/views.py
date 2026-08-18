from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .forms import CustomerForm

@staff_member_required
@require_POST
@csrf_protect
def add_customer_ajax(request):
    form = CustomerForm(request.POST, request.FILES)
    if form.is_valid():
        customer = form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Customer added successfully!',
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'full_name': customer.full_name,
                'phone_number': customer.phone_number,
                'address': customer.address,
                'photo_url': customer.photo.url if customer.photo else None,
                'created_at': customer.created_at.strftime('%b %d, %Y'),
            }
        })
    else:
        errors = {field: error_list[0] for field, error_list in form.errors.items()}
        return JsonResponse({
            'status': 'error',
            'errors': errors
        }, status=400)
