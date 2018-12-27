import requests
from bs4 import BeautifulSoup

LAZONA_CHECKEDIN_URL = 'https://lazona.co/es/directory/members?onlycheckedin=true'


def get_people_lazona():
    req = requests.get(LAZONA_CHECKEDIN_URL)
    status_code = req.status_code

    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")
        members = html.find_all('h3', {'class': 'user-badge__name'})

        return [member.getText().strip() for member in members]


def is_in_lazona(member_name, members):
    return member_name in members


def main():
    # TODO
    pass


if __name__ == '__main__':
    main()
