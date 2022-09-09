# Check if areas contains points

```
usage: areaselector.py [-h] -c CSV -k KML [-x LAT] [-y LON] [-d DLM]

Setting area inclusion

options:
  -h, --help         show this help message and exit
  -c CSV, --csv CSV  Path to CSV file
  -k KML, --kml KML  Path to KML file
  -x LAT, --lat LAT  Latitude field position
  -y LON, --lon LON  Longitude field position
  -d DLM, --dlm DLM  CSV delimiter

If unspecified - [lat, lon] is last two CSV fields
```

## Example
python .\areaselector.py --kml .\areas.kml --csv points.csv --lat 1 --lon 2

Where KML file is (exported from Google Earth):
```xml
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <Folder>
        <Placemark>
            <name>Area2</name>
            <styleUrl>#m_ylw-pushpin</styleUrl>
            <Polygon>
                <tessellate>1</tessellate>
                <outerBoundaryIs>
                    <LinearRing>
                        <coordinates>
                            79.95474557842684,31.65901703907556,0 78.81974752325115,26.64835913696043,0 82.45019300573046,24.87205053786336,0 87.92836063354439,24.93430166942352,0 88.95463906871693,28.10965761073364,0 88.13783683298331,32.46810427636363,0 84.03157778885559,33.22063458708855,0 79.95474557842684,31.65901703907556,0 
                        </coordinates>
                    </LinearRing>
                </outerBoundaryIs>
            </Polygon>
        </Placemark>
        <Placemark>
            <name>Area1</name>
            <styleUrl>#m_ylw-pushpin</styleUrl>
            <Polygon>
                <tessellate>1</tessellate>
                <outerBoundaryIs>
                    <LinearRing>
                        <coordinates>
                            90.82931735059036,29.41995980410493,0 90.46145353241529,26.12430611896649,0 92.45489541152537,23.47674797036035,0 99.21409133811221,23.73202491179474,0 99.38781381690829,27.29212019406671,0 95.55083577933901,31.65618310507069,0 90.82931735059036,29.41995980410493,0 
                        </coordinates>
                    </LinearRing>
                </outerBoundaryIs>
            </Polygon>
        </Placemark>
        <Placemark>
            <name>Area0</name>
            <styleUrl>#m_ylw-pushpin</styleUrl>
            <Polygon>
                <tessellate>1</tessellate>
                <outerBoundaryIs>
                    <LinearRing>
                        <coordinates>
                        </coordinates>
                    </LinearRing>
                </outerBoundaryIs>
            </Polygon>
        </Placemark>
    </Folder>
</Document>
</kml>
```

And CSV file is:
```
Pin0;31.5583711033568;91.84942315017878
Pin1;28.84807135882143;95.98483861545775
Pin2;30.05070454448402;85.33359958283256
```

## Result

Result is the CSV file:
```
Pin0;31.5583711033568;91.84942315017878
Pin1;28.84807135882143;95.98483861545775;Area1
Pin2;30.05070454448402;85.33359958283256;Area2
```

`Area1` contains `Pin1` and `Area2` contains `Pin2`