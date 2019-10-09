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
                        text: qsTr("First layout")

                        onClicked: {
                            tv.currentIndex = 0
                        }
                    }

                    Cust.CustTabButton {
                        text: qsTr("add layout")

                        onClicked: {
                            tv.addChild("../TextComponent.qml", tbar, tv)
                        }
                    }

                }

            }

            // the view
            Cust.CustTabView {
                id: tv
                Layout.fillWidth: true
                Layout.fillHeight: true

                Rectangle {
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
