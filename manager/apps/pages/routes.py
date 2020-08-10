from flask import Blueprint, render_template, request, redirect, url_for
from manager.models.Books import Books, Authors
from manager.models.Users import Users
from manager.apps.pages.forms import FeedbackForm

pages = Blueprint('pages', __name__)

@pages.route('/you-reached-download-limit')
def download_limit():
    return render_template('apps/pages/download_limit.html')

@pages.route('/privacy')
def privacy():
    return render_template('apps/pages/privacy.html')


# @pages.route('/feedback')
# def feedback():
#     form = FeedbackForm()
#     return render_template('apps/pages/feedback.html', form=form)


@pages.route('/terms')
def terms():
    return render_template('apps/pages/terms.html')

@pages.route('/dmca')
def dmca():
    return render_template('apps/pages/dmca.html')
