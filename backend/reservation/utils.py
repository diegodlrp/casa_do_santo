from django.utils import timezone
from .models import ReservationEditToken
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from .models import DailyPrice, Discount

def create_one_time_link(request, reservation):
    """
    Genera un token para editar una vez la reserva
    Solo permite modificar la reserva asociada
    """

    # creamos el token
    token, created = ReservationEditToken.objects.get_or_create(reservation=reservation)

    # If the token already existed, we'll refresh it to ensure it's not expired or used.
    # This makes the button "re-send a new link" if one was sent before.
    if not created:
        token.created_at = timezone.now()
        token.used = False
        token.save()

    return token

def get_reservation_price(request, data):
    """
    Calculates the total reservation price based on daily rates and applies the best discount.
    """
    check_in_str = data.get("checkInDate", "")
    check_out_str = data.get("checkOutDate", "")
    base_price = 0
    total_price = 0
    max_reduction = 0
    # 1. Validate and Parse Input Dates
    # ------------------------------------
    if not check_in_str or not check_out_str:
        # Or handle as an error, e.g., return JsonResponse({'error': 'Dates are required'}, status=400)
        return {
            "base_price": base_price,
            "total_price": total_price,
            "max_reduction": max_reduction
        }
    try:
        # Assuming dates are in 'YYYY-MM-DD' format
        start_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()
    except ValueError:
        # Handle invalid date format
        return {
            "base_price": base_price,
            "total_price": total_price,
            "max_reduction": max_reduction
        }

    if start_date >= end_date:
        return {
            "base_price": base_price,
            "total_price": total_price,
            "max_reduction": max_reduction
        }

    # 2. Calculate the Total Base Price
    # ------------------------------------
    # Get the sum of prices for all days from check-in up to (but not including) check-out.
    price_query = DailyPrice.objects.filter(
        date__gte=start_date,
        date__lt=end_date
    ).aggregate(total=Sum('price'))

    base_price = price_query['total'] or Decimal('0.00')

    # If no prices were found for the date range, there's nothing more to do.
    if base_price <= 0:
        return {
            "base_price": base_price,
            "total_price": total_price,
            "max_reduction": max_reduction
        }
    
    # 3. Find and Apply the Best Discount
    # ------------------------------------
    num_days = (end_date - start_date).days

    # Find all discounts that are applicable for this length of stay.
    applicable_discounts = Discount.objects.filter(days_number__lte=num_days)

    if not applicable_discounts.exists():
        return {
            "base_price": base_price,
            "total_price": total_price,
            "max_reduction": max_reduction
        }

    max_reduction = Decimal('0.00')

    # Loop through the applicable discounts to find the biggest price reduction.
    for discount in applicable_discounts:
        current_reduction = Decimal('0.00')
        if discount.percentage:
            # It's a percentage, so calculate the reduction amount.
            # We divide by 100 to convert percentage to a decimal factor.
            current_reduction = base_price * (discount.discount / Decimal('100.00'))
        else:
            # It's a fixed value.
            current_reduction = discount.discount

        # Keep track of the largest reduction found so far.
        if current_reduction > max_reduction:
            max_reduction = current_reduction
            
    # 4. Calculate and Return the Final Price
    # ------------------------------------
    total_price = base_price - max_reduction

    return {
            "base_price": base_price,
            "total_price": total_price,
            "max_reduction": max_reduction
        }