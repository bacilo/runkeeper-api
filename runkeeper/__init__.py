from requests_oauthlib import OAuth2Session

import unicodecsv as csv

# Where user is redirected to authorize access to his or her Runkeeper account.
AUTHORIZATION_URL = 'https://runkeeper.com/apps/authorize'

# Where your application can convert an authorization code to an access token.
ACCESS_TOKEN_URL = 'https://runkeeper.com/apps/token'

# Where your application can disconnect itself from the user's account.
DE_AUTHORIZATION_URL = 'https://runkeeper.com/apps/de-authorize'

# API Endpoint
API_URL = 'https://api.runkeeper.com/'


class RunKeeper(object):
    def __init__(self,
                 client_id,
                 client_secret,
                 access_token="",
                 redirect_uri='http://localhost:8000/gettoken.html'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.oauth = OAuth2Session(self.client_id, redirect_uri=redirect_uri)

    def get_profile(self):
        return self.get('user', 'User')

    def get_activities(self, page):
        return self.get(page, 'FitnessActivityFeed').json()

    def get_all_activities_csv(self, output_folder=''):
        l_acts = self.get_all_activities()
        f_acts = open(output_folder + 'rk_activities.csv', 'wb')
        f_act_data = open(output_folder + 'rk_activity_data.csv', 'wb')
        w_acts = csv.writer(
            f_acts,
            dialect='excel',
            encoding='utf-8',
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_NONNUMERIC)
        w_act_data = csv.writer(
            f_act_data,
            dialect='excel',
            encoding='utf-8',
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_NONNUMERIC)

        w_acts.writerow((
            'id',
            'type',
            'equipment',
            'start_time',
            'total_distance',
            # 'distance',
            'duration',
            'calories',
            'total_climb'
            ))

        w_act_data.writerow((
            'id',
            'timestamp',
            'longitude',
            'latitude',
            'altitude',
            'type'
            ))

        for _a in l_acts:
            a = self.get_activity(_a['uri']).json()
            w_acts.writerow((
                _a['uri'].split('/fitnessActivities/')[1],
                a['type'],
                a['equipment'],
                a['start_time'],
                a['total_distance'],
                # a['distance'],
                a['duration'],
                a['calories'],
                a['total_climb'] if 'total_climb' in a else 'n/a'
                ))

            for p in a['path']:
                w_act_data.writerow((
                    _a['uri'].split('/fitnessActivities/')[1],
                    p['timestamp'],
                    p['longitude'],
                    p['latitude'],
                    p['altitude'],
                    p['type']
                    ))

    def get_all_activity_uris(self):
        _uris = []
        page = 'fitnessActivities?page=0&pageSize=50'
        while True:
            r = self.get_activities(page)
            for a in r['items']:
                _uris.append(a['uri'])
            if 'next' not in r:
                break
            page = r['next']
        return _uris

    def get_all_activities(self):
        _acts = []
        page = 'fitnessActivities?page=0&pageSize=50'
        while True:
            r = self.get_activities(page)
            for a in r['items']:
                _acts.append(a)
            if 'next' not in r:
                break
            page = r['next']
        return _acts

    def get_activity(self, act_uri):
        return self.get(act_uri, 'FitnessActivity')

    def get(self, endpoint, media_type):
        return self.oauth.get(
            API_URL + endpoint,
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'Accept': 'application/vnd.com.runkeeper.{}+json'.format(
                    media_type)})

    # An attempt to automate the getting of the token.
    # Still an ambition to do but not a priority:

    # def get_access_token(self):
    #   authorization_url, state = oauth.authorization_url(AUTHORIZATION_URL)
    #   # print 'Please go to %s and authorize access.' % authorization_url
    #   # authorization_response = raw_input('Enter the full callback URL')
    #   # print authorization_response
    #   self.access_token = self.oauth.fetch_token(
    #       self.access_token,
    #       authorization_response=authorization_response,
    #       client_secret=self.client_secret)
