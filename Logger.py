import csv
import time


def WriteInLog(loglist):
    zeit = time.asctime().replace(" ","_")
    with open(r'C:\Users\valen\OneDrive\Dokumente\Berufsschule\LF8\LOGGER.csv', 'a', newline='') as csvdatei:
        writer = csv.writer(csvdatei)
        writer.writerow([zeit,loglist])
    
