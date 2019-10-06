import QtQuick 2.10
import QtQuick.Controls 2.3

Button {
    id: ctrl

    background: Rectangle {
        implicitWidth: 24
        implicitHeight: 12
        color: "transparent"
    }

    contentItem: Text {
        text: ctrl.text
        font.family: font_mat.name
        font.pixelSize: 16
        color: "white"
    }

}
