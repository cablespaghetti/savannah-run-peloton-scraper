import datetime

import requests

API_BASE = 'https://api.onepeloton.co.uk/api/'
COOKIE = '584455b4a61846988936ee504407f2fd'
CHALLENGE_START = datetime.datetime(2021, 11, 22, 0, 0)


def get_users():
    return [
        '32df2a456cd94a77bbf3a6c32af6cb26',
    ]


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
        print(f"Got {len(activity_data_list)} workouts for {user_id}")
        print(f"Challenge start at {CHALLENGE_START.timestamp()}. Next timestamp {next_timestamp}.")
    return activity_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for user_id in get_users():
        user_activities = get_user_running_workouts(user_id)

        for activity in user_activities:
            if activity['metrics_type'] != 'running' and activity['status'] == 'COMPLETE':
                continue
            class_id = activity['ride']['id']
            pr = activity['is_total_work_personal_record']
            time = activity['start_time']

            distance_response = requests.get(
                f"{API_BASE}workout/{activity['id']}/performance_graph?every_n=5",
                cookies={'peloton_session_id': COOKIE}
            )
            distance_response_object = distance_response.json()
            for distance_response_summary in distance_response_object['summaries']:
                if distance_response_summary['slug'] == 'distance':
                    print(distance_response_summary['value'])