import requests
import datetime


DEVMAN_API_URL = 'http://devman.org/api/challenges/solution_attempts/'


def load_attempts():
    pages = requests.get(
        DEVMAN_API_URL,
        params={'page': 1},
    ).json()['number_of_pages']
    for page in range(1, pages):
        params = {'page': page}
        attempts_page = requests.get(DEVMAN_API_URL, params=params).json()
        for attempt in attempts_page['records']:
            yield attempt


def is_attempt_after_midnight(attempt):
    midnight = datetime.time(0)
    morning = datetime.time(6)
    dt = datetime.datetime.fromtimestamp(attempt['timestamp'])
    return (midnight < dt.time() < morning)


def get_midnighters(attemps):
    users = set()
    for attempt in attempts:
        if is_attempt_after_midnight(attempt):
            users.add(attempt['username'])
    return users


if __name__ == '__main__':
    attempts = load_attempts()
    users = get_midnighters(attempts)
    print(
        'Список людей, которые отправляли задачи на проверку после полуночи:',
        users,
    )
