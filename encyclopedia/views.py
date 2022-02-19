from xml.dom.minidom import Document
from django.shortcuts import render

from . import util

from markdown2 import Markdown

import random
import requests

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    # Check to see if the .md file exists
    print("inside wiki")
    mdfile = util.get_entry(name)
    # If not an md entry, return error page
    if(mdfile == None):
        return render(request, "encyclopedia/apology.html")
    # convert .md file to html
    markdowner = Markdown()
    html = markdowner.convert(mdfile)
    with open(f'encyclopedia/templates/html/{name}.html', 'w') as f:
        header = """{% extends "encyclopedia/layout.html" %}
                        {% block title %}
                            Wiki
                        {% endblock %}
                    {% block body %}"""
        f.write(header)
        f.write(html)
        print("we in baby")
        print(name)
        f.write(f"""<a href="/edit/{name}">Edit Page</a>""")
        f.write("{% endblock %}")

    return render(request, f"html/{name}.html")

def search(request):
    q = request.GET['q']
    mdfile = util.get_entry(q)

    # If not an md entry, provide search results page with substring entries
    if(mdfile == None):
        similar_entries = []
        listmd = util.list_entries()

        # Adding similar entries to a list
        for i in listmd:
            if q in i:
                similar_entries.append(i)
        
        if (len(similar_entries) == 0):
            return render(request, "encyclopedia/apology.html")

        return render(request, "encyclopedia/results.html",{
            "similar_entries" : similar_entries
        })

    # else section: convert .md file to html
    markdowner = Markdown()
    html = markdowner.convert(mdfile)
    print("about to go in")
    with open(f'encyclopedia/templates/html/{q}.html', 'w') as f:
        header = """{% extends "encyclopedia/layout.html" %}
                        {% block title %}
                            Wiki
                        {% endblock %}
                    {% block body %}"""
        f.write(header)
        f.write(html)
        f.write(f"""<a href="/edit/{q}">Edit Page</a>""")
        print("we in baby")
        f.write("{% endblock %}")

    return render(request, f"html/{q}.html")


def create(request):
    if request.method == "POST":
        
        # store title in a variable 
        title = request.POST['title']
        content = request.POST['content']
        
        # Check to see if title is already an entry
        mdfile = util.get_entry(title)

        # If entry is already created, alert user
        if(mdfile != None):
            # somehow alert the user here
            pass
            
        #else we want to create the form 
        util.save_entry(title, content)
        
        #redirecting user to the newly created page
        mdfile = util.get_entry(title)

        markdowner = Markdown()
        html = markdowner.convert(mdfile)
        with open(f'encyclopedia/templates/html/{title}.html', 'w') as f:
            header = """{% extends "encyclopedia/layout.html" %}
                            {% block title %}
                                Wiki
                            {% endblock %}
                        {% block body %}"""
            f.write(header)
            f.write(html)
            f.write(f"""<a href="/edit/{title}">Edit Page</a>""")
            f.write("{% endblock %}")

        return render(request, f"html/{title}.html")

    else:
        return render(request, "encyclopedia/create.html")

def random_page(request):
    listmd = util.list_entries()
    listsize = len(listmd)
    num = random.randrange(0,listsize-1)
    selected = listmd[num]
    return render(request, f"html/{selected}.html")

def edit(request, name):
    if request.method == "POST":
        pass

    content = util.get_entry(name)

    return render(request, "encyclopedia/edit.html", {
        "title": name,
        "content": content
    })
