import time
import datetime
import os
import json
import pandas as pd

import api_client
from pdql_filteres import event_filters
from event_analyzer import dataparse, visualize


def run(custom_input_enabled=False):
    new_column_names = {
        "time": "Время",
        "event_src.host": "fortigate",
        "src.ip": "Атакующий",
        "object.type": "Сигнатура",
        "text": "Описание"
    }

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    current_time = time.localtime()
    formatted_time = time.strftime('_%d-%m-%Y_%H-%M-%S', current_time)

    output_file_pdf = os.path.join(output_dir, f'stats{formatted_time}.pdf')
    output_file_xlsx = os.path.join(output_dir, f'events{formatted_time}.xlsx')

    writer = pd.ExcelWriter(output_file_xlsx, engine='xlsxwriter')

    ip_whitelist = dataparse.parse_ip_file("config/filtered_addresses.txt")

    if custom_input_enabled:
        json_list = dataparse.csv_to_json_list("input.csv", ip_whitelist)
    else:
        json_list = get_json_list_from_API(ip_whitelist)

    df = dataparse.json_to_dataframe(json_list)
    dataparse.dataframe_to_excel(df, writer, 'Все события', new_column_names)
    dataparse.group_by_src_ip_to_excel(df, writer, 'Группировка по атакующим', new_column_names)
    dataparse.group_by_unique_src_ip(df, writer, 'Уникальные атакующие адреса', new_column_names)
    dataparse.group_by_unique_dst_combinations(df, writer, 'Уникальные ресурсы', new_column_names)
    dataparse.create_summary_statistics(df, writer, 'Статистика')

    writer._save()
    print(f"Saving the output to {output_file_xlsx}")

    visualize.visualize_data_to_pdf(json_list, output_file_pdf)
    print(f"Saving the output to {output_file_pdf}")

    print("\nDone!")


def get_json_list_from_API(ip_list):
    with open('config/credentials.json', 'r') as file:
        creds = json.load(file)

    ROOT_URL_API=creds["url_root_api"]
    USERNAME=creds["username"]
    PASSWORD=creds["password"]
    CLIENT_SECRET=creds["secret"]

    bearer_token = api_client.get_bearer_token(
        root_url_api=ROOT_URL_API,
        username=USERNAME,
        password=PASSWORD,
        client_secret=CLIENT_SECRET
    )

    time_from = int(time.mktime(time.strptime('2024-06-23 12:00:00', '%Y-%m-%d %H:%M:%S')))
    time_to = int(time.mktime(time.strptime('2024-06-25 12:00:00', '%Y-%m-%d %H:%M:%S')))

    events_buffer = []

    while True:

        events, total_count, last_incident_time = api_client.get_events_by_filter(
            root_url_api=ROOT_URL_API,
            access_token=bearer_token,
            filter=event_filters.fortinet_attacks,
            time_from=time_from,
            time_to=time_to
        )

        print(total_count, last_incident_time)
        events_buffer += events

        if total_count <= 10000:
            break

        time_to = int(datetime.datetime.strptime(last_incident_time, "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp()) + 15000

    unique_events = {}
    for event in events_buffer:
        uuid = event['uuid']
        if uuid not in unique_events:
            unique_events[uuid] = event

    total_events = list(unique_events.values())

    count = 0
    ip_cache = {}
    for event in total_events:
        src_ip = event.get('src.ip')
        if dataparse.ip_in_list(src_ip, ip_list):
            total_events.remove(event)
        elif src_ip:
            if src_ip not in ip_cache:
                count += 1
                ip_cache[src_ip] = api_client.get_country_by_ip(src_ip)
            event['src.geo.country'] = ip_cache[src_ip]

    print(len(total_events))
    print(f"{count} IPs")
    return total_events
