import requests


class ApiClient:

    def __init__(self, api_base_url=None):
        self.api_base_url = api_base_url or "https://magic-dice.com/api"

    def _generate_url(self, path):
        return f"{self.api_base_url}/{path}/"

    def bets(self, username, params=None):
        return requests.get(
            self._generate_url('bets/' + username),
            params=params
        ).json()

    def globals(self):
        return requests.get(
            self._generate_url('globals')
        ).json()

    def user(self, username):
        return requests.get(
            self._generate_url('user/' + username)
        ).json()

    def top_winners(self, params=None):
        resp = requests.get(
            self._generate_url('bets/top_winners'),
            params=params
        )

        return resp.json()

    def rare_wins(self, params=None):
        return requests.get(
            self._generate_url('bets/rare_wins'),
            params=params
        ).json()