from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    t = loader.get_template('places/index.html')
    c = Context({ 'name': 'Red Stripe' })
    return HttpResponse(t.render(c))

def update(request):
    return 'Updated!'
    
