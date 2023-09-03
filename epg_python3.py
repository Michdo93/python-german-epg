import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Aktuelles Datum in gewünschtem Format erstellen
current_date = datetime.now().strftime("%Y-%m-%d")

# Basis-URL für TV-Programm
base_url = "https://www.tvspielfilm.de/tv-programm/tv-sender/"

# Anzahl der Seiten, die du abrufen möchtest
num_pages = 5

# Liste für die Sender und ihre Informationen erstellen
sender_info_list = []

# Gehe durch die Seiten
for page in range(1, num_pages + 1):
    # URL für die aktuelle Seite erstellen
    url = f"{base_url}?page={page}&date={current_date}"

    # Eine GET-Anfrage an die URL senden
    response = requests.get(url)

    # Den HTML-Inhalt der Seite abrufen
    html_content = response.text

    # BeautifulSoup verwenden, um die HTML-Seite zu analysieren
    soup = BeautifulSoup(html_content, "html.parser")

    # Die Senderliste auswählen (dies kann je nach Website variieren)
    # Hier verwenden wir die Klasse "heading-link", um Sender auszuwählen
    sender_list = soup.find_all(class_="heading-link")

    i = 0
    # Gehe durch die gefundenen Sender und sammle ihre Informationen
    for sender in sender_list:
        i = i + 1
        sender_name = sender.text.strip()
        sender_info = {sender_name: {"Prime Time Highlight": [], "Vormittag von 5 bis 11 Uhr": [], "Mittag von 11 bis 14 Uhr": [],
                       "Nachmittag von 14 bis 18 Uhr": [], "Vorabend von 18 bis 20 Uhr": [],
                       "Prime Time von 20 bis 0 Uhr": [], "Nachts von 0 bis 5 Uhr": []}}

        # Finde die Div-Container für die verschiedenen Zeiträume
        slot_ids = ["5", "11", "14", "18", "20", "0"]

        # Die Senderliste auswählen (dies kann je nach Website variieren)
        # Hier verwenden wir die Klasse "block-1", um Sender auszuwählen
        sender_blocks = soup.find_all(class_="block-1")
        j = 0
        # Gehe durch die gefundenen Sender und ihre Informationen sammeln
        for sender_block in sender_blocks:
            j = j + 1
            if i == j:
                # Finde die Zeit und den Titel innerhalb des aktuellen Senderblocks
                time = sender_block.find(class_="time").text.strip()
                title = sender_block.find(class_="title").text.strip()

                # Finde das <source> Tag, um die image_url zu extrahieren
                source_tags = sender_block.find_all("source")
                image_url = None

                for source_tag in source_tags:
                    if "image/jpeg" in source_tag.get("type", ""):
                        image_url = source_tag.get("srcset").split(" ")[0]
                        break

                # Füge die Informationen zum Sender-Dictionary hinzu
                sender_info[sender_name]["Prime Time Highlight"].append({"Zeit": time, "Titel": title, "image_url": image_url})
            else:
                continue

        for slot_id in slot_ids:
            slot_div = soup.find(id=f"toggleslot-{slot_id}-p")
            if slot_div:
                li_elements = slot_div.find_all("li")
                for li_element in li_elements:
                    program_blocks = li_element.find_all(class_="program-block")
                    k = 0
                    for program_block in program_blocks:
                        k = k + 1
                        info_divs = program_block.find_all(class_="info")
                        for info_div in info_divs:
                            if i == k:
                                time = info_div.find(class_="time").text.strip()
                                title = info_div.find(class_="title").text.strip()
                                subtitle = info_div.find(class_="subtitle").text.strip()

                                # Bestimme den passenden Bereich (Zeitraum) basierend auf der Slot-ID
                                if slot_id == "5":
                                    sender_info[sender_name]["Vormittag von 5 bis 11 Uhr"].append({"Zeit": time, "Titel": title, "Subtitle": subtitle})
                                elif slot_id == "11":
                                    sender_info[sender_name]["Mittag von 11 bis 14 Uhr"].append({"Zeit": time, "Titel": title, "Subtitle": subtitle})
                                elif slot_id == "14":
                                    sender_info[sender_name]["Nachmittag von 14 bis 18 Uhr"].append({"Zeit": time, "Titel": title, "Subtitle": subtitle})
                                elif slot_id == "18":
                                    sender_info[sender_name]["Vorabend von 18 bis 20 Uhr"].append({"Zeit": time, "Titel": title, "Subtitle": subtitle})
                                elif slot_id == "20":
                                    sender_info[sender_name]["Prime Time von 20 bis 0 Uhr"].append({"Zeit": time, "Titel": title, "Subtitle": subtitle})
                                elif slot_id == "0":
                                    sender_info[sender_name]["Nachts von 0 bis 5 Uhr"].append({"Zeit": time, "Titel": title, "Subtitle": subtitle})

        # Füge das Sender-Dictionary zur Liste hinzu
        sender_info_list.append(sender_info)

# Gib die Liste der Sender und ihre Informationen aus
for sender_info in sender_info_list:
    print(sender_info)
