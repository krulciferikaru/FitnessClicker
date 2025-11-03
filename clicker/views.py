from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# In-memory game state
game_state = {
    'clicks': 0,
    'clicks_per_click': 1,
    'upgrades': {}, 
    'notifications': []
}

# Upgrades list
UPGRADES = [
    {'name': 'Yoga Mat', 'base_cost': 25, 'multiplier': 2},
    {'name': 'Jump Rope', 'base_cost': 50, 'multiplier': 4},
    {'name': 'Dumbbells', 'base_cost': 100, 'multiplier': 8},
    {'name': 'Kettlebell', 'base_cost': 200, 'multiplier': 16},
    {'name': 'Barbell', 'base_cost': 400, 'multiplier': 32},
]

def welcome_view(request):
    return render(request, 'welcome.html')

def game_view(request):
    # Calculate upgrades with level and lock state
    upgrades = []
    for i, u in enumerate(UPGRADES):
        level = game_state['upgrades'].get(u['name'], 0)
        # Locked if previous upgrade not purchased and not first
        locked = False
        if i > 0 and game_state['upgrades'].get(UPGRADES[i-1]['name'], 0) == 0:
            locked = True
        upgrades.append({**u, 'level': level, 'locked': locked, 'cost': int(u['base_cost'] * (1.5 ** level))})

    context = {
        'clicks': game_state['clicks'],
        'clicks_per_click': game_state['clicks_per_click'],
        'upgrades': upgrades,
        'notifications': game_state['notifications'][-5:],
    }
    return render(request, 'index.html', context)

@csrf_exempt
@require_POST
def click(request):
    game_state['clicks'] += game_state['clicks_per_click']
    return JsonResponse({'clicks': game_state['clicks'], 'clicks_per_click': game_state['clicks_per_click']})

@csrf_exempt
@require_POST
def purchase_upgrade(request):
    data = json.loads(request.body)
    upgrade_name = data.get('upgrade_name')

    upgrade = next((u for u in UPGRADES if u['name'] == upgrade_name), None)
    if not upgrade:
        return JsonResponse({'error': 'Upgrade not found'}, status=400)

    # Check previous upgrade for lock
    idx = UPGRADES.index(upgrade)
    if idx > 0:
        prev = UPGRADES[idx-1]['name']
        if game_state['upgrades'].get(prev, 0) == 0:
            return JsonResponse({'error': f"{upgrade_name} is locked. Purchase previous upgrade first."}, status=400)

    level = game_state['upgrades'].get(upgrade_name, 0)
    cost = int(upgrade['base_cost'] * (1.5 ** level))
    if game_state['clicks'] < cost:
        return JsonResponse({'error': 'Not enough clicks'}, status=400)

    # Purchase upgrade
    game_state['clicks'] -= cost
    game_state['clicks_per_click'] += upgrade['multiplier']
    game_state['upgrades'][upgrade_name] = level + 1
    game_state['notifications'].append(f"✅ {upgrade_name} Level {level + 1} purchased!")

    next_cost = int(upgrade['base_cost'] * (1.5 ** (level + 1)))

    return JsonResponse({
        'clicks': game_state['clicks'],
        'clicks_per_click': game_state['clicks_per_click'],
        'upgrade': upgrade_name,
        'level': level + 1,
        'next_cost': next_cost,
        'notifications': game_state['notifications'][-1:]
    })

@csrf_exempt
def reset(request):
    game_state['clicks'] = 0
    game_state['clicks_per_click'] = 1
    game_state['upgrades'] = {}
    game_state['notifications'] = []
    return JsonResponse({'clicks': 0, 'clicks_per_click': 1})

@csrf_exempt
def prestige(request):
    # Can only prestige if all upgrades purchased
    if any(game_state['upgrades'].get(u['name'], 0) == 0 for u in UPGRADES):
        return JsonResponse({'error': 'Purchase all upgrades before prestiging.'}, status=400)

    game_state['clicks'] = 0
    game_state['clicks_per_click'] = int(game_state['clicks_per_click'] * 1.1)
    game_state['upgrades'] = {}
    game_state['notifications'].append("✨ Prestige activated! Click power increased!")
    return JsonResponse({
        'clicks': game_state['clicks'],
        'clicks_per_click': game_state['clicks_per_click'],
        'notifications': game_state['notifications'][-1:]
    })
