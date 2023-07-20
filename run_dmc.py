from enum import Enum
from qgis.core import (
    QgsProject,
    QgsPrintLayout,
    QgsLayoutItemShape,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsFillSymbol,
    QgsLayoutItemLabel,
    QgsUnitTypes,
    QgsLayoutItemPage,
)
from qgis.utils import iface
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

MM = QgsUnitTypes.LayoutMillimeters

sizes = {"A4": (210, 297)}
page_size = "A4"

height, width = sizes[page_size]
layout_name = "sample_layout"

global_font_color = QColor(255, 255, 255)
global_font_type_bold = QFont("Gill Sans", 20, QFont.Bold)
global_font_type = QFont("Gill Sans", 20)


class LayoutItem(Enum):
    SHAPE = 1
    LABEL = 2


def create_layout_shape(item):
    qgs_item = QgsLayoutItemShape(layout)
    qgs_item.setId(item["id"])
    qgs_item.setShapeType(item["shape_type"])

    symbol = QgsFillSymbol.createSimple(item["props"])
    qgs_item.setSymbol(symbol)

    x, y = item["position"]
    qgs_item.attemptMove(QgsLayoutPoint(x, y, MM))
    width, height = item["size"]
    qgs_item.attemptResize(QgsLayoutSize(width, height, MM))

    qgs_item.setLocked(True)

    return qgs_item


def create_layout_label(item):
    qgs_item = QgsLayoutItemLabel(layout)
    qgs_item.setId(item["id"])
    qgs_item.setText(item["label_text"])
    qgs_item.setFontColor(item["label_color"])
    qgs_item.setFont(item["label_font"])

    if "rotation" in item.keys():
        qgs_item.setItemRotation(item["rotation"])

    x, y = item["position"]
    qgs_item.attemptMove(QgsLayoutPoint(x, y, MM))
    width, height = item["size"]
    qgs_item.attemptResize(QgsLayoutSize(width, height, MM))

    if "alignment" in item.keys():
        qgs_item.setHAlign(item["alignment"])

    qgs_item.setLocked(True)

    return qgs_item


items = [
    {
        "id": "header",
        "type": LayoutItem.SHAPE,
        "shape_type": QgsLayoutItemShape.Rectangle,
        "position": (0, 0),
        "size": (20, height),
        "props": {
            "color": "#0A6EB4",
            "outline_width": 0,
        },
    },
    {
        "id": "title",
        "type": LayoutItem.LABEL,
        "label_text": "COUNTRY_NAME",
        "label_color": global_font_color,
        "label_font": global_font_type_bold,
        "rotation": 270,
        "position": (2, 210),
        "size": (205, 10),
        "alignment": Qt.AlignmentFlag.AlignRight,
    },
    {
        "id": "sub_title",
        "type": LayoutItem.LABEL,
        "label_text": "Veni, vidi, vici. I came, I saw, I conquered.",
        "label_color": global_font_color,
        "label_font": global_font_type,
        "rotation": 270,
        "position": (9, 210),
        "size": (205, 20),
        "alignment": Qt.AlignmentFlag.AlignRight,
    },
]
project = QgsProject.instance()
manager = project.layoutManager()
layouts = manager.printLayouts()

# remove the same named layout
for layout in layouts:
    if layout.name() == layout_name:
        layout_manager.removeLayout(layout)

### (1) Initialize a layout
layout = QgsPrintLayout(project)
layout.setName(layout_name)
layout.initializeDefaults()

page = layout.pageCollection().pages()[0]
page.setPageSize(page_size, QgsLayoutItemPage.Orientation.Landscape)
iface.openLayoutDesigner(layout)

qgs_item = create_layout_shape(items[0])
layout.addLayoutItem(qgs_item)
# Create header.

title = create_layout_label(items[1])
layout.addLayoutItem(title)

sub_title = create_layout_label(items[2])
layout.addLayoutItem(sub_title)
