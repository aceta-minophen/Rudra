import fitbit
import gather_keys_oath2 as Oauth2

import pandas as pd
import datetime

CLIENT_ID = '238B7Z'
CLIENT_SECRET = '421db587b7eaa6ff0ab7e37bde55ca10'

print("Hello world")

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True,
                             access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


yesterday = str((datetime.datetime.now() -
                datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() -
                 datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))

fit_statsHR = auth2_client.intraday_time_series(
    'activities/heart', base_date=yesterday2, detail_level='1sec')
