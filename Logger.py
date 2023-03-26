import csv
import time


def WriteInLog(loglist):
    zeit = time.asctime().replace(" ","_")
    with open(r'LOGGER.csv', 'a', newline='') as csvdatei:
        writer = csv.writer(csvdatei)
        writer.writerow([zeit,loglist])
    
