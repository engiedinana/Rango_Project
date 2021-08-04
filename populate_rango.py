import os
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.
    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/',
        },
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/',
        },
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/',
        }
    ]
    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        },
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        },
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        }
    ]

    sup_cat = [
        {'title': 'Machine Learning'},
        {'title': 'Frameworks'},
        {'title': 'Algorithms'},
        {'title': 'Web Design'},
    ]

    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask',
        'url':'http://flask.pocoo.org'}
    ]
        
    cats = {'Python': {'pages': python_pages},
        'Django': {'pages': django_pages},
        'Other Frameworks': {'pages': other_pages} }

    comments = [
        {'description': 'This course was intriguing but at the same time interesting',
         'date': datetime.date(2021,7,3)
         },
        {'description': 'What a wonderful experience, thank you for the links! Glad I discovered it',
         'date': datetime.date(2021,7,1)
         },
        {'description': 'I hated this, it was such a wasteful experience! I paid $10 for it as well',
         'date': datetime.date(2021,7,1)
         }
    ]

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['rating'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

def add_sup_cat(title):
    sc = SuperCategories.objects.get_or_create(name=title)[0]
    sc.save()
    return sc

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()