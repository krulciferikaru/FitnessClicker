from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# In-memory storage (replace with database models in production)
game_state = {
    'clicks': 0,
    'clicks_per_click': 1,
    'upgrades_purchased': []
}

# Define upgrade tiers
UPGRADES = [
    {'name': 'Yoga Mat', 'cost': 25, 'multiplier': 2, 'icon': ''},
    {'name': 'Jump Rope', 'cost': 50, 'multiplier': 4},
    {'name': 'Dumbbells', 'cost': 100, 'multiplier': 8},
    {'name': 'Kettlebell', 'cost': 200, 'multiplier': 16},
    {'name': 'Barbell', 'cost': 400, 'multiplier': 32},
    {'name': 'Power Rack', 'cost': 800, 'multiplier': 64},
]

def game_view(request):
    """Render the main game page"""
    # Calculate available upgrades
    available_upgrades = []
    for upgrade in UPGRADES:
        if upgrade['name'] not in game_state['upgrades_purchased']:
            available_upgrades.append(upgrade)
    
    context = {
        'clicks': game_state['clicks'],
        'clicks_per_click': game_state['clicks_per_click'],
        'upgrades': available_upgrades,
        'purchased_upgrades': game_state['upgrades_purchased']
    }
    return render(request, 'game.html', context)

@csrf_exempt
@require_POST
def click(request):
    """Handle click events and update the counter"""
    game_state['clicks'] += game_state['clicks_per_click']
    
    # Check for available upgrades
    available_upgrades = []
    for upgrade in UPGRADES:
        if upgrade['name'] not in game_state['upgrades_purchased'] and game_state['clicks'] >= upgrade['cost']:
            available_upgrades.append(upgrade)
    
    return JsonResponse({
        'clicks': game_state['clicks'],
        'clicks_per_click': game_state['clicks_per_click'],
        'available_upgrades': available_upgrades
    })

def reset(request):
    """Reset the game counter"""
    game_state['clicks'] = 0
    game_state['clicks_per_click'] = 1
    game_state['upgrades_purchased'] = []
    return JsonResponse({
        'clicks': game_state['clicks'],
        'clicks_per_click': game_state['clicks_per_click']
    })

@csrf_exempt
@require_POST
def purchase_upgrade(request):
    """Purchase an upgrade"""
    data = json.loads(request.body)
    upgrade_name = data.get('upgrade_name')
    
    # Find the upgrade
    upgrade = next((u for u in UPGRADES if u['name'] == upgrade_name), None)
    
    if not upgrade:
        return JsonResponse({'error': 'Upgrade not found'}, status=400)
    
    # Check if already purchased
    if upgrade_name in game_state['upgrades_purchased']:
        return JsonResponse({'error': 'Already purchased'}, status=400)
    
    # Check if user has enough clicks
    if game_state['clicks'] < upgrade['cost']:
        return JsonResponse({'error': 'Not enough clicks'}, status=400)
    
    # Purchase the upgrade
    game_state['clicks'] -= upgrade['cost']
    game_state['clicks_per_click'] += upgrade['multiplier']
    game_state['upgrades_purchased'].append(upgrade_name)
    
    return JsonResponse({
        'clicks': game_state['clicks'],
        'clicks_per_click': game_state['clicks_per_click'],
        'purchased': upgrade_name
    })