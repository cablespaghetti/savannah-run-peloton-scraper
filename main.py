import csv
import datetime
import os

import requests

API_BASE = 'https://api.onepeloton.co.uk/api/'
COOKIE = os.getenv('PELOTON_SESSION_ID')
CHALLENGE_START = datetime.datetime(2021, 11, 22, 0, 0)
USER_DICT = {
    '32df2a456cd94a77bbf3a6c32af6cb26': 'Nicki_Cycology',
    '945ba7f2f9144c45b6c2c74c748f107b': 'irish_claire',
    'c90e078b1ae442d4a7b827ae4dce7a62': 'beingmybestself',
    '31686e4e13b54d758d8fe36dd79cbf5a': 'BecsDX',
    'ed7fcf56ee8c49fb92ebb97cb3d8311e': 'nomes79',
    '3f7c8144aed64e97888d4a71545e5da3': 'Lee_Lee6',
    'f9761e7da1cd4eb8a7549fecf92598d6': 'lockandloaded',
    'd6516453101c4a76b196957118ebb486': 'Sweaty_Petty',
    'f7e76eb36a464a16b0a0c25d585cf8b0': 'NatSandford',
    '1e94855281a449498a36f17b1fefec2d': 'riaj44',
    'ba575e119e90443dbf39f2a8ebc2bb0f': 'Clarabellaton',
    'e7336ba47aca45d2a2be42ea9faf8c35': 'CruellaDeSpin',
    '925f924297934aabba1f738bd9d89522': 'pastheicecream',
    '560ef299756044cda5e50ccad8d5f89c': 'PhilH79',
    'ac540877948e4a7e8149d5abd87bc6ce': 'GingerNut1',
    '530639823f514afd98cb309d6d82e116': 'WeMoveTogether',
    'f953affc0d68461cbb2fa0c2b3187aab': 'littlesid1',
    'a241748577e241e597d36630f97f06ea': 'CrystalMet',
    '8b09d1313f04427a9bcdf51bb5ef0799': 'Kay_UK',
    '6d5ad73229334f08805579790f755516': 'allycatty',
    'e56af6663ccc4bc6b6417e3079fa074a': 'Charlie_73',
    '5f92c512d89b4e9ab4d8a3c074198b88': 'louise12112',
    'ad3f1733b146487abef1d7375873e661': 'Twinmum23',
    '346a716b00b44069b83d67f5cdf64aad': 'Natt82',
    '814d84035a694053a337829c108826e6': 'Julesymc22',
    '33ec6ab574e84ccaa137f7d25409d459': 'amyridesuk',
    '85a87f4d37014a8596f577e2b531dc0d': 'Wupsadaisy',
    '95e1b043cc2040c7af11a1e0376fd2f7': 'MissLianneJo',
    'a84860ef1cb6412882a1d12f0bdb133b': 'JacTay',
    'cfbe2ff87f904ecbb7f7721152c27a18': 'GinaUK',
    '13e21c19d8bc4645a935d32d3311613e': 'PassTheDutchie',
    'fb16f711d0ff42e3ac46e05fe9137492': 'Skyline_Pigeon',
    'ab4dd8ba84fd483c8ab05bc24b722c74': 'what_katy_did',
    'a8771c58f85c4471a26fa7faa7f879d4': 'julette45',
    '0c01d93de3b949818f4d9e585c2e2a5d': 'HappySpinRunner',
    '9e3d2241afc8449abd8ad5cb40450c08': 'Ukmumof3_trying',
    '649caab816b54321b3e200b2f993921f': 's5stw',
    'e611dd125b0b438b92e5c09f764269ec': 'sweatwithsteph',
    'f3a75d4cc8f34ed5812cb6ca9a63b50c': 'taz520',
    'ade268b8be814472aaa591ced1bf6941': 'careskell'
}
RUN_DICT = {
    1: {
        'start': datetime.datetime(2021, 11, 22, 0, 0),
        'end': datetime.datetime(2021, 11, 29, 0, 0),
        'runs': {
            'f28a1a8788ca4ac5a72deed1e1171b2b': '20 min recovery run - Susie Chan - 23/10/21',
            'ef73518d446f4c5b83c2cfc0ce951a81': '30 min endurance run - Becs Gentry - 3/11/21',
            'dc35da04423644f08e07a9b29b656f07': '30 min endurance run - Matt Wilpers - 7/9/21'
        }
    },
    2: {
        'start': datetime.datetime(2021, 11, 29, 0, 0),
        'end': datetime.datetime(2021, 12, 6, 0, 0),
        'runs': {
            'ff5dca33e7b647deb3c6bfc19763a5e4': '30 min endurance run - Selena Samuela - 14/3/21',
            'a7fca7df520742b5af771c8b12b72926': '30 min progression run - Becs Gentry - 9/7/21',
            'b9bfcfda74c64c639d4510987f6b4368': '45 min endurance run - Matt Wilpers - 7/6/21'
        }
    },
    3: {
        'start': datetime.datetime(2021, 12, 6, 0, 0),
        'end': datetime.datetime(2021, 12, 13, 0, 0),
        'runs': {
            '79ac1f29dd7d4c30820f048831c0bf3a': '30 min you can run: form  - Matt Wilpers - 23/4/21',
            '9aafb3a29e2e482bac4cc46e716db77b': '45 min NYC Marathon simulation run - Robin Arzon - 7/10/19',
            'e4229c0132fc4c5d998693c7d044afb2': '30 min intervals run - Olivia Amato - 16/6/21'
        }
    },
    4: {
        'start': datetime.datetime(2021, 12, 13, 0, 0),
        'end': datetime.datetime(2021, 12, 20, 0, 0),
        'runs': {
            'ed8a76e5590c469c9e9067a3dbae0d24': '30 min recovery run - Matt Wilpers - 3/8/20',
            '144a8ec7f56d4949a1fdd1b22c7aaee2': '30 min tempo run - Olivia Amato - 18/11/20',
            '0bf1c3f590784cd9b9392176d9170456': '60 min endurance run - Marcel Dinkins - 12/9/21',
            '6213fb1fbd9945c2985b3efde630cc0b': '60 min endurance run - Susie Chan - 15/12/21'
        }
    },
    5: {
        'start': datetime.datetime(2021, 12, 20, 0, 0),
        'end': datetime.datetime(2021, 12, 27, 0, 0),
        'runs': {
            'ac56d7fa789a43c9a7321beafbd29e97': '30 min HIIT run - Robin Arzon - 23/9/19',
            '0be5c37b63164379a885d8c6f8873002': '60 min NYC Marathon simulation run - Becs Gentry - 1/11/20',
            '8db4bbcd0232457f97071a86a0f79180': '45 min endurance run - Selena Samuela - 22/12/20',
            '8b73ca8b875d4a0bbd6b3fc517ee59fa': '45 min endurance run - Becs Gentry - 23/12/21'
        }
    },
    6: {
        'start': datetime.datetime(2021, 12, 27, 0, 0),
        'end': datetime.datetime(2022, 1, 3, 0, 0),
        'runs': {
            'e1cfa230fa6842cfb8bce724ab171ce3': '30 min recovery run - Becs Gentry - 28/10/19',
            '27339dae48084112bbc98ae246c32bea': '30 min endurance run - Matt Wilpers - 10/8/20',
            '549de6c8c6dc42789d9088dfafaac015': '45 min endurance run - Matt Wilpers - 24/9/21'
        }
    }
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
    total_run_counter = 0
    run_week_counter_dict = {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {}
    }
    for activity in user_activities:
        if activity['metrics_type'] != 'running' and activity['status'] != 'COMPLETE':
            continue
        activity_class_id = activity['ride']['id']
        activity_time = datetime.datetime.utcfromtimestamp(activity['start_time'])

        for run_week, run_week_dict in RUN_DICT.items():
            if run_week_dict['start'] < activity_time < run_week_dict['end']:
                if activity_class_id in run_week_dict['runs'].keys():
                    distance = get_distance_for_activity(activity)

                    print(
                        f"Found matching activity for {user_name} - Week {run_week} - {run_week_dict['runs'][activity_class_id]} - {distance}Mi")

                    # Deal with people doing the same run twice
                    if activity_class_id in run_week_counter_dict[run_week]:
                        print(f"Found multiple attempts for {run_week_dict['runs'][activity_class_id]}")
                        if run_week_counter_dict[run_week][activity_class_id] > distance:
                            print(f"This one is shorter, ignoring")
                            break
                        else:
                            print(f"This one is longer, overwriting")
                            distance_total -= run_week_counter_dict[run_week][activity_class_id]
                            total_run_counter -= 1

                    if is_activity_pr(activity):
                        print(f"PR ALERT!!!")
                        pr_counter += 1

                    distance_total += distance
                    run_week_counter_dict[run_week][activity_class_id] = distance
                    total_run_counter += 1
                break

    completed_challenge = True
    for run_week, run_week_activities in run_week_counter_dict.items():
        if len(run_week_activities) < 3:
            print(f'WARNING: User {user_name} did {len(run_week_activities)} in week {run_week}')
            completed_challenge = False
        elif len(run_week_activities) > 3:
            print(f'WARNING: User {user_name} did {len(run_week_activities)} in week {run_week}')
    return distance_total, pr_counter, completed_challenge, total_run_counter


def get_distance_for_activity(activity):
    distance_response = requests.get(
        f"{API_BASE}workout/{activity['id']}/performance_graph?every_n=5",
        cookies={'peloton_session_id': COOKIE}
    )
    distance_response_object = distance_response.json()
    for distance_response_summary in distance_response_object['summaries']:
        if distance_response_summary['slug'] == 'distance':
            return distance_response_summary['value']

    return 0


def is_activity_pr(activity):
    workout_response = requests.get(
        f"{API_BASE}workout/{activity['id']}",
        cookies={'peloton_session_id': COOKIE}
    )
    workout_response_object = workout_response.json()
    if 'achievement_templates' in workout_response_object:
        for achievement in workout_response_object['achievement_templates']:
            if achievement['slug'] == 'best_output':
                return True

    return False


if __name__ == '__main__':
    total_challenge_distance = 0
    total_challenge_runs = 0
    with open('savannah_run.csv', 'w', newline='') as csv_file:
        fieldnames = ['Username', 'Distance (Miles)', 'PRs', 'Completed Challenge']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for user_id, user_name in USER_DICT.items():
            user_distance, user_prs, completed_challenge, total_runs = get_total_distance(user_id, user_name)
            print(f"Total distance for {user_name} is {round(user_distance, 2)}Mi - They got {user_prs} PRs")
            writer.writerow(
                {
                    'Username': user_name,
                    'Distance (Miles)': round(user_distance, 2),
                    'PRs': user_prs,
                    'Completed Challenge': completed_challenge
                }
            )
            if not completed_challenge:
                print(f"User {user_name} did not complete the challenge but distance was {round(user_distance, 2)}Mi")
            total_challenge_distance += user_distance
            total_challenge_runs += total_runs
    print(f"Total Challenge Distance was {total_challenge_distance}Mi")
    print(f"Total Challenge Runs was {total_challenge_runs}")
