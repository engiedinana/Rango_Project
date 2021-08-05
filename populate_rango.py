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

    flask_pages = [
        {'title':'Introduction to Flask',
        'url':'https://opensource.com/article/18/4/flask'},
        {'title':'Documentation',
        'url':'https://flask.palletsprojects.com/en/2.0.x/'},
        {'title': 'Comparison with Django',
        'url': 'https://www.guru99.com/flask-vs-django.html'}
    ]

    bottle_pages = [
        {'title':'REST APIs with Bottle',
        'url':'https://www.toptal.com/bottle/building-a-rest-api-with-bottle-framework'},
        {'title':'Documentation',
        'url':'https://bottlepy.org/docs/dev/tutorial.html'},
        {'title': 'Comparison with Django',
        'url': 'https://www.slant.co/versus/1741/1746/~bottle_vs_django'}
    ]

    KNN_pages = [
        {'title':'KNN Introduction',
        'url':'https://www.mygreatlearning.com/blog/knn-algorithm-introduction/'},
        {'title':'When to Use KNN?',
        'url':'https://www.linkedin.com/pulse/machine-learning-when-should-i-use-k-nn-classifier-over-swapnil-amin/'},
        {'title': 'KNN VS KMeans',
        'url': 'https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2889-z'}
    ]

    regression_pages = [
        {'title':'Regression Analysis Introduction',
        'url':'https://www.codecademy.com/articles/introduction-regression-analysis'},
        {'title':'Why Use Regression?',
        'url':'https://statisticsbyjim.com/regression/when-use-regression-analysis/'},
        {'title': 'Regression in Forecasting',
        'url': 'https://smallbusiness.chron.com/advantages-regression-analysis-forecasting-61800.html'}
    ]

    sorting_pages = [
        {'title':'Intro From Geeks For Geeks',
        'url':''},
        {'title':'Why Use Regression?',
        'url':''},
        {'title': 'Regression in Forecasting',
        'url': ''}
    ]

    backtracking_pages = [
        {'title':'Intro From Geeks For Geeks',
        'url':''},
        {'title':'Why Use Regression?',
        'url':''},
        {'title': 'Regression in Forecasting',
        'url': ''}
    ]

    html_pages = [
        {'title':'Intro From Geeks For Geeks',
        'url':''},
        {'title':'Why Use Regression?',
        'url':''},
        {'title': 'Regression in Forecasting',
        'url': ''}
    ]

    API_pages = [
        {'title':'Intro From Geeks For Geeks',
        'url':''},
        {'title':'Why Use Regression?',
        'url':''},
        {'title': 'Regression in Forecasting',
        'url': ''}
    ]

    sup_cat = [
        {'title': 'Machine Learning'},
        {'title': 'Frameworks'},
        {'title': 'Algorithms'},
        {'title': 'Web Design'},
    ]

    # each category now has pages and comments 
    cats = {'Python': {'pages': python_pages},
        'Django': {'pages': django_pages},
        'Flask': {'pages': flask_pages},
        'Bottle': {'pages': bottle_pages},
        'KNN': {'pages': KNN_pages},
        'Regression': {'pages': regression_pages},
        'Sorting': {'pages': sorting_pages},
        'Backtracking': {'pages': backtracking_pages},
        'HTML': {'pages': html_pages},
        'APIs': {'pages': API_pages},
    }

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