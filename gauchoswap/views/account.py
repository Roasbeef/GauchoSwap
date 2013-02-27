from flask import (redirect, url_for, session, request, Blueprint, flash, g)
from gauchoswap import db, oauth, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from gauchoswap.models import Student, Swapblock


mod = Blueprint('account', __name__)


facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': 'email'}
                            )


@mod.route('/logout')
def logout():
    session.pop('oauth_token')
    session.pop('fb_id')

    flash('You have been logged out!', category='success')
    return redirect(url_for('frontend.index'))


@mod.route('/fb_auth')
def fb_auth():
    return facebook.authorize(callback=url_for('account.login_or_register', _external=True))


@mod.route('/login/authorized')
@facebook.authorized_handler
def login_or_register(resp):
    if resp is None:
        flash('Something happend: %s, %s' % (request.args['error_reason'],
                                             request.args['error_description']))
        return redirect(url_for('frontend.index'))

    session['oauth_token'] = (resp['access_token'], '')

    fb_account = facebook.get('/me?fields=picture,link,name,id')
    fb_id = fb_account.data['id']

    user_account = Student.query.filter_by(facebook_id=fb_id).first()
    message = 'Log in successful!'

    if user_account is None:
        new_student = Student(name=fb_account.data['name'], umail_address='',
                              facebook_id=fb_account.data['id'], fb_auth_token=resp['access_token'],
                              fb_profile_link=fb_account.data['link'],
                              fb_picture_link=fb_account.data['picture']['data']['url'])
        block = Swapblock(new_student)
        db.session.add(new_student)
        db.session.add(block)
        db.session.commit()
        user_account = new_student
        message = 'You have been registered congrats!'

    flash(message, category='success')
    session['fb_id'] = fb_account.data['id']
    g.user = user_account
    return redirect(url_for('frontend.index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
