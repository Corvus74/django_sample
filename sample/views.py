from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse # New import

from .dependencies import get_api_service
from api.dependencies import get_replacement_part_service
from api.schemas import ReplacementPartCreate # New import

def sample_page(request: HttpRequest):
    api_service = get_api_service()
    data = api_service.get_data()
    return render(request, 'sample.html', {'sample_data': data})

def replacement_parts_page(request: HttpRequest):
    part_service = get_replacement_part_service()
    parts = part_service.get_replacement_parts()
    # Convert Pydantic models to dicts for template rendering
    data = [part.model_dump(by_alias=True) for part in parts]
    return render(request, 'replacement_parts.html', {'parts': data})

def add_replacement_part_view(request: HttpRequest):
    part_service = get_replacement_part_service()
    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        quantity = request.POST.get('quantity')

        errors = {}
        if not name: errors['name'] = "Name is required."
        if not sku: errors['sku'] = "SKU is required."
        try:
            quantity = int(quantity)
            if quantity < 0: errors['quantity'] = "Quantity must be non-negative."
        except (ValueError, TypeError): errors['quantity'] = "Quantity must be an integer."

        if not errors:
            try:
                # Create Pydantic object for validation and service call
                part_create_data = ReplacementPartCreate(name=name, sku=sku, quantity=quantity)
                part_service.add_replacement_part(part_create_data)
                return redirect(reverse('replacement_parts_page')) # Redirect to the list view
            except Exception as e:
                errors['general'] = f"Error adding part: {e}"
        
        # If there are errors or GET request, render the form
        return render(request, 'sample/add_replacement_part.html', {'errors': errors, 'form_data': request.POST})
    
    return render(request, 'sample/add_replacement_part.html')
