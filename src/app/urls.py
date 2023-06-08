from .views import SignupView


def add_routes(app):
    app.route('/account/signup', methods=['GET', 'POST'])(SignupView.as_view("signup"))

