from .views import SignupView, SigninView


def add_routes(app):
    app.route('/account/signup', methods=['GET', 'POST'])(SignupView.as_view("signup"))
    app.route('/account/signin', methods=['GET', 'POST'])(SigninView.as_view("signin"))
