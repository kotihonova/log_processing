import argparse
import sys
from typing import Dict, List
import json
from tabulate import tabulate


def get_full_logs(files: List[str]) -> List:
    logs = list()
    for filename in files:
        try:
            with open(filename, 'r') as file:
                content = file.read()
                logs += parse_content(content)
        except FileNotFoundError as e:
            print(e)
    return logs


def parse_content(data) -> List:
    lines = data.strip().split('\n')
    logs = [json.loads(line.strip()) for line in lines]
    return logs


def generate_average_report(data) -> Dict:
    report = {}
    for item in data:
        url = item['url'].split('?')[0]
        if url not in report:
            report[url] = {
                'count': 1,
                'time': item['response_time']
            }
        else:
            report[url]['count'] += 1
            report[url]['time'] += item['response_time']

    for item in report:
        report[item]['time'] = str(round(report[item]['time'] / report[item]['count'], 3))
    return report


def get_report_for_table(data) -> List[List]:
    sorted_report = sorted(generate_average_report(full_logs).items(),
                           key=lambda x: x[1]['count'], reverse=True)
    report_for_table = [[item[0], item[1]['count'], item[1]['time']] for item in sorted_report]
    return report_for_table


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Report generator',
        description='Script for report generation')
    parser.add_argument('-f', '--filename', nargs='+')
    parser.add_argument('-r', '--report')
    args = parser.parse_args()

    full_logs = get_full_logs(args.filename)

    if args.report == 'average':
        print(tabulate(get_report_for_table(full_logs)))
    else:
        print('Report name not found', file=sys.stderr)
