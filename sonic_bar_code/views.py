from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
import datetime
from   django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from models import sound
import re
from audio import *
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()

#class UploadFileForm(forms.Form):
#    file = forms.FileField(
#        label='Select a file',
#        help_text='max. 42 megabytes'
#    )

target = 20000
base = 10
tolerance = 500


def home(request):
    return render(request, 'home.html', {"message": "Whisper"},
        )


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print 'about to check if valid', request.FILES

        url = handle_uploaded_file(request.FILES['userfile'])
        return HttpResponse(url)
        #return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()

    return HttpResponse('err')
#    return render_to_response('upload.html',
#            {'form': form},
#            context_instance=RequestContext(request))

@csrf_exempt
def handle_uploaded_file(f):

    print 'handling uploaded file ', f

    #saves file as caf
    name = 'C:\Users\Aran\PycharmProjects/blackmagic\sonic_bar_code\static\%s' % f
    with open(name,  'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    name = convert(name)


    returnkey = find_freq(name, target, tolerance)
    print "This is the key decoded: " + returnkey


    return match(returnkey)


def home_error(request):
    print 'im going to home error'
    return render_to_response('home.html',
    {'message': 'Not a valid url. Try again: '},
    context_instance=RequestContext(request))

def generate_view(request):
    print base
    url = ''
    if ('url' in request.GET) and request.GET['url'].strip():
        url = request.GET['url']
        #START ARAN
        p = re.compile('[a-zA-Z0-9\-\.]+\.(com|org|net|mil|edu|COM|ORG|NET|MIL|EDU)')
        if p.match(url):
        #if True:
            p=re.compile('^https?://')
            if not p.match(url):
                url = "http://"+url
            p=re.compile('^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            if not p.match(url):
                return home_error(request)

        else:
            return home_error(request)

    else:
        return home_error(request)



        #END ARAN


    #create sound and add to database

    filename = "%d.wav" %  (int(sound.objects.count()) + 1)

    while(True):
        key = generate("C:\Users\Aran\PycharmProjects/blackmagic\sonic_bar_code\static/%s" % filename, target, base)
        if check_if_same(key):
            break


    new_sound = sound(data= key, last_name = url)
    new_sound.save()  # Overrides the previous blog with ID=3!

    return render_to_response('generate.html',
        {'url': request.GET['url'], 'fname' : filename},
        context_instance=RequestContext(request))

def view_past(request, id):
    url = sound.objects.get(pk = id)
    return render_to_response('generate.html',
        {'url': url, 'fname' : '%s.wav' % id},
        context_instance=RequestContext(request))
