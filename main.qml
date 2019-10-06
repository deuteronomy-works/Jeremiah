import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Window 2.3
import QtQuick.Layouts 1.3
import "Components" as Comp
import "Components/customs" as Cust

ApplicationWindow {
    id: mainWindow
    visible: true
    width: Screen.width
    height: Screen.desktopAvailableHeight
    color: "#f1f1f1"
    flags: Qt.FramelessWindowHint | Qt.Window

    Component.onCompleted: {
        mainWindow.showMaximized()
        Connector.startUp()
    }

    signal spacePressed(string full_text, string curr_char, string line, int cur_pos, var ln_breaks)
    signal enterPressed(string full_text,int cur_pos)
    signal charPressed(string full_text, string curr_char, string line, int cur_pos, var ln_breaks)
    signal backspacePressed(string some_text, int cur_pos)
    signal tabPressed(string some_text, int cur_pos, bool pure)
    signal mousePressed(int cur_pos)

    property QtObject textComp
    property string word
    property var breaks: []
    property string words: ""
    property string prop_text: ""
    property int tab_width: 0

    // FileSystem
    property string file_name: ""
    property url cwd

    onSpacePressed: {
        Connector.pressed_space(full_text, curr_char, line, cur_pos, ln_breaks)
    }

    onEnterPressed: {
        breaks.push(textComp.cursorPosition)
        Connector.pressed_enter(full_text, cur_pos)
    }

    onCharPressed: {
        Connector.pressed_char(full_text, curr_char, line, cur_pos, ln_breaks)
    }

    onBackspacePressed: {
        Connector.pressed_backspace(some_text, cur_pos)
    }

    onTabPressed: {
        Connector.pressed_tab(some_text, cur_pos, pure)
    }

    onMousePressed: {
        Connector.pressed_mouse(cur_pos)
    }

    FontLoader {
        id: font_mat
        source: "fonts/materialdesignicons-webfont.ttf"
    }

    Comp.Settings { id: settings }

    menuBar: Rectangle {
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
                    Action { text: qsTr("File") }
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

    header: Rectangle {
        width: parent.width
        height: 36
        color: "transparent"

        ToolBar {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 8
            anchors.rightMargin: 12
            //width: parent.width
            height: 36

            background: Rectangle {
                color: 'transparent'
            }

            RowLayout {
                height: parent.height

                Cust.CustToolButton {
                    Layout.preferredHeight: 24
                    text: settings.add_f_icon
                }

                Cust.CustToolButton {
                    Layout.preferredHeight: 24
                    text: settings.save_icon
                }

                Cust.CustToolButton {
                    Layout.preferredHeight: 24
                    text: settings.save_all_icon
                }

                Cust.CustToolSeparator {}

                Cust.CustToolButton {
                    Layout.preferredHeight: 24
                    text: settings.undo_icon
                }

                Cust.CustToolButton {
                    Layout.preferredHeight: 24
                    text: settings.redo_icon
                }

                Cust.CustToolSeparator {}

                Cust.CustomComboBox {
                    model: Comp.FreezerModel {}
                }

                Cust.CustomComboBox {
                    model: Comp.RunPlatformModel {}
                }

                Cust.CustomComboBox {
                    model: Comp.RunTypeModel {}
                }

                Cust.CustToolSeparator {}

                Cust.CustToolButton {
                    Layout.preferredHeight: 24
                    text: settings.run_icon
                }

                Cust.CustToolButton {
                    Layout.preferredHeight: 24
                    text: settings.run_icon
                }


            }
        }

    }

    Rectangle {
        width: parent.width
        height: parent.height
        color: "transparent"

        // the rectangle beneath
        Rectangle {
            id: main_content_rect
            anchors.fill: parent
            anchors.leftMargin: 12
            anchors.rightMargin: 12
            color: "transparent"

            // the main layout
            RowLayout {
                width: parent.width
                height: parent.height

                Comp.CenterBlock {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }


                Comp.PropertiesBlock {
                    Layout.preferredWidth: main_content_rect.width / 4
                    Layout.fillHeight: true
                }


            }

        }

        // the rectangle onTop
        Rectangle {
            width: parent.width
            height: parent.height
            color: "transparent"
        }

    }

    footer: Rectangle {
        width: parent.width
        height: 24
        color: "indigo"

        Text {
            text: prop_text
            color: "white"
        }

    }

    Connections {
        target: Connector

        onSend_base_html: {
            //textComp.text = startUp
        }

        onSendCoOrd: {
            var ret = returnCoOrd
            prop_text = "Line: " + ret[0] + ", Col: " + ret[1]
        }

        onEnter_return: {
            var ret = return_enter
            textComp.insert(textComp.cursorPosition, ret)
            Connector.wake_enter_up(textComp.getText(0, textComp.length), textComp.cursorPosition, breaks)
        }

        onBackspace_return: {
            var ret = return_backspace
            textComp.remove(ret[0], ret[1])
            Connector.wake_enter_up(textComp.getText(0, textComp.length), textComp.cursorPosition, breaks)
        }

        onBacktab_return: {
            var ret = return_backtab
            textComp.remove(ret[0], ret[1])
        }

        onWakeUp: {
            var ret = _pressed_mouse
            Connector.wake_me_up(textComp.cursorPosition)
        }

    }

}
