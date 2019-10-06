import QtQuick 2.10
import QtQuick.Controls 2.3

ToolButton {
    id: ctrl
    font.family: font_mat.name
    font.pixelSize: 16

    background: Rectangle {
        color: ctrl.pressed ? "#45777777" : "transparent"
    }

}
