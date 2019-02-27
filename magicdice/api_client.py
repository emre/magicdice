import requests


class ApiClient:
    """The main API client to interact with the magic-dice website's
    HTTP endpoint.
    """

    def __init__(self, api_base_url=None):
        self.api_base_url = api_base_url or "https://magic-dice.com/api"

    def _generate_url(self, path):
        """Generates URLS based on the path.

        :param path (str): Path. Ex: bets
        :return (str): Full path
        """
        return f"{self.api_base_url}/{path}/"

    def bets(self, username, params=None):
        """Returns the bets of a specific user.

        :param username (str): Steem account
        :param params (dict): Query params
        :return (dict): API Response
        """
        return requests.get(
            self._generate_url('bets/' + username),
            params=params
        ).json()

    def globals(self):
        """Returns the global properties of the game.

        :return (dict): API Response
        """
        return requests.get(
            self._generate_url('globals')
        ).json()

    def user(self, username):
        """Returns the base user information.

        :param username (str): Steem account
        :return (dict): API Response
        """
        return requests.get(
            self._generate_url('user/' + username)
        ).json()

    def top_winners(self, params=None):
        """Returns the top winners

        :param params (dict): Query params
        :return (dict): API Response
        """
        resp = requests.get(
            self._generate_url('bets/top_winners'),
            params=params
        )

        return resp.json()

    def rare_wins(self, params=None):
        """Returns the rare wins

        :param params (dict): Query params
        :return (dict): API Response
        """
        return requests.get(
            self._generate_url('bets/rare_wins'),
            params=params
        ).json()