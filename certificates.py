import csv

from PIL import Image, ImageDraw, ImageFont


def get_text_offset(text, draw, font, width, height, offset_x=0, offset_y=0):
    width_text, height_text = draw.textsize(text, font)
    center_offset_x, center_offset_y = font.getoffset(text)
    width_text += center_offset_x
    height_text += center_offset_y
    top_left_x = width / 2 - width_text / 2
    top_left_y = height / 2 - height_text / 2
    return top_left_x + offset_x, top_left_y + offset_y


def render_duration(duration_string):
    duration_list = duration_string.split(':')
    return f'{duration_list[0]} Hours {duration_list[1]} Minutes'


def render_user_certificate(username, stats_dict):
    img = Image.open('certificate_background.png')
    img_draw = ImageDraw.Draw(img)
    width_image, height_image = img.size
    color = (0, 0, 0)

    username_font = ImageFont.truetype('PTSans', 65)
    username_location = get_text_offset('#' + username, img_draw, username_font, width_image, height_image, 0, 100)
    img_draw.text(username_location, '#' + username, font=username_font, fill=color)

    body_font = ImageFont.truetype('PTSans', 30)

    stats_column_1 = f'''
    Total Runs: {stats_dict['runs']}
    Total Distance: {stats_dict['distance']} Miles
    Total Duration: {render_duration(stats_dict['duration'])}
    Total Calories: {stats_dict['calories']}
    '''

    img_draw.text((20, 660), stats_column_1, font=body_font, fill=color, spacing=16)

    stats_column_2 = f'''
    Max Speed: {stats_dict['max_speed']} MPH
    Total Output: {stats_dict['total_output']} kJ
    '''
    if stats_dict['prs']:
        stats_column_2 += f"New PRs: {stats_dict['prs']}"
    img_draw.text((560, 660), stats_column_2, font=body_font, fill=color, spacing=16)
    img.save(f"certificates/{username}.png")


with open('savannah_run.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        row_stats_dict = {
            'runs': row['Runs'],
            'distance': row['Distance (Miles)'],
            'duration': row['Duration'],
            'calories': row['Calories'],
            'max_speed': row['Max Speed (MPH)'],
            'average_speed': row['Average Speed (MPH)'],
            'output': row['Average Output (Watts)'],
            'total_output': row['Total Output (kJ)'],
            'prs': int(row['PRs'])
        }
        render_user_certificate(row['Username'], row_stats_dict)
