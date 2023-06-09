from flask import render_template, request, flash, redirect
from flask.views import MethodView
from flask_login import login_user, current_user

from app.forms import SignupForm, SigninForm
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
                flash('Signup was successful. please signin now!', 'success')
                return redirect('signin')
            except:
                flash('There was an error during operation. please try again later', 'danger')

            # Redirect to a success page or perform other actions

        # Render the template with form and validation errors
        return render_template('signup.html', form=form)


class SigninView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            # Redirect the user to the dashboard if already signed in
            return 'dashboard'
        form = SigninForm()
        return render_template('signin.html', form=form)

    def post(self):
        form = SigninForm(request.form)
        if form.validate_on_submit():
            # Get form data
            email = form.email.data
            password = form.password.data

            # Perform sign-in authentication
            user = User.get_user_by('email', email)

            if user and user.check_password(password):
                # Sign in the user
                login_user(user)

                # Redirect to the dashboard or perform other actions upon successful sign-in
                flash('Sign-in successful!', 'success')
                return 'dashboard'
            else:
                # Display error message for failed sign-in attempt
                flash('Invalid email or password. Please try again.', 'danger')

        return render_template('signin.html', form=form)
