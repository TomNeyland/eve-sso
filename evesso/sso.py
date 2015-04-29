
from flask_oauthlib.client import OAuth

oauth = OAuth()

eve_oauth = oauth.remote_app('EVEOAUTH',
                             app_key='EVEOAUTH',
                             base_url='https://crest-tq.eveonline.com/',
                             access_token_url='https://login.eveonline.com/oauth/token/',
                             authorize_url='https://login.eveonline.com/oauth/authorize/',
                             access_token_method='POST',
                             request_token_method='GET',
                             request_token_params={'scope': 'publicData'})
