from flask import Flask, jsonify, Response
import csv
import os
import logging
import glob

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def read_csv(file_name):
    with open(file_name, 'r') as file:
        return file.read()

@app.route('/data/<date>/<hour>/<minute>')
def send_csv_data(date, hour, minute):
    hour = hour.zfill(2)
    minute = minute.zfill(2)

    pattern = f'traffic_data_{date}{hour}{minute}*.csv'
    file_path = os.path.join('./csv/', pattern)

    logging.info(f"Recherche du fichier avec le motif : {pattern}")

    matching_files = glob.glob(file_path)

    if matching_files:
        logging.info(f"Fichier trouvé : {matching_files[0]}")
        csv_data = read_csv(matching_files[0])
        return Response(csv_data, mimetype='text/plain')
    else:
        logging.error("Fichier non trouvé")
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
