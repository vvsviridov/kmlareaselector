import unittest
import csv

from lxml import etree
from shapely.geometry import Point, Polygon

from areaselector import (
    Area,
    _get_xml_tag_text,
    _create_point,
    _create_polygon,
    _get_point_from_line,
    _check_area_inclusion
)


XML = """
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
"""

CSV = """Pin0;91.84942315017878;31.5583711033568
Pin1;95.98483861545775;28.84807135882143
Pin2;85.33359958283256;30.05070454448402"""

class TestAreaSelector(unittest.TestCase):

    def setUp(self):
        self.tree = etree.fromstring(XML)
        self.placemarks = self.tree.xpath('.//*[local-name()="Placemark"]')
        self.csv = csv.reader(CSV.split('\n'), delimiter=';')
    
    def test_tagsTextExists(self):
        area_name = _get_xml_tag_text(self.placemarks[0], tag='name')
        self.assertEqual(area_name, 'Area2', 'Area name should be Area2')
    
    def test_tagsTextRaises(self):
        self.assertRaises(IndexError, _get_xml_tag_text, self.placemarks[0], 'qwe')
    
    def test_tagsTextNotExists(self):
        coordinates = _get_xml_tag_text(self.placemarks[-1], tag='coordinates')
        self.assertEqual(coordinates, '',
                         'Coordinates name should be empty string')

    def test_createPointInstance(self):
        point = _create_point('79.95474,31.659017,0')
        self.assertIsInstance(point, Point, 'Result should be Point')

    def test_createPointRaises1(self):
        self.assertRaises(ValueError, _create_point, '')

    def test_createPointRaises2(self):
        self.assertRaises(ValueError, _create_point, 'asd,qwe,123')

    def test_createPolygonInstance(self):
        polygon = _create_polygon(self.placemarks[0])
        self.assertIsInstance(polygon,
                              Polygon, 'Result should be Polygon')

    def test_createPolygonEmpty(self):
        self.assertTrue(_create_polygon(self.placemarks[2]).is_empty)
    
    def test_getPointFromLine(self):
        self.assertEqual(
            _get_point_from_line(next(self.csv), -1, -2),
            _create_point('91.84942315017878,31.5583711033568,0')
        )
    
    def test_checkAreaIncluded(self):
        line = next(self.csv)
        line = next(self.csv)
        line = next(self.csv)
        areas = [Area(
            _get_xml_tag_text(self.placemarks[0], 'name'),
            _create_polygon(self.placemarks[0]),
            )]
        check = _check_area_inclusion(line, areas, -1, -2)
        self.assertEqual(
            check[-1],
            areas[0].name
        )
    
    def test_checkAreaNotIncluded(self):
        line = next(self.csv)
        line = next(self.csv)
        line = next(self.csv)
        areas = [Area(
            _get_xml_tag_text(self.placemarks[1], 'name'),
            _create_polygon(self.placemarks[1]),
            )]
        check = _check_area_inclusion(line, areas, -1, -2)
        self.assertNotEqual(
            check[-1],
            areas[0].name
        )


if __name__ == '__main__':
    unittest.main()