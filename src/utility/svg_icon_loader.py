from PySide6.QtCore import QByteArray
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer


def get_icon(file_path, color):
    with open(file_path, "r") as file:
        svg_content = file.read()

    modified_svg = svg_content.replace('fill="currentColor"', f'fill="{color}"')

    byte_array = QByteArray(modified_svg.encode("utf-8"))

    svg_renderer = QSvgRenderer(byte_array)
    pixmap = QPixmap(100, 100)
    pixmap.fill(QColor("transparent"))

    painter = QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()

    return QIcon(pixmap)
