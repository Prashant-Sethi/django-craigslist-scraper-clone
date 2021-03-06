import requests
from requests.compat import quote_plus
from django.shortcuts import render
from .models import Search

from bs4 import BeautifulSoup

# Create your views here.

BASE_CRAIGSLIST_URL = 'https://delhi.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_titles = soup.find_all('li', {'class': 'result-row'})
    post_data_list = []
    for post in post_titles:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        post_data_list.append({
            'post_title': post_title,
            'post_url': post_url,
            'post_image_url': post_image_url
        })
    context = {
        'search': search,
        'data': post_data_list
    }
    return render(request, 'my_app/new_search.html', context)