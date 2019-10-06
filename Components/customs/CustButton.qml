import QtQuick 2.10
import QtQuick.Controls 2.3

Button {
    id: ctrl

    background: Rectangle {
        implicitWidth: 36
        color: ctrl.pressed | ctrl.hovered ? "#ccc" : "transparent"
    }

    contentItem: Text {
        padding: ctrl.padding
        text: ctrl.text
        font.family: font_mat.name
    }

}
