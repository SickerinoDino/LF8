from psutil import *
import tkinter as tk
import Logger 


#Liste für LOG Datei wie Variable schon sagt du Idiot
loglist = []

#Erstellen des Hauptfensters und Festlegen des Titels und der Größe
root = tk.Tk()
root.title("System-Monitor")
root.geometry("400x300")

#Erstellen des Alert-Fensters und Ausblenden, damit es nicht sichtbar ist
alert = tk.Toplevel()
alert.title("Warnung")
alert.geometry("400x300")
alert.withdraw()

#Erstellen der Scrollbar für das Text-Widget im alert-Fenster
alert_scrollbar = tk.Scrollbar(alert)
alert_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#Erstellen des Text-Widgets für die Fehlermeldung im Alert-Fenster und Verknüpfung mit dem Scrollbar
alert_text = tk.Text(alert, height=10, yscrollcommand=alert_scrollbar.set)
alert_text.pack(side=tk.LEFT, fill=tk.BOTH)
alert_scrollbar.config(command=alert_text.yview)

#Funktion, die aufgerufen wird, wenn eine kritische Systeminformation erfasst wird. Sie öffnet das Alert-Fenster und gibt eine Fehlermeldung aus.
def fehlermeldung(fcode, fehler):
    alert.deiconify()
    if fcode == "Netzwerk":
        alert_text.insert(tk.END,"Keine Internetverbindung!\n")
    else:
        alert_text.insert(tk.END, f"{fcode} ist im kritischen Bereich! mit {fehler}%\n")
    
# Funktionen zur Ausgabe der Systeminformationen
# refreshed die ausgegebenen CPU-Daten aller 1000ms 
def update_cpu():
    cpu_perc = cpu_percent()
    cpu_label.config(text=f"CPU-Auslastung: {cpu_perc}%")
    root.after(1000, update_cpu)
    if cpu_perc >= 90:
        fehlermeldung("CPU", cpu_perc)
    loglist.append(cpu_perc)

# refreshed die ausgegebenen Memory-Daten aller 1000ms 
def update_ram():
    memory_usage = virtual_memory().used
    memory = memory_usage/1024/1024/1024
    memory_perc = virtual_memory().percent
    ram_label.config(text=f"Arbeitsspeicher-Auslastung: {round(memory,3)} GiB")
    root.after(1000, update_ram)
    if memory_perc >= 90:
        fehlermeldung("RAM", memory_perc)
    loglist.append(memory_perc)

# refreshed die ausgegebenen Festplatten-Daten aller 1000ms 
def update_disk():
    disk_par = disk_partitions()
    for i in range(len(disk_par)):
        disk_use = disk_usage(disk_par[i][0]).used/1024/1024/1024
        disk_total = disk_usage(disk_par[i][0]).total/1024/1024/1024
        disk_perc = disk_usage(disk_par[i][0]).percent
        disk_label.config(text=f"{disk_par[i][0]} {round(disk_use,3)} GiB frei von {round(disk_total,3)} GiB: {disk_perc}%")
    root.after(1000, update_disk)
    if disk_perc >= 90 :
        fehlermeldung("Disk", disk_perc)

# refreshed die ausgegebenen Network-Daten aller 1000ms 
def update_network():
    network_io_counters = net_io_counters()
    network_usage = (network_io_counters.bytes_sent + network_io_counters.bytes_recv)/1024/1024/1024
    network_label.config(text=f"Netzwerkauslastung: {round(network_usage,3)} GB")
    root.after(1000, update_network)
    if network_io_counters.bytes_recv == 0:
        fehlermeldung("Netzwerk", 0)
    loglist.append(network_usage)
    Logger.WriteInLog(loglist)
    loglist.clear()

#Erstellen der Labels für die verschiedenen Systeminformationent und Verbindung mit dem Root-Fenster.
cpu_label = tk.Label(root, text="CPU-Auslastung: ")
cpu_label.pack()

ram_label = tk.Label(root, text="Arbeitsspeicher-Auslastung: ")
ram_label.pack()

disk_label = tk.Label(root, text="Festplatten-Auslastung: ")
disk_label.pack()

network_label = tk.Label(root,text="Netzwerkauslastung: ")
network_label.pack()

# Funktionen zur Aktualisierung der Systeminformationen starten
root.after(1000, update_cpu)
root.after(1000, update_ram)
root.after(1000, update_disk)
root.after(1000, update_network)




root.mainloop()
