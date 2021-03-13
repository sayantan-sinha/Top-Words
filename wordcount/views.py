from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import WordTree
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
import requests

# Create your views here.
def frequency(request):
    return render(request, 'wordcount/frequency.html')

def search(request):
    url = request.POST['web_url']
    try:
        word_obj = WordTree.objects.get(link=url)
        db_status = True
        print("Present in DB")
    except WordTree.DoesNotExist:
        word_obj = WordTree()
        word_obj.link = url
        words = parse_page(url)
        word_obj.store_strings(words)
        db_status = False
        print("Not present in DB")

    print(url)
    return HttpResponseRedirect(reverse('wordcount:result', args=(word_obj.id, db_status)))

def parse_page(url):
    page = requests.get(url)
    tokenizer = RegexpTokenizer(r"\w+")
    soup = BeautifulSoup(page.content)
    text = list(''.join(s.findAll(text=True)) for s in soup.findAll('p'))
    text_stream = ''.join(text)
    text_tok = tokenizer.tokenize(text_stream)
    c = Counter((x.rstrip(punctuation).lower() for x in text_tok))
    s = set(stopwords.words('english'))
    w = list(filter(lambda w: w not in s, [x[0] for x in c.most_common()]))
    return w[:10]

def result(request, payload, db_status):
    word_obj = WordTree.objects.get(pk=payload)
    return render(request, 'wordcount/result.html', {'word_obj':word_obj, 'db_status':db_status})






