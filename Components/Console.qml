import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import "customs"

Rectangle {
    Layout.bottomMargin: 5
    Layout.fillWidth: true
    Layout.preferredHeight: 152
    border.color: "#45777777"

    ColumnLayout {
        anchors.centerIn: parent
        width: parent.width - 2
        height: parent.height - 2

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 24
            color: "#0082E8"

            RowLayout {
                anchors.verticalCenter: parent.verticalCenter
                anchors.fill: parent
                anchors.rightMargin: 4
                anchors.leftMargin: 4
                anchors.bottomMargin: 4

                Text {
                    Layout.alignment: Qt.AlignVCenter
                    text: "Output"
                    font.family: "Segoe UI Semilight"
                    color: "white"
                }

                Row {
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                    CustTinyButton {
                        text: settings.menu_icon
                    }

                    CustTinyButton {
                        text: settings.pin_icon
                    }

                    CustTinyButton {
                        text: settings.close_icon
                    }

                }

            }

        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

    }

}
