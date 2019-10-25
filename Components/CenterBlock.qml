import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import "customs" as Cust

Rectangle {
    id: ideal
    color: "transparent"

    property QtObject ttc

    ColumnLayout {

        width: parent.width
        height: parent.height
        //spacing: 0

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            // tabBar
            Rectangle {
                Layout.fillWidth: true
                //Layout.preferredHeight: 40
                Layout.preferredHeight: 24
                color: "#f1f1f1"

                TabBar {
                    id: tbar
                    width: parent.width
                    height: parent.height

                    Component.onCompleted: tab_bar = this

                    ButtonGroup {
                        buttons: tbar.children

                    }

                    background: Rectangle {
                        implicitHeight: 24
                        color: "transparent"

                        Rectangle {
                            anchors.bottom: parent.bottom
                            width: parent.width
                            height: 2
                            color: "dodgerblue"
                        }

                    }

                    Cust.CustTabButton {
                        text: qsTr(tab_headers[0])

                        onClicked: {
                            current_tab = 0
                            tv.currentIndex = 0
                        }
                    }

                }

            }

            // the view
            Cust.CustTabView {
                id: tv
                Layout.fillWidth: true
                Layout.fillHeight: true

                Component.onCompleted: tab_view = this

                TextComponent {
                    property int index: 0
                    anchors.fill: parent
                    color: "dodgerblue"
                }

           }

        }

       Console {
       }


    }

}
