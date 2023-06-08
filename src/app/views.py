from flask import render_template, request, flash
from flask.views import MethodView

from app.forms import SignupForm
from app.models import User


class SignupView(MethodView):
    @staticmethod
    def get():
        form = SignupForm()
        return render_template('signup.html', form=form)

    @staticmethod
    def post():
        form = SignupForm(request.form)
        if form.validate_on_submit():
            # Get form data
            email = form.email.data
            username = form.username.data
            password = form.password.data

            # Create a User object
            user = User(email=email, username=username, password=password)

            # Save the user to the database

            try:
                user.save_to_database()
            except:
                flash('There was an error during operation.\n please try again later', 'danger')

            # Redirect to a success page or perform other actions

        # Render the template with form and validation errors
        return render_template('signup.html', form=form)
