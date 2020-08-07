from flask import Blueprint, render_template, request, redirect, url_for
from manager.models.Books import Books, Authors
from manager.models.Users import Users

pages = Blueprint('pages', __name__)

@pages.route('/privacy')
def privacy():
    return render_template('apps/pages/privacy.html')


@pages.route('/feedback')
def feedback():
    return render_template('apps/pages/feedback.html')


@pages.route('/terms')
def terms():
    return render_template('apps/pages/terms.html')
