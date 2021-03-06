from django.shortcuts import render
from django.http import HttpResponse

import random
import urllib
import itertools
import simplejson as json
from datetime import datetime, timedelta
from decorator import decorator

from places.models import Place, Visit

@decorator
def jsonify(fn, request, *args, **kwargs):
    ret = fn(request, *args, **kwargs)
    retstr = json.dumps({'data': ret, 'ok': True })
    return HttpResponse(retstr, mimetype="application/json")

def total_days(td):
    return td.total_seconds() / 86400

def index(request):
    _update()
    return render(request, 'index.html')

@jsonify
def suggestions(request):

    places = Place.objects.all()
    place_stats = []
    dnow = datetime.now()
    for p in places:
        visits = filter(lambda v: v.is_relevant(), p.visit_set.all())
        if len(visits) == 0:
            continue
        
        dates = [v.date for v in visits] + [dnow]
        dates.sort()
        deltas = [v - dates[i-1] for i, v in enumerate(dates[1:], start=1)]
        cur_delta = total_days(deltas[-1])
        mean_delta = sum([total_days(d) for d in deltas]) / len(deltas)

        place_stats.append({'name': p.name, 'mean': mean_delta, 'current': cur_delta})

    # Randomize, so if there are multiple, equally good, choices, we get a different one each time.
    random.shuffle(place_stats)

    # Sort by longest time since "due" date, then by longest absolute time
    place_stats.sort(key=lambda x: round(x['current']) / round(x['mean']), reverse=True)

    return place_stats

def _update():
    # import os
    # here = os.path.dirname(os.path.realpath(__file__))
    # filename = os.path.join(here, '../test/data.txt')
    # f = open(filename)

    tr_access_token = 'OG2XGLHEC5ZMB5QBPRV3CHD0QLNPUQWSRAH55RQXTAEUIITJ'
    url = 'https://api.foursquare.com/v2/users/self/checkins?oauth_token=%s&limit=250' % tr_access_token
    f = urllib.urlopen(url)

    data_str = ''.join(f.readlines())
    f.close()
    data_arr = json.loads(data_str)

    # Sync the places
    places = [i['venue'] for i in data_arr['response']['checkins']['items']]
    place_ids = set(pl['id'] for pl in places)
    existing_places = Place.objects.filter(api_id__in=place_ids)
    existing_place_ids = set(p.api_id for p in existing_places)
    places_to_add = [p for p in places if p['id'] not in existing_place_ids]

    place_objs = {}
    for p in existing_places:
        place_objs[p.api_id] = p
    for p in places_to_add:
        
        categories = set([c['name'] for c in p['categories']])
        categories = categories.union(set(itertools.chain(*[c['parents'] for c in p['categories']])))

        if p['id'] not in place_objs and 'Food' in categories:
            place_objs[p['id']] = Place.objects.create(name=p['name'], api_id=p['id'])

    # Sync the visits
    visits = data_arr['response']['checkins']['items']
    visit_ids = set(v['id'] for v in visits)
    existing_visits = Visit.objects.filter(api_id__in=visit_ids)
    existing_visit_ids = set(v.api_id for v in existing_visits)
    visits_to_add = [v for v in visits if v['id'] not in existing_visit_ids]

    for v in visits_to_add:
        d = datetime.fromtimestamp(v['createdAt'])
        if v['venue']['id'] in place_objs:
            place_objs[v['venue']['id']].visit_set.create(date=d, api_id=v['id'])
        
    return { 'places_created': len(places_to_add), 'visits_created': len(visits_to_add)}
    
