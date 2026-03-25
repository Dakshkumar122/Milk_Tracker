from django.shortcuts import render, redirect, get_object_or_404
from .models import MilkEntry
from .forms import MilkEntryForm
import datetime
from django.contrib import messages
from django.db.models import Sum

def milk_tracker(request):
    # Get current date
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year
    
    # Get filter parameters from request
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    
    # CRITICAL FIX: Check if this is a page load vs filter action
    # If there's no filter parameter in URL OR if it's a fresh page load (no query params)
    # Then use current month/year
    is_filter_applied = request.GET.get('month') is not None or request.GET.get('year') is not None
    
    # If filter is NOT applied (fresh page load or no filter), use current month/year
    if not is_filter_applied:
        selected_month = str(current_month)
        selected_year = str(current_year)
    # If both month and year are empty strings (user selected "All Months" and "All Years")
    elif selected_month == '' and selected_year == '':
        selected_month = str(current_month)
        selected_year = str(current_year)
    # If only month is selected but year is empty
    elif selected_month and selected_month != '' and (selected_year == '' or selected_year is None):
        # Keep month filter, don't override
        pass
    # If only year is selected but month is empty
    elif selected_year and selected_year != '' and (selected_month == '' or selected_month is None):
        # Keep year filter, don't override
        pass
    
    # Base queryset
    entries = MilkEntry.objects.all()
    
    # Apply filters
    if selected_month and selected_year and selected_month != '' and selected_year != '':
        try:
            month_int = int(selected_month)
            year_int = int(selected_year)
            entries = entries.filter(
                date__month=month_int,
                date__year=year_int
            )
        except ValueError:
            pass
    elif selected_month and selected_month != '':
        try:
            month_int = int(selected_month)
            entries = entries.filter(date__month=month_int)
        except ValueError:
            pass
    elif selected_year and selected_year != '':
        try:
            year_int = int(selected_year)
            entries = entries.filter(date__year=year_int)
        except ValueError:
            pass
    
    # Calculate totals for FILTERED entries only
    total_qty = entries.aggregate(total=Sum('quantity'))['total'] or 0
    total_bill = sum(entry.total() for entry in entries)
    
    # Handle Edit and Delete
    edit_id = request.GET.get('edit_id')
    delete_id = request.GET.get('delete_id')
    
    # Handle Delete
    if delete_id:
        entry = get_object_or_404(MilkEntry, id=delete_id)
        entry.delete()
        messages.success(request, f'✅ Successfully deleted entry for {entry.date}!')
        # After delete, redirect to current month/year
        return redirect(f'/?month={current_month}&year={current_year}')
    
    edit_entry = None
    if edit_id:
        edit_entry = get_object_or_404(MilkEntry, id=edit_id)
        initial_data = {
            'date': edit_entry.date,
            'quantity': edit_entry.quantity,
        }
    else:
        initial_data = {'date': today}
    
    # Initialize form
    if request.method == 'POST':
        if edit_id:
            edit_entry = get_object_or_404(MilkEntry, id=edit_id)
            form = MilkEntryForm(request.POST, instance=edit_entry)
        else:
            form = MilkEntryForm(request.POST)
        
        if form.is_valid():
            date = form.cleaned_data.get('date')
            quantity = form.cleaned_data.get('quantity')
            
            # Validations
            if date > today:
                messages.error(request, '❌ Cannot add/edit entry for future date!')
                return redirect(f'/?month={current_month}&year={current_year}')
            
            if quantity <= 0:
                messages.error(request, '❌ Quantity must be greater than 0!')
                return redirect(f'/?month={current_month}&year={current_year}')
            
            if quantity > 1000:
                messages.error(request, '❌ Quantity is too high! Maximum 1000 liters allowed.')
                return redirect(f'/?month={current_month}&year={current_year}')
            
            # Save the entry
            obj = form.save(commit=False)
            obj.price_per_litre = 60
            obj.save()
            
            if edit_id:
                messages.success(request, f'✅ Successfully updated entry for {date}!')
            else:
                messages.success(request, f'✅ Successfully added {quantity}L milk for {date}!')
            
            # After add/edit, redirect to current month/year
            return redirect(f'/?month={current_month}&year={current_year}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'❌ {field}: {error}')
    
    else:
        if edit_id:
            form = MilkEntryForm(instance=edit_entry)
        else:
            form = MilkEntryForm(initial=initial_data)
    
    # Prepare month choices
    MONTH_CHOICES = []
    for i in range(1, 13):
        month_name = datetime.date(2000, i, 1).strftime('%B')
        MONTH_CHOICES.append((i, month_name))
    
    # Prepare year choices
    current_year_num = datetime.datetime.now().year
    YEAR_CHOICES = []
    for y in range(current_year_num - 2, current_year_num + 3):
        YEAR_CHOICES.append((y, str(y)))
    
    # Get month name for display
    month_name = ""
    if selected_month and selected_month != '':
        try:
            month_name = datetime.date(2000, int(selected_month), 1).strftime('%B')
        except:
            month_name = ""
    
    context = {
        'form': form,
        'entries': entries,
        'total_qty': total_qty,
        'total_bill': total_bill,
        'MONTH_CHOICES': MONTH_CHOICES,
        'YEAR_CHOICES': YEAR_CHOICES,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'month_name': month_name,
        'today_date': today,
        'edit_mode': edit_id is not None,
        'edit_id': edit_id,
        'current_month': current_month,
        'current_year': current_year,
    }
    
    return render(request, 'tracker/milk_tracker.html', context)