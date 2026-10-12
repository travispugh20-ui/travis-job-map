import json,html,datetime,zoneinfo
d=json.load(open('/workspace/jobmap/applications.json'))
C={"applied":"#2a7de1","interview":"#f2a900","rejected":"#d33","offer":"#2a2"}
apps=sorted(d["applications"],key=lambda a:a["date"],reverse=True)
cnt={k:sum(a["status"]==k for a in apps) for k in C}
now=datetime.datetime.now(zoneinfo.ZoneInfo("America/Chicago")).strftime("%b %d, %Y %I:%M %p CT")
e=html.escape
rows="".join(f'<li onclick="go({i})"><b style="color:{C[a["status"]]}">●</b> <b>{e(a["company"])}</b> – {e(a["role"])}<br><small>{e(a["location"])}{" (approx.)" if a.get("approx") else ""} · {e(a["date"])} · {a["status"]} · {e(a["pay"])}{" · "+e(a["note"]) if a.get("note") else ""}</small></li>' for i,a in enumerate(apps))
out=f'''<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Travis's Job Applications</title>
<link rel=stylesheet href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>body{{margin:0;font-family:sans-serif}}#map{{height:60vh}}ul{{list-style:none;padding:0 10px}}li{{padding:8px 0;border-bottom:1px solid #ddd;cursor:pointer}}.h{{padding:10px}}@media(min-width:900px){{body{{display:flex}}#map{{height:100vh;flex:2}}#side{{flex:1;height:100vh;overflow:auto}}}}</style></head><body>
<div id=map></div><div id=side><div class=h><h2>Job Applications ({len(apps)})</h2>
{" · ".join(f'<span style="color:{C[k]}">●</span> {k}: {v}' for k,v in cnt.items())}<br><small>Last updated: {now}</small></div><ul>{rows}</ul></div>
<script>const A={json.dumps(apps)},C={json.dumps(C)},H={json.dumps(d["home"])};
const m=L.map('map');L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap'}}).addTo(m);
const M=A.map(a=>L.circleMarker([a.lat,a.lng],{{radius:10,color:'#fff',weight:2,fillColor:C[a.status],fillOpacity:.9}}).addTo(m).bindPopup(`<b>${{a.company}}</b><br>${{a.role}}<br>Applied: ${{a.date}}<br>Status: ${{a.status}}<br>Pay: ${{a.pay}}${{a.note?'<br>'+a.note:''}}${{a.approx?'<br><i>Location approximate</i>':''}}`));
L.marker([H.lat,H.lng]).addTo(m).bindPopup(H.label);
m.fitBounds(L.featureGroup(M).getBounds().pad(.2));function go(i){{m.setView(M[i].getLatLng(),11);M[i].openPopup();scrollTo(0,0)}}</script></body></html>'''
open('/workspace/jobmap/index.html','w').write(out);print("built",now)
