SOURCES = {
"Satellite Tracking":[
("Look4Sat","https://github.com/rt-bishop/Look4Sat"),
("SatNOGS","https://satnogs.org/"),
("Gpredict","https://oz9aec.dk/gpredict"),
("Find Satellites","https://www.find-satellites.com/"),
("AGSatTrack","https://agsattrack.com/"),
("CelesTrak","https://celestrak.org/"),
("N2YO","https://www.n2yo.com/"),
("JSatTrak","https://gano.name/shawn/JSatTrak/"),
("OrbTrack","https://www.orbtrack.org/"),
("Heavens-Above","https://www.heavens-above.com/"),
("In-The-Sky","https://in-the-sky.org/"),
],
"Orbital Intelligence":[
("Space-Track","https://www.space-track.org/"),
("CelesTrak","https://celestrak.org/"),
("N2YO","https://www.n2yo.com/"),
("Heavens-Above","https://www.heavens-above.com/"),
("AMSAT-UK","https://amsat-uk.org/beginners/satellite-tracking/"),
("Jonathan's Space Report","http://www.planet4589.org/"),
("Gunter's Space Page","https://space.skyrocket.de/index.html"),
],
"Visualization":[
("LeoLabs","https://platform.leolabs.space/visualization"),
("Stuff in Space","http://stuffin.space/"),
("ESRI Satellite Map","https://maps.esri.com/rc/sat2/index.html"),
("ESRI Satellite Explorer","https://geoxc-apps.bd.esri.com/space/satellite-explorer/"),
("Starlink Map","https://satellitemap.space/"),
("Find Starlink","https://findstarlink.com/"),
("ISS Tracker","http://www.isstracker.com/"),
("In-The-Sky Satellite Map","https://in-the-sky.org/satmap_worldmap.php"),
],
"Earth Observation":[
("NASA Worldview","https://worldview.earthdata.nasa.gov/"),
("NASA Earthdata Search","https://search.earthdata.nasa.gov/"),
("ESA Earth Observation","https://earth.esa.int/eogateway"),
("Radiant Earth","https://www.radiant.earth/"),
("EO Browser","https://apps.sentinel-hub.com/eo-browser/"),
("Sentinel Hub","https://www.sentinel-hub.com/explore/eobrowser/"),
("EOS LandViewer","https://eos.com/landviewer/"),
("Mapbox","https://www.mapbox.com/"),
("ArcGIS Map Viewer","https://www.arcgis.com/home/webmap/viewer.html"),
("Maxar","https://discover.maxar.com/"),
("Soar Earth","https://soar.earth/"),
("ArcGIS Wayback","https://livingatlas.arcgis.com/wayback/"),
("ESA SNAP","https://step.esa.int/main/toolboxes/snap/"),
],
"Space & Astronomy":[
("Stellarium","https://stellarium-web.org/"),
("NASA Moon Trek","https://trek.nasa.gov/moon/"),
("NASA Mars Trek","https://trek.nasa.gov/mars/"),
("TheSkyLive","https://theskylive.com/3dsolarsystem"),
("Solar System Scope","https://www.solarsystemscope.com/"),
("100,000 Stars","https://stars.chromeexperiments.com/"),
("MoonCalc","https://www.mooncalc.org/"),
("SunCalc","https://www.suncalc.org/"),
("Aurora Forecast","https://auroraforecast.space/"),
("Wikimapia","https://wikimapia.org/"),
],
"References":[
("Open Cosmos","https://www.open-cosmos.com/"),
("SatDump","https://www.satdump.org/"),
("NASA ISS Reference Guide","https://www.nasa.gov/pdf/508318main_ISS_ref_guide_nov2010.pdf"),
("NASA ISS Guide Utilization Edition","https://www.nasa.gov/sites/default/files/atoms/files/np-2015-05-022-jsc-iss-guide-2015-update-111015-508c.pdf"),
("Mission Patches","http://www.seasky.org/space-exploration/mission-patches-menu.html"),
]
}

def run(target="all"):
    return {
        "module":"satellite_sources",
        "target":target,
        "total_sources":sum(len(v) for v in SOURCES.values()),
        "categories":{
            k:[{"name":n,"url":u} for n,u in v]
            for k,v in SOURCES.items()
        }
    }
