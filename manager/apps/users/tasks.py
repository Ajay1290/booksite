from manager.lib.flask_mailplus import send_email
from manager import create_celery_app
from manager.models import Users

celery = create_celery_app()


@celery.task()
def deliver_password_reset_email(user_id, reset_token):
    """
    Send a reset password e-mail to a user.

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    user = Users.query.get(user_id)

    if user is None:
        return None

    confirm_url = url_for('users.password_reset', reset_token=reset_token, _external=True)
    html = render_template('mails/users/password_reset', username=user.username, confirm_url=confirm_url)

    send_email(to=user.email,subject='Password reset from Snake Eyes',template=html)

    return None
