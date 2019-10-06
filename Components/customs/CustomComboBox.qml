import QtQuick 2.10
import QtQuick.Controls 2.3

ComboBox {
    id: ctrl

    background: Rectangle {
        implicitWidth: 120
        implicitHeight: 28
        border.color: "#ccc"
    }

    indicator: Text {
        width: 12
        x: ctrl.width - width - ctrl.rightPadding
        y: (ctrl.availableHeight - height) / 2 + ctrl.topPadding
        font.family: font_mat.name
        font.pixelSize: 16
        text: settings.down_icon
    }

}
