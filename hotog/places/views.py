from django.shortcuts import render_to_response
from django.http import HttpResponse

import urllib
import simplejson as json
import datetime

from places.models import Place, Visit

def index(request):
    return render_to_response('places/index.html', { 'name': 'Red Stripe' })

def update(request, live=False):
    # f = open('test/data.txt')

    tr_access_token = 'OG2XGLHEC5ZMB5QBPRV3CHD0QLNPUQWSRAH55RQXTAEUIITJ'
    url = 'https://api.foursquare.com/v2/users/self/checkins?oauth_token=%s' % tr_access_token
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
        place_objs[p['id']] = Place.objects.create(name=p['name'], api_id=p['id'])

    # Sync the visits
    visits = data_arr['response']['checkins']['items']
    visit_ids = set(v['id'] for v in visits)
    existing_visits = Visit.objects.filter(api_id__in=visit_ids)
    existing_visit_ids = set(v.api_id for v in existing_visits)
    visits_to_add = [v for v in visits if v['id'] not in existing_visit_ids]

    for v in visits_to_add:
        date = datetime.datetime.fromtimestamp(v['createdAt'])
        place_objs[v['venue']['id']].visit_set.create(date=date, api_id=v['id'])
        
    ret = { 'places_created': len(places_to_add), 'visits_created': len(visits_to_add)}
    return HttpResponse(json.dumps(ret), mimetype="application/json")
    
