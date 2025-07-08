import osmnx as ox
import networkx as nx
import folium
from folium.plugins import FloatImage

# Ort festlegen
ort = "Mauthausen, Austria"

# Graphen laden
rad_graph = ox.graph_from_place(ort, network_type="bike")
lauf_graph = ox.graph_from_place(ort, network_type="walk")

# Abschnitt 1: Radfahren
rad_coords = [
    (48.24528510915935, 14.506265553390474),  # Punkt 1: Hinterholz
    (48.23854019421386, 14.559327697631678),  # Punkt 2: Albern
    (48.2450841545805, 14.544986505056013),  # Punkt 3: Obersebern
]

# Abschnitt 2: Laufen
lauf_coords = [
    (48.2450841545805, 14.544986505056013),  # Punkt 3: Obersebern
    (48.25182199201539, 14.542427232949514),  # Punkt 4: Reiferdorf
    (48.2450841545805, 14.544986505056013),  # Punkt 5: Mauthausen
]

# Route berechnen
def berechne_route(graph, koordinaten):
    route_coords = []
    for i in range(len(koordinaten) - 1):
        start = koordinaten[i]
        ziel = koordinaten[i + 1]
        start_node = ox.nearest_nodes(graph, start[1], start[0])
        ziel_node = ox.nearest_nodes(graph, ziel[1], ziel[0])
        teilroute = nx.shortest_path(graph, start_node, ziel_node, weight="length")
        coords = [(graph.nodes[n]['y'], graph.nodes[n]['x']) for n in teilroute]
        route_coords.extend(coords)
    return route_coords

# Routen generieren
radweg = berechne_route(rad_graph, rad_coords)
laufweg = berechne_route(lauf_graph, lauf_coords)

# Karte
karte = folium.Map(location=rad_coords[0], zoom_start=13)

# Linien
folium.PolyLine(radweg, color="magenta", weight=5, tooltip="Radweg").add_to(karte)
folium.PolyLine(laufweg, color="orange", weight=5, tooltip="Laufweg").add_to(karte)

folium.PolyLine(
    radweg,
    color="magenta",
    weight=5,
    tooltip=folium.Tooltip("Radstrecke", permanent=True)
).add_to(karte)



# Marker mit Beschreibung
beschreibungen = [
    "Punkt 1: Freibad (Start Rad)",
    "Punkt 2: Albern",
    "Punkt 3: Karosserie Steinkellner",
    "Punkt 4: Einbahnstraße",
    "Punkt 5: Karosserie Steinkellner (Ziel)"
]
alle_punkte = rad_coords + lauf_coords[1:]  

for idx, coord in enumerate(alle_punkte):
    folium.Marker(
        location=coord,
        popup=beschreibungen[idx],
        tooltip=beschreibungen[idx],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(karte)

# Legende 
legende_html = '''
<div style="
    position: fixed;
    bottom: 30px;
    right: 30px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:14px;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
<b>Legende:</b><br>
<span style="color:magenta;">■</span> Radweg<br>
<span style="color:orange;">■</span> Laufweg<br><br>
<b>Punkte:</b><br>
1. Freibad (Start Rad)<br>
2. Albern<br>
3. Karosserie Steinkellner<br>
4. Einbahnstraße<br>
5. Karosserie Steinkellner (Ziel)
</div>
'''

karte.get_root().html.add_child(folium.Element(legende_html))

# Speichern
karte.save("karte_mit_legende.html")
print("Karte gespeichert als 'karte_mit_legende.html'")
