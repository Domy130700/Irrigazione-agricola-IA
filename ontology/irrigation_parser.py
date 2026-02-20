import os
import xml.etree.cElementTree as ET
from tkinter import Tk, filedialog

def elimina_duplicati(x):
    return list(dict.fromkeys(x))

def pulisci_stringa(s):
    return s.replace(" ", "_").lower()

def parse_osm_irrigation():
    # Selezione del file XML (map.xml o campo_x.xml)
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        initialdir="ontology/map", 
        title="Seleziona Mappa Irrigazione (XML)",
        filetypes=(("XML files", "*.xml"), ("all files", "*.*"))
    )
    
    if not file_path:
        print("Nessun file selezionato.")
        return

    tree = ET.parse(file_path)
    root_xml = tree.getroot()

    nodi_per_prolog = {}
    condotte_per_prolog = []

    # 1. Lettura dei NODI (Valvole, Sensori, Punti)
    for node in root_xml.findall('node'):
        node_id = node.get('id')
        lat = node.get('lat')
        lon = node.get('lon')
        
        presenza_elettrovalvola = "0"
        nome_punto = f"punto_{node_id}"
        
        for tag in node.findall('tag'):
            # --- ADATTAMENTO CHIAVE ---
            # Se nel XML c'è 'traffic_signals', per noi è una Elettrovalvola
            if tag.get("v") == "traffic_signals": 
                presenza_elettrovalvola = "1"
            
            # Supporto anche per tag corretti se presenti
            if tag.get("k") == "irrigation" and tag.get("v") == "valve":
                presenza_elettrovalvola = "1"

            if tag.get("k") == "name":
                nome_punto = pulisci_stringa(tag.get("v"))

        nodi_per_prolog[node_id] = {
            "id": node_id,
            "lat": lat,
            "lon": lon,
            "valvola": presenza_elettrovalvola,
            "nome": nome_punto,
            "condotte": []
        }

    # 2. Lettura delle CONDOTTE (Way)
    for way in root_xml.findall('way'):
        way_id = way.get('id')
        nome_condotta = f"condotta_{way_id}"
        nodi_della_condotta = []

        for tag in way.findall('tag'):
            if tag.get("k") == "name":
                nome_condotta = pulisci_stringa(tag.get("v"))

        for nd in way.findall('nd'):
            ref = nd.get('ref')
            nodi_della_condotta.append(ref)
            if ref in nodi_per_prolog:
                nodi_per_prolog[ref]["condotte"].append(nome_condotta)

        condotte_per_prolog.append({
            "id": nome_condotta,
            "nodi": nodi_della_condotta
        })

    # Creazione cartella se non esiste
    os.makedirs("KB/prolog/class_value", exist_ok=True)

    # 3. Scrittura file Prolog: CONDOTTA
    with open("KB/prolog/class_value/condotta.pl", "w") as f:
        f.write(":- dynamic prop/3.\n\n")
        for c in condotte_per_prolog:
            f.write(f"prop({c['id']}, tipo, condotta).\n") 
            nodi_str = str(c['nodi']).replace("'", "")
            f.write(f"prop({c['id']}, nodi_collegati, {nodi_str}).\n")

    # 4. Scrittura file Prolog: PUNTO IRRIGAZIONE
    with open("KB/prolog/class_value/punto_irrigazione.pl", "w") as f:
        f.write(":- dynamic prop/3.\n\n")
        for n_id in nodi_per_prolog:
            n = nodi_per_prolog[n_id]
            # Scriviamo il nodo se è collegato a condotte o se è un punto isolato rilevante
            if len(n["condotte"]) > 0 or n["valvola"] == "1":
                condotte_list = "[" + ",".join(n["condotte"]) + "]"
                f.write(f"prop({n_id}, tipo, punto_irrigazione).\n") 
                f.write(f"prop({n_id}, condotte_attestate, {condotte_list}).\n")
                f.write(f"prop({n_id}, dispositivo_controllo, {n['valvola']}).\n")
                f.write(f"prop({n_id}, lat, {n['lat']}).\n")
                f.write(f"prop({n_id}, lon, {n['lon']}).\n")
                f.write(f"prop({n_id}, nome, '{n['nome']}').\n\n")

    print(f"✅ Parsing completato! Generati condotta.pl e punto_irrigazione.pl")
    
if __name__ == "__main__":
    parse_osm_irrigation()