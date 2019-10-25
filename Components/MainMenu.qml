import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import "customs" as Cust

Rectangle {
        height: 36
        color: "transparent"

        property int prevX
        property int prevY

        // To GO
        /*MouseArea {
            anchors.fill: parent

            onPressed: {
                parent.prevX = mouseX
                parent.prevY = mouseY
            }

            onMouseXChanged: {
                var change = mouseX - parent.prevX
                mainWindow.setX(mainWindow.x + change)

            }

            onMouseYChanged: {
                var change = mouseY - parent.prevY
                mainWindow.setY(mainWindow.y + change)

            }
        }*/

        RowLayout {
            anchors.fill: parent

            MenuBar {
                Menu {
                    title: qsTr("File")
                    Action {
                        text: qsTr("File")

                        onTriggered: createNewTab()

                    }

                    Action {
                        text: qsTr("&Save")

                        onTriggered: {
                            saveBtnPressed(textComp[current_tab].getText(0, textComp[current_tab].length))
                        }

                    }
                }
                Menu {
                    title: qsTr("Edit")
                    Action { text: qsTr("Edit") }
                }
                Menu {
                    title: qsTr("Project")
                    Action { text: qsTr("Project") }
                }
                Menu {
                    title: qsTr("Build")
                    Action { text: qsTr("Build") }
                }

                background: Rectangle {
                    color: "transparent"
                }

            }

            Row {
                //Layout.preferredWidth: 144
                Layout.alignment: Qt.AlignRight
                Cust.CustButton {
                    text: "\uE921"
                    onClicked: mainWindow.showMinimized()
                }
                Cust.CustButton {
                    text: "\uE922"
                    onClicked: mainWindow.showMaximized()

                }
                Cust.CustButton {
                    text: "\uE8BB"
                    onClicked: mainWindow.close()
                }
            }

        }

    }
