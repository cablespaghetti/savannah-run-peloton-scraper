import datetime

import requests

API_BASE = 'https://api.onepeloton.co.uk/api/'
COOKIE = '584455b4a61846988936ee504407f2fd'
CHALLENGE_START = datetime.datetime(2021, 11, 22, 0, 0)
RUN_DICT = {
    1: {
        'start': datetime.datetime(2021, 11, 22, 0, 0),
        'end': datetime.datetime(2021, 11, 29, 0, 0),
        'runs': {
            'f28a1a8788ca4ac5a72deed1e1171b2b':  '20 min recovery run - Susie Chan - 23/10/21',
            'ef73518d446f4c5b83c2cfc0ce951a81':  '30 min endurance run - Becs Gentry - 3/11/21',
            'dc35da04423644f08e07a9b29b656f07':  '30 min endurance run - Matt Wilpers - 7/9/21'
        }
    },
    2: {
        'start': datetime.datetime(2021, 11, 29, 0, 0),
        'end': datetime.datetime(2021, 12, 6, 0, 0),
        'runs': {
            'ff5dca33e7b647deb3c6bfc19763a5e4': '30 min endurance run - Selena Samuela - 14/3/21',
            'a7fca7df520742b5af771c8b12b72926':  '30 min progression run - Becs Gentry - 9/7/21',
            'b9bfcfda74c64c639d4510987f6b4368':  '45 min endurance run - Matt Wilpers - 7/6/21'
        }
    },
    3: {
        'start': datetime.datetime(2021, 12, 6, 0, 0),
        'end': datetime.datetime(2021, 12, 13, 0, 0),
        'runs': {
            '79ac1f29dd7d4c30820f048831c0bf3a':  '30 min you can run: form  - Matt Wilpers - 23/4/21',
            '9aafb3a29e2e482bac4cc46e716db77b':  '45 min NYC Marathon simulation run - Robin Arzon - 7/10/19',
            'e4229c0132fc4c5d998693c7d044afb2':  '30 min intervals run - Olivia Amato - 16/6/21'
        }
    },
    4: {
        'start': datetime.datetime(2021, 12, 13, 0, 0),
        'end': datetime.datetime(2021, 12, 20, 0, 0),
        'runs': {
            'ed8a76e5590c469c9e9067a3dbae0d24':  '30 min recovery run - Matt Wilpers - 3/8/20',
            '144a8ec7f56d4949a1fdd1b22c7aaee2': '30 min tempo run - Olivia Amato - 18/11/20',
            '0bf1c3f590784cd9b9392176d9170456':  '60 min endurance run - Marcel Dinkins - 12/9/21',
            '6213fb1fbd9945c2985b3efde630cc0b': '60 min endurance run - Susie Chan - 15/12/21'
        }
    },
    5: {
        'start': datetime.datetime(2021, 12, 20, 0, 0),
        'end': datetime.datetime(2021, 12, 27, 0, 0),
        'runs': {
            'ac56d7fa789a43c9a7321beafbd29e97':  '30 min HIIT run - Robin Arzon - 23/9/19',
            '0be5c37b63164379a885d8c6f8873002':  '60 min NYC Marathon simulation run - Becs Gentry - 1/11/20',
            '8db4bbcd0232457f97071a86a0f79180':  '45 min endurance run - Selena Samuela - 22/12/20',
            '8b73ca8b875d4a0bbd6b3fc517ee59fa':  '45 min endurance run - Becs Gentry - 23/12/21'
        }
    },
    6: {
        'start': datetime.datetime(2021, 12, 27, 0, 0),
        'end': datetime.datetime(2022, 1, 3, 0, 0),
        'runs': {
            'e1cfa230fa6842cfb8bce724ab171ce3':  '30 min recovery run - Becs Gentry - 28/10/19',
            '27339dae48084112bbc98ae246c32bea':  '30 min endurance run - Matt Wilpers - 10/8/20',
            '549de6c8c6dc42789d9088dfafaac015':  '45 min endurance run - Matt Wilpers - 24/9/21'
        }
    }
}


def get_users():
    return {
        '32df2a456cd94a77bbf3a6c32af6cb26': 'User name 1'
    }


def get_user_running_workouts(user_id):
    next_timestamp = datetime.datetime.utcnow().timestamp()
    activity_data = []
    loop_counter = 0
    while next_timestamp > CHALLENGE_START.timestamp():
        response = requests.get(
            f'{API_BASE}user/{user_id}/workouts?joins=ride&limit=10&page={loop_counter}',
            cookies={'peloton_session_id': COOKIE}
        )
        response_object = response.json()
        activity_data_list = response_object['data']
        activity_data.extend(activity_data_list)
        if 'next' in response_object:
            next_timestamp = response_object['next']['created_at']
            loop_counter += 1
        else:
            break
        # print(f"Got {len(activity_data_list)} workouts for {user_id}")
        # print(f"Challenge start at {CHALLENGE_START.timestamp()}. Next timestamp {next_timestamp}.")
    activity_data.reverse()
    return activity_data


def get_total_distance(user_id, user_name):
    user_activities = get_user_running_workouts(user_id)
    distance_total = 0
    pr_counter = 0
    for activity in user_activities:
        if activity['metrics_type'] != 'running' and activity['status'] != 'COMPLETE':
            continue
        activity_class_id = activity['ride']['id']
        activity_time = datetime.datetime.utcfromtimestamp(activity['start_time'])
        pr = activity['is_total_work_personal_record']

        for run_week, run_week_dict in RUN_DICT.items():
            if run_week_dict['start'] < activity_time < run_week_dict['end']:
                if activity_class_id in run_week_dict['runs'].keys():
                    distance = get_distance_for_activity(activity)

                    print(f"Found matching activity for {user_name} - Week {run_week} - {run_week_dict['runs'][activity_class_id]} - {distance}Mi")
                    if pr:
                        print(f"PR ALERT!!!")
                        pr_counter += 1
                    distance_total += distance
                break
    return distance_total, pr_counter


def get_distance_for_activity(activity):
    distance_response = requests.get(
        f"{API_BASE}workout/{activity['id']}/performance_graph?every_n=5",
        cookies={'peloton_session_id': COOKIE}
    )
    distance_response_object = distance_response.json()
    for distance_response_summary in distance_response_object['summaries']:
        if distance_response_summary['slug'] == 'distance':
            return distance_response_summary['value']


if __name__ == '__main__':
    for user_id, user_name in get_users().items():
        user_distance, user_prs = get_total_distance(user_id, user_name)
        print(f"Total distance for {user_name} is {round(user_distance,2)}Mi - They got {user_prs} PRs")
