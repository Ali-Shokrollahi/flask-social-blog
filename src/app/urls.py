from .views import index


def add_routes(app):
    app.route('/')(index)
