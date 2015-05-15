# THIS FILE NEEDS TO BE CONVERTED INTO A FLASK BLUEPRINT
# THIS IS JUST A WIP FILE WHERE I FIGURED OUT THE CREST OAUTH WORKFLOW
# THIS CODE DOES NOT REPRESENT BEST PRACTICES

import base64
import logging
import os
import sys
import datetime
import pytz
from dateutil.parser import parse
from flask import current_app, Blueprint, render_template, redirect, url_for, session, request, jsonify, send_from_directory
from flask import jsonify
from flask.ext.login import LoginManager, login_required, current_user, login_user, AnonymousUserMixin
import requests
import simplejson as json

from evesso import db, utils
from .models import Character, CrestAuthorization, Chatroom
from .sso import oauth, eve_oauth


log = logging.getLogger(__name__)
auth = Blueprint('auth', __name__)

REFRESH_HEADERS = {
    'Host': 'login.eveonline.com',
    'Content-Type': 'application/x-www-form-urlencoded',
}

login_manager = LoginManager()

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(character_id):
    return Character.query.get(character_id)


@auth.route('/')
@login_required
def index():
    return current_app.send_static_file('index.html')


@auth.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    log.debug('send_static_file: %s', path)
    return current_app.send_static_file(path)


@auth.route('/login')
def login():
    return eve_oauth.authorize(callback=url_for('.sso',
                                                next=request.args.get('next') or request.referrer or None,
                                                _external=True),
                               )


@auth.route('/sso/')
def sso():
    crest_auth = eve_oauth.authorized_response()

    if crest_auth is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['access_token'] = crest_auth['access_token']
    session['refresh_token'] = crest_auth['refresh_token']
    character_data = eve_oauth.get('https://login-tq.eveonline.com/oauth/verify/', headers={'Host': 'login.eveonline.com',
                                                                                            'Content-Type': 'application/x-www-form-urlencoded',
                                                                                            'Authorization': 'Bearer %s' % (crest_auth['access_token'][0])})

    session['character'] = dict(
        CharacterID=character_data.data['CharacterID'], CharacterName=character_data.data['CharacterName'])
    created = False
    main_character = None

    if isinstance(current_user._get_current_object(), Character) and current_user.is_authenticated:
        chr_data = character_data.data
        chr_data['mainCharacterID'] = current_user.CharacterID
        character, created = get_or_create_character(chr_data, crest_auth, login=True)
        chr_data['mainCharacter'] = current_user
    else:
        character, created = get_or_create_character(character_data.data, crest_auth, login=True)

    if character.mainCharacter is not None:
        login_user(character.mainCharacter)
        main_character = character.mainCharacter
    else:
        login_user(character)
        main_character = character

    # do initial setup
    if created:
        notifications_room = Chatroom.query.get('notifications')
        main_character.chatrooms.append(notifications_room)
        db.session.commit()

    del session['access_token']
    del session['refresh_token']

    response = redirect(request.args.get('next', '/access_token'))
    response.set_cookie('crestConfig', value=json.dumps(
        {'character': session.get('character'), 'Authorization': 'Bearer %s' % (crest_auth['access_token'][0])}))

    return response


@auth.route('/access_token')
@login_required
def access_token():
    return jsonify(get_character_info(current_user))


@auth.route('/endpoints')
@login_required
def endpoints():
    return jsonify(json.loads(eve_oauth.get('https://crest-tq.eveonline.com/').data))


def get_character_info(character):

    data = dict(expires_at=character.crest_authorization.expires_at.isoformat(),
                expires_in=(character.crest_authorization.expires_at - utils.utcnow()).total_seconds(),
                CharacterOwnerHash=character.CharacterOwnerHash,
                CharacterName=character.CharacterName,
                CharacterID=character.CharacterID,)

    if character.crest_authorization:
        data['access_token'] = character.crest_authorization.access_token

    if character.other_characters:
        other_char_data = []
        data['other_characters'] = other_char_data

        for char in character.other_characters:
            other_char_data.append(get_character_info(char))

    return data


def get_or_create_character(character_data, crest_auth=None, login=True):

    character_data = dict(**character_data)
    expires_on = character_data.get('ExpiresOn')
    created = False

    if expires_on is not None:
        expires_on = parse(expires_on)
        character_data['ExpiresOn'] = expires_on

    character = Character.query.filter_by(CharacterID=character_data['CharacterID']).first()

    if character is None:
        created = True
        character = Character(**character_data)
        character.crest_authorization = CrestAuthorization(character=character, **crest_auth)
        character.crest_authorization.CharacterID = character.CharacterID
        expires_at = utils.utcnow() + datetime.timedelta(seconds=int(crest_auth['expires_in']) - 60)
        character.crest_authorization.expires_at = expires_at
    else:
        expires_at = utils.utcnow() + datetime.timedelta(seconds=int(crest_auth['expires_in']) - 60)
        character.crest_authorization.expires_at = expires_at
        character.crest_authorization.access_token = crest_auth['access_token']
        character.crest_authorization.refresh_token = crest_auth['refresh_token']

    db.session.add(character)
    db.session.commit()

    return (character, created)


@eve_oauth.tokengetter
def get_eve_oauth_access_token(token='access'):

    if 'access_token' in session:
        return (session['access_token'], '')

    if hasattr(current_user, 'crest_authorization'):
        if token == 'access':
            expires_at = current_user.crest_authorization.expires_at
            if expires_at is None or (expires_at - utils.utcnow()).total_seconds() <= 60:
                log.debug('Refreshing Authorization')
                new_auth = refresh_authorization(refresh_token=current_user.crest_authorization.refresh_token).json()
                for key, value in new_auth.items():
                    setattr(current_user.crest_authorization, key, value)

                current_user.crest_authorization.expires_at = datetime.datetime.utcnow(
                ) + (datetime.timedelta(seconds=int(new_auth['expires_in']) - 60))
                db.session.add(current_user.crest_authorization)
                db.session.add(current_user)
                db.session.commit()

            return (current_user.crest_authorization.access_token, '')
        elif token == 'refresh':
            return (current_user.crest_authorization.refresh_token, '')
    elif 'access_token' in session:
        return (session['access_token'], '')
    else:
        return ''

    # if token == 'access':
    #     if 'authorization' in session:
    #         expires_at = session.get('expires_at')
    #         log.debug('Authorization will expire at: %s \n\t %s', expires_at, session['authorization'])

    #         if expires_at is None or utils.utcnow() >= parse(expires_at):

    #             log.debug('Refreshing Authorization')

    #             expires_at = datetime.datetime.utcnow(
    #             ) + datetime.timedelta(seconds=int(session['authorization']['expires_in']) - 60)
    #             session['expires_at'] = expires_at.isoformat()

    #             log.debug('Authorization will expire at: %s \n\t %s', expires_at, session['authorization'])

    #     return (session.get('authorization', {}).get('access_token'), '')
    # elif token == 'refresh':
    #     return (session.get('authorization', {}).get('refresh_token'), '')


def refresh_authorization(refresh_token=None):

    auth_hash = base64.encodestring(eve_oauth.consumer_key + ':' + eve_oauth.consumer_secret).replace('\n', '')
    auth_header = 'Basic %s' % auth_hash

    refresh_response = requests.post("https://login.eveonline.com/oauth/token",
                                     headers=dict(Authorization=auth_header, **REFRESH_HEADERS),
                                     data=_get_refresh_body(refresh_token=refresh_token))

    print refresh_response.text, refresh_response.reason, refresh_response.headers

    refresh_data = refresh_response.json()

    return refresh_response


def _get_refresh_body(refresh_token=None):
    return dict(scope='publicData',
                grant_type='refresh_token',
                refresh_token=refresh_token or get_eve_oauth_access_token('refresh'))


if __name__ == '__main__':
    current_app.run()
