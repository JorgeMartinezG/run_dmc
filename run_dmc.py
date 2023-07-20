from qgis.core import (
    QgsProject,
    QgsPrintLayout,
    QgsLayoutItemShape,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsFillSymbol,
    QgsLayoutItemLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

MM = QgsUnitTypes.LayoutMillimeters

A4_size = (297, 210) # mms
height, height = A4_size

layout_name = "sample_layout"

items = [
    {
        "id": "header",
        "type": QgsLayoutItemShape.Rectangle,
        "position": (0, 0),
        "size": (20, height),
        "props": {
            "color": "#0A6EB4",
            "outline_width": 0,
            "outline_color": "transparent"
        }
    }
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
page.setPageSize('A4', QgsLayoutItemPage.Orientation.Landscape)
iface.openLayoutDesigner(layout)

item = items[0]

# Create header.
qgs_item = QgsLayoutItemShape(layout)
qgs_item.setShapeType(item["type"])
qgs_item.setId(item["id"])
symbol = QgsFillSymbol.createSimple(item["props"])
qgs_item.setSymbol(symbol)

x, y = item["position"]
qgs_item.attemptMove(QgsLayoutPoint(x, y, MM))
width, height = item["size"]
qgs_item.attemptResize(QgsLayoutSize(width, height, MM))

layout.addLayoutItem(qgs_item)

title = QgsLayoutItemLabel(layout)
title.setText("COUNTRY_NAME")
title.setFontColor(QColor(255, 255, 255))
title.setFont(QFont("Gill Sans" , 20 , QFont.Bold))
title.setItemRotation(270)

title.attemptMove(QgsLayoutPoint(2, 210, MM))
title.attemptResize(QgsLayoutSize(205, 10, MM))
title.setHAlign(Qt.AlignmentFlag.AlignRight)

layout.addLayoutItem(title)

sub_title = QgsLayoutItemLabel(layout)
sub_title.setText("Veni, vidi, vici. I came, I saw, I conquered.")
sub_title.setFontColor(QColor(255, 255, 255))
sub_title.setFont(QFont("Gill Sans" , 18))
sub_title.setItemRotation(270)

sub_title.attemptMove(QgsLayoutPoint(9, 210, MM))
sub_title.attemptResize(QgsLayoutSize(205, 20, MM))
sub_title.setHAlign(Qt.AlignmentFlag.AlignRight)
layout.addLayoutItem(sub_title)



