from django.shortcuts import render, redirect
from markdown2 import Markdown
from django import forms
import random

from . import util



class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Page Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={"placeholder": "Enter Page Content using markdown2 language"}))

class EditForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), "data" : util.list_entries()})


def entry(request, title):
    md = util.get_entry(title)

    if md != None:
        HTML = Markdown().convert(md)
        return render(request, "encyclopedia/entry.html", {"title": title, "entry": HTML,"data" : util.list_entries()})
    else:
        return render(request, "encyclopedia/error.html", {"title": title, "data" : util.list_entries()})


def search(request):
    if request.method == "POST":
        title = request.POST['find']
        md = util.get_entry(title)
        if md != None:
            HTML = Markdown().convert(md)
            return render(request, "encyclopedia/entry.html", {"title": title, "entry": HTML,"data" : util.list_entries()})
        else:
            return render(request, "encyclopedia/error.html", {"title": title, "data" : util.list_entries()})
    else:
        return redirect('index')


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {"create_form": CreateForm(), "data" : util.list_entries()})

    elif request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
        else:
            return redirect('index')

        bomb = False
        if util.get_entry(title):
            bomb = True
            md = util.get_entry(title)
            HTML = Markdown().convert(md)
            return render(request, "encyclopedia/entry.html", {"title": title, "entry": HTML, "data" : util.list_entries(), 'bomb': bomb})
        else:
            util.save_entry(title, text)
            md = util.get_entry(title)
            HTML = Markdown().convert(md)
            return render(request, "encyclopedia/entry.html", {"title": title, "entry": HTML, "data" : util.list_entries(), 'bomb': bomb})


def edit(request, title):
    if request.method == "GET":
        text = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "edit_form": EditForm(initial={'text':text}), "data" : util.list_entries()})

    elif request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            util.save_entry(title, text)
            md = util.get_entry(title)
            HTML = Markdown().convert(md)
            return render(request, "encyclopedia/entry.html", {"title": title, "entry": HTML, "data" : util.list_entries()})


def random_title(request):
    titles = util.list_entries()
    title = random.choice(titles)

    md = util.get_entry(title)
    HTML = Markdown().convert(md)
    return render(request, "encyclopedia/entry.html", {"title": title, "entry": HTML, "data" : util.list_entries()})