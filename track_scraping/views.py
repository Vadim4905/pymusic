from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, CreateView,DetailView,FormView 
from track_scraping import forms
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse,Http404,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from celery.result import AsyncResult

from home.models import Artist,Album,Music
from home.views import GroupRequiredMixin
from .tasks import scrape_artist,my_long_task

from ytmusicapi import YTMusic



class ArtistScrapeCreateView(GroupRequiredMixin,FormView ):
    template_name = "track_scraping/scrape_artist.html"
    form_class = forms.ArtistForm
    group_required = 'admin'
   
    def form_valid(self, form):
        artist_name = form.cleaned_data['name']
        
        ytmusic = YTMusic()  
        search_results = ytmusic.search(artist_name, filter='artists')
        if not search_results:
            raise Http404("Artist wasn't found")

        task = scrape_artist.apply_async(args=[artist_name])
        # task = my_long_task.apply_async(args=[artist_name])
        url = reverse('download-progress',kwargs={'task_id': task.id})
        return redirect(url)

def download_progress(request, task_id):
    task = AsyncResult(task_id)
    task_data ={
        'id': task_id,
        'state': task.state,
        'result': task.result,
    }
    
    return render(request,"track_scraping/download_progress.html",{'task':task_data})

def task_status(request, task_id):
    task = AsyncResult(task_id)
    response_data = {
        'state': task.state,
        'result': task.result
    }
    print(response_data)
    return JsonResponse(response_data)

def start_task(request):
    task = my_long_task.delay(100)
    return render(request,"track_scraping/progress.html",{'task_id':task.id})

    


