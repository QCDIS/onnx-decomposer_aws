import csv
import os

import get_lambda_metrics
import sfn_constants

durations, durations_with_units, memories, memories_with_units = get_lambda_metrics.get_metrics()

if not os.path.exists(sfn_constants.METRICS_FOLDER):
    os.mkdir(sfn_constants.METRICS_FOLDER)

with open(sfn_constants.METRICS_FILE, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(sfn_constants.CSV_HEADERS)
    for i in range(len(durations)):
        for j in range(len(durations[i])):
            writer.writerow([i, j, durations[i][j], memories[i][j]])
