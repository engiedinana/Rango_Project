"""
This file is used to populate the category, pages and super categories tables to be able to utilize the webapp
"""
import os
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, SuperCategories, Comments

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    # Pages Data
    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/',
        'description': 'This website is very useful for python beginners.'
        },
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/',
        'description': 'Are you looking up to experts in CS? This website helps you think like one!'
        },
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/',
        'description': 'A very good ramp up for python to use on the go while developing.'
        }
    ]
    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        'description': 'This website is very useful for django beginners.'
        },
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        'description': 'Wondering why django is better than other frameworks; visit this website!'
        },
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        'description': 'A useful book for django beginners.'
        }
    ]

    flask_pages = [
        {'title':'Introduction to Flask',
        'url':'https://opensource.com/article/18/4/flask',
        'description': 'This website is very useful for flask beginners.'},
        {'title':'Documentation',
        'url':'https://flask.palletsprojects.com/en/2.0.x/',
        'description': 'All the documentation you need can be found here. Cheat Sheet!'},
        {'title': 'Comparison with Django',
        'url': 'https://www.guru99.com/flask-vs-django.html',
        'description': 'Take a decision on which framework to use here.'}
    ]

    bottle_pages = [
        {'title':'REST APIs with Bottle',
        'url':'https://www.toptal.com/bottle/building-a-rest-api-with-bottle-framework',
        'description': 'This website is very useful for bottle beginners.'},
        {'title':'Documentation',
        'url':'https://bottlepy.org/docs/dev/tutorial.html',
        'description': 'All the documentation you need can be found here. Cheat Sheet!'},
        {'title': 'Comparison with Django',
        'url': 'https://www.slant.co/versus/1741/1746/~bottle_vs_django',
        'description': 'Take a decision on which framework to use here.'}
    ]

    KNN_pages = [
        {'title':'KNN Introduction',
        'url':'https://www.mygreatlearning.com/blog/knn-algorithm-introduction/',
        'description': 'This website is very useful for ML beginners.'},
        {'title':'When to Use KNN?',
        'url':'https://www.linkedin.com/pulse/machine-learning-when-should-i-use-k-nn-classifier-over-swapnil-amin/',
        'description': 'A good explanation of the usefulness of KNN'},
        {'title': 'KNN VS KMeans',
        'url': 'https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2889-z',
        'description': 'Take a decision on which classification algorithm to use.'}
    ]

    regression_pages = [
        {'title':'Regression Analysis Introduction',
        'url':'https://www.codecademy.com/articles/introduction-regression-analysis',
        'description': 'This website is very useful for ML beginners.'},
        {'title':'Why Use Regression?',
        'url':'https://statisticsbyjim.com/regression/when-use-regression-analysis/',
        'description': 'The reason for regression usefulness is explained thoroughly.'},
        {'title': 'Regression in Forecasting',
        'url': 'https://smallbusiness.chron.com/advantages-regression-analysis-forecasting-61800.html',
        'description': 'How do people use regression in forecasting?'}
    ]

    sorting_pages = [
        {'title':'Practice Problems',
        'url':'https://www.geeksforgeeks.org/sorting-algorithms/',
        'description': 'This website is very useful for coding beginners.'},
        {'title':'Bubble Sort',
        'url':'https://www.geeksforgeeks.org/bubble-sort/',
        'description': 'This website is very useful for coding beginners. One of the most interesting algorithms'},
        {'title': 'Insertion Sort',
        'url': 'https://www.geeksforgeeks.org/insertion-sort/',
        'description': 'This website is very useful for coding beginners. One of the most interesting algorithms'}
    ]

    backtracking_pages = [
        {'title':'What is backtracking',
        'url':'https://www.baeldung.com/cs/backtracking-algorithms',
        'description': 'This website is very useful for coding beginners.'},
        {'title':'N Queen Problem',
        'url':'https://www.geeksforgeeks.org/n-queen-problem-backtracking-3/',
        'description': 'This problem is a well-known one in the history of CS. Must try this out!'},
        {'title': 'Practice Problems',
        'url': 'https://www.codingame.com/learn/backtracking',
        'description': 'Get ready for interviews!'}
    ]

    html_pages = [
        {'title':'HTML for Beginners',
        'url':'https://html.com/',
        'description': 'This website is very useful for HTML beginners.'},
        {'title':'HTML Editors',
        'url':'http://www-db.deis.unibo.it/courses/TW/DOCS/w3schools/html/html_editors.asp.html',
        'description': 'This website gives good suggestions for the possible editors.'},
        {'title': 'Geolocation',
        'url': 'http://www-db.deis.unibo.it/courses/TW/DOCS/w3schools/html/html5_geolocation.asp.html',
        'description': 'How to set geolocation using html'}
    ]

    database_pages = [
        {'title':'Types of databases',
        'url':'matillion.com/resources/blog/the-types-of-databases-with-examples',
        'description': 'What types of database are out there? the world is full of options.'},
        {'title':'SQL DB Introduction',
        'url':'https://www.w3schools.com/sql/sql_intro.asp',
        'description': 'SQL Introduction in databases'},
        {'title': 'NoSQL DB',
        'url': 'https://www.mongodb.com/nosql-explained',
        'description': 'NoSQL Introduction in databases'}
    ]

    # Category Section
    # each category now has pages, ratings, image and last modified date
    ml_categories = {
        'KNN': {'pages': KNN_pages, 'rating': 4, 'image': 'KNN.png', 'last_modified': datetime.date.today()},
        'Regression': {'pages': regression_pages, 'rating': 4, 'image': 'Regression.png', 'last_modified': datetime.date.today()},
    }
    
    frameworks_categories = {
        'Django': {'pages': django_pages, 'rating': 5, 'image': 'Django.png', 'last_modified': datetime.date.today()},
        'Flask': {'pages': flask_pages, 'rating': 5,  'image': 'Flask.png', 'last_modified': datetime.date.today()},
        'Bottle': {'pages': bottle_pages, 'rating': 4,  'image': 'Bottle.png', 'last_modified': datetime.date.today()},
    }

    algos_categories = {
        'Sorting': {'pages': sorting_pages, 'rating': 3,'image': 'Sorting.jpeg', 'last_modified': datetime.date.today()},
        'Backtracking': {'pages': backtracking_pages, 'rating': 3, 'image': 'Backtracking.jpeg', 'last_modified': datetime.date.today()},
    }

    web_categories = {
        'Python': {'pages': python_pages, 'rating': 5, 'image': 'Python.png', 'last_modified': datetime.date.today()},
        'HTML': {'pages': html_pages, 'rating': 2, 'image': 'HTML.png', 'last_modified': datetime.date.today()},
        'Database': {'pages': database_pages, 'rating': 1, 'image': 'Database.png', 'last_modified': datetime.date.today()},
    }

    sup_cats = {
        'Machine Learning':{'categories':ml_categories},
        'Frameworks':{'categories':frameworks_categories},
        'Algorithms':{'categories':algos_categories},
        'Web Design':{'categories':web_categories},
    }

    # Populate the super categories and then the categories and then the pages
    # the order is important in order to accommodate the table relations
    for sup_cat, sup_data in sup_cats.items():
        sup = add_sup_cat(sup_cat)
        for cat, cat_data in sup_data['categories'].items():
            c = add_cat(sup, cat, cat_data['rating'], cat_data['image'], cat_data['last_modified'])
            for p in cat_data['pages']:
                add_page(c, p['title'], p['url'], p['description'])

# add a page to the pages DB
def add_page(category, title, url, description):
    p = Page.objects.get_or_create(category=category, title=title)[0]
    p.url=url
    p.description = description
    p.save()
    return p

# add a category to the category DB
def add_cat(super_cat, name, rating, image, last_modified):
    c = Category.objects.get_or_create(super_cat=super_cat, name = name)[0]
    c.rating = rating
    c.image = image
    c.last_modified = last_modified
    c.save()
    return c

# add a super category to the supercategory table
def add_sup_cat(title):
    sc = SuperCategories.objects.get_or_create(title=title)[0]
    sc.save()
    return sc

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()