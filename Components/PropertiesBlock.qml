import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import "customs"

Rectangle {
    width: parent.width
    height: parent.height
    color: "transparent"

    ColumnLayout {
        anchors.fill: parent

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"
            border.color: "#45777777"

            ColumnLayout {
                anchors.centerIn: parent
                width: parent.width - 2
                height: parent.height - 2
                spacing: 0

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 24
                    color: "transparent"

                    Row {
                        anchors.verticalCenter: parent.verticalCenter
                        Text {
                            leftPadding: 4
                            text: "Explorer"
                        }
                    }

                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 24
                    color: "transparent"
                    visible: false

                    ToolBar {
                        anchors.fill: parent

                        background: Rectangle {
                            color: "transparent"
                        }

                        RowLayout {
                            CustToolButton { text: "\uf808"}
                        }
                    }

                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 24
                    color: "transparent"

                    TextField {
                        width: parent.width
                        height: parent.height
                        placeholderText: qsTr("Search")
                    }

                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 24
                    color: "transparent"

                    Text {
                        leftPadding: 4
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Explorer")
                    }

                }

                Rectangle {
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    color: "transparent"

                    ListView {
                        width: parent.width
                        height: parent.height
                        model: ExplorerModel {}
                        delegate: ExplorerDelegate {}
                    }

                }


            }

        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"
            border.color: "#45777777"
        }

    }

}
