import csv

from argparse import ArgumentParser, Namespace
from shapely.geometry import Point, Polygon
from lxml import etree
from lxml.etree import _Element as XmlElement
from dataclasses import dataclass
from typing import Generator, List


@dataclass
class Area:
    name: str
    polygon: Polygon

_XPATH = './/*[local-name()=$tag]'


def _get_xml_tag_text(xml_element: XmlElement, tag: str) -> str:
    """Returns text from specified xml tag

    Args:
        place (XmlElement): Xml element
        tag (str): Tag name of xml element

    Returns:
        str: Text contained in specified tag
    """
    return xml_element.xpath(_XPATH, tag=tag)[0].text.strip()


def _create_point(coord: str) -> Point:
    """Creates Point object from string with coordinates
    '35.55926608650697,27.52840923934243,0'
    taken from kml/Placemark//coordinates

    Args:
        coord (str): String with coordinates

    Returns:
        Point: Point object
    """
    lon, lat, _ = coord.split(",")
    return Point(float(lat), float(lon))


def _create_polygon(place: XmlElement) -> Polygon:
    """Creates Polygon object from parsed list of coordinates

    Args:
        place (XmlElement): Placemark xml element

    Returns:
        Polygon: Polygon object
    """
    return Polygon(
        _create_point(coord)
        for coord in _get_xml_tag_text(place, 'coordinates').split()[:-1]
    )


def _get_areas_from_kml(kml_file: str) -> List[Area]:
    """Return Area list from kml file

    Args:
        kml_file (str): /path/to/kmlfile

    Returns:
        List[Area]: List of Area objects
    """
    root = etree.parse(kml_file)
    tree = root.getroot()
    return [
        Area(
            _get_xml_tag_text(place, 'name'),
            _create_polygon(place),
            )
        for place in tree.xpath(_XPATH, tag='Placemark')
    ]


def _get_point_from_line(line: List[str], lat: int, lon: int) -> Point:
    """Parsing latitude and longitude from csv line

    Args:
        line (List[str]): Csv line
        lat (int): Latitude position in csv line
        lon (int): Longitude position in csv line

    Returns:
        Point: Point object
    """
    return _create_point(
        f'{line[lon].replace(",", ".")},'
        f'{line[lat].replace(",", ".")},0'
    )


def _read_csv(csv_name: str, delimiter: str) -> Generator:
    """Return Generator object with list of csv lines

    Args:
        csv_name (str): /path/to/csvfile
        delimiter (str): Field delimiter used in csv

    Yields:
        Generator: Generator object
    """
    with open(csv_name, newline='', encoding='utf-8') as csvfile:
        csv_lines = csv.reader(csvfile, delimiter=delimiter)
        for line in csv_lines:
            yield line


def _write_csv(csv_name: str, delimiter: str, lines: List[List[str]]) -> None:
    """Writes modified lines to new csv file

    Args:
        csv_name (str): /path/to/csvfile
        delimiter (str): Field delimiter used in csv
        lines (List[List[str]]): List of csv lines
    """
    f_name_new = '{}_mod.{}'.format(*csv_name.rsplit('.', maxsplit=1))
    with open(f_name_new, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        writer.writerows(lines)


def _check_area_inclusion(line: List[str], areas: List[Area],
                          lat: int, lon: int) -> List[str]:
    """Appends areas names to csv line in which it is contains

    Args:
        line (List[str]): Csv line
        areas (List[Area]): List of areas parsed from kml file
        lat (int): Latitude position in csv line
        lon (int): Longitude position in csv line

    Returns:
        List[str]: _description_
    """
    try:
        point = _get_point_from_line(line, lat, lon)
        for area in areas:
            if area.polygon.contains(point):
                line.append(area.name)
    except:
        print(f'Problem with line:\n{line}')
    finally:
        return line


def _set_area_to_csv(args: Namespace) -> None:
    """Main function which reads csv, check area inclusion and writes result

    Args:
        args (Namespace): Arguments from command line
    """
    areas = _get_areas_from_kml(args.kml)
    _write_csv(args.csv, args.dlm, [
        _check_area_inclusion(line, areas, args.lat, args.lon)
        for line in _read_csv(args.csv, args.dlm)
    ])


def main() -> None:
    """Modules entry point parsing command line arguments and runs
       main functionality
    """
    description = "Setting area inclusion"
    epilog = "If unspecified - [lat, lon] is last two CSV fields"

    parser = ArgumentParser(description=description, epilog=epilog)
    parser.add_argument("-c", "--csv",
                        help="Path to CSV file", required=True)
    parser.add_argument("-k", "--kml",
                        help="Path to KML file", required=True)
    parser.add_argument("-x", "--lat", type=int,
                        help="Latitude field position", default=-2)
    parser.add_argument("-y", "--lon", type=int,
                        help="Longitude field position", default=-1)
    parser.add_argument("-d", "--dlm",
                        help="CSV delimiter", default='\t')
    args = parser.parse_args()

    _set_area_to_csv(args)


if __name__ == '__main__':
    main()