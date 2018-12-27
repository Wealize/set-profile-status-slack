import os

import requests
from bs4 import BeautifulSoup


LAZONA_CHECKEDIN_URL = 'https://lazona.co/es/directory/members?onlycheckedin=true'
TNP_MEMBERS_SLACK_IDS = {
        'Daniel Luque Quintana': '',
        'Miguel Ángel Calero Fernández': '',
        'Javier Aguirre': '',
        'Nieves María Borrero Barea': '',
        'Natalia Moreno Arévalo': ''
}
SLACK_API_KEY = os.environ.get('SLACK_API_KEY')
SLACK_USER_PROFILE_SET_ENDPOINT = 'https://theneonproject.slack.com/api/users.profile.set'
SLACK_LAZONA_PAYLOAD = {
	"user": '',
	"profile": {
                "status_text": "En la Zona",
                "status_emoji": ":zona:",
                "status_expiration": 0
	}
}
SLACK_NOTLAZONA_PAYLOAD = {
	"user": '',
	"profile": {
                "status_text": "",
                "status_emoji": "",
                "status_expiration": 0
	}
}
STATUSES = {
        'zona': SLACK_LAZONA_PAYLOAD,
        'notzona': SLACK_NOTLAZONA_PAYLOAD
}
HEADERS = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': ' '.join(['Bearer', SLACK_API_KEY])
}


def set_status_slack(user_id, status):
    payload = STATUSES[status].copy()
    payload['user'] = user_id
    requests.post(SLACK_USER_PROFILE_SET_ENDPOINT, json=payload, headers=HEADERS)

def get_people_lazona():
    req = requests.get(LAZONA_CHECKEDIN_URL)
    status_code = req.status_code

    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")
        members = html.find_all('h3', {'class': 'user-badge__name'})

        return [member.getText().strip() for member in members]


def is_in_lazona(member_name, members):
    return member_name in TNP_MEMBERS_SLACK_IDS.keys()


def main():
    members = get_people_lazona()
    tnp_members_zona = []

    for member_name in members:
        if is_in_lazona(member_name, members):
            set_status_slack(TNP_MEMBERS_SLACK_IDS[member_name], 'zona')
            tnp_members_zona.append(member_name)

    members_out = [
        member_name
        for member_name in TNP_MEMBERS_SLACK_IDS.keys()
        if member_name not in tnp_members_zona
    ]

    if members_out:
        for member_name in members_out:
            set_status_slack(TNP_MEMBERS_SLACK_IDS[member_name], 'notzona')


if __name__ == '__main__':
    main()
