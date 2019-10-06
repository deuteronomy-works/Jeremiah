import QtQuick 2.10
import QtQuick.Controls 2.3

TabButton {
    width: 124

    background: Rectangle {
        color: parent.checked ?"dodgerblue" : parent.pressed ? "dodgerblue" : "transparent"
    }

    contentItem: Text {
        width: 124
        text: parent.text
    }

}
