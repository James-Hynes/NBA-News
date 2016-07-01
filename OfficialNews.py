import requests


class Stat:
    def __init__(self, url, params, args):
        self.headers = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/45.0.2454.101 Safari/537.36'),
                        'referer': 'http://stats.nba.com/scores/'
                        }
        self.params = self.handle_args(params, args)

        self.data = self.get_json(url, params)

    def get_json(self, url, n=0):
        try:
            js_data = requests.get(url, self.params, headers=self.headers, timeout=10).json()
        except ConnectionError:
            if n < 3:
                return self.get_json(url, n+1)
            else:
                return None
        except requests.RequestException:
            return None

        # put the headers and the stats together -- create a dictionary
        try:
            return [dict(zip(js_data['resultSet']['headers'], v)) for v in js_data['resultSet']['rowSet']]
        except KeyError:
            try:
                return {rset['name']: [dict(zip(rset['headers'], v)) for v in rset['rowSet']]
                        for rset in js_data['resultSets']}
            except KeyError:
                return [v for v in js_data['NBA_Player_Movement']['rows']]

    @staticmethod
    def handle_args(params, args):
        for key in params:
            if key in args.keys():
                params[key] = args[key]
        return params


class Transactions(Stat):
    def __init__(self):
        self.url = 'http://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json'
        super().__init__(self.url, {}, {})