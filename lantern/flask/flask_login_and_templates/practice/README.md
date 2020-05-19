# to start work on project being in practice folder

    $ pip install -r grocery_store/requirements.txt
    $ pip install -e .
    $ python grocery_store/manage.py db upgrade
    $ python grocery_store/manage.py populate

To run server:

    $ python grocery_store/manage.py runserver
