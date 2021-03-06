import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import "Components" as Comp
import "Components/customs" as Cust

ApplicationWindow {
    id: mainWindow
    visible: true
    width: screen.width
    height: screen.desktopAvailableHeight - 48
    color: "#f1f1f1"
    flags: Qt.FramelessWindowHint | Qt.Window


    // Application
    property int current_tab: 0
    property QtObject tab_view
    property QtObject tab_bar
    property var textComp: []
    property var tab_headers: ["First Layout"]

    // Editor
    property string word
    property var breaks: []
    property string words: ""
    property string prop_text: ""
    property int tab_width: 0

    // FileSystem
    property var file_names: ["First Layout"]
    property string opening_file: ""
    property url cwd
    property bool saved: false
    property string full_text

    // Runner
    property bool sing_running
    property bool project_running


    // Application
    signal createNewTab()
    signal startNewDocument(string file_contents)
    signal updateList(int pos, int ind, string value)

    // Editor
    signal spacePressed(string full_text, string curr_char, string line, int cur_pos, var ln_breaks)
    signal enterPressed(string full_text,int cur_pos)
    signal charPressed(string full_text, string curr_char, string line, int cur_pos, var ln_breaks)
    signal backspacePressed(string some_text, int cur_pos)
    signal tabPressed(string some_text, int cur_pos, bool pure)
    signal mousePressed(int cur_pos)
    signal count()

    // FileSystem
    signal openBtnPressed()
    signal openFile(string file)
    signal updateFileName(string file)
    signal saveBtnPressed(string fulltext)
    signal save(string filename)

    // Runner
    signal runSingleFile()
    signal runProject()


    // Application
    onCreateNewTab: {
        tab_view.addChild('../TextComponent.qml', tab_bar, 'tv')
    }

    onStartNewDocument: {

        createNewTab()
        var ind = tab_headers.length - 1
        textComp[ind].text = file_contents
        updateFileName(opening_file)
        updateList(1, ind, opening_file)

    }

    onUpdateList: {
        var headers
        var files

        if(pos == 0) {
            tab_headers[ind] = value
            headers = tab_headers
            tab_headers = new Object(headers)
        } else if(pos == 1) {
            file_names[ind] = value
            files = file_names
            file_names = new Object(file_names)
        }

        if(pos == 2) {
            tab_headers[ind] = value
            headers = tab_headers
            tab_headers = new Object(headers)
            file_names[ind] = value
            files = file_names
            file_names = new Object(file_names)
        }

    }

    Component.onCompleted: {
        Connector.startUp()
    }

    // Editor
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

    onCount: {
        var tComp = textComp[current_tab]
        Connector.editor_count(tComp.getText(0, tComp.length), tComp.cursor_position)
    }

    // FileSystem
    onOpenBtnPressed: {
        o_Dialog.open()
    }

    onOpenFile: {
        opening_file = file
        Connector.read_file(file)
    }

    onUpdateFileName: {

        // Update File name with real name

        var ind = file_names.length - 1
        var splits = file.split("/")
        var last_id = splits.length - 1
        var name = splits[last_id]
        updateList(0, ind, name)
    }

    onSaveBtnPressed: {
        full_text = fulltext
        var filename = file_names[current_tab]
        if (filename === "Untitled") {
            s_Dialog.open()
        } else {
            save(filename)
        }
    }

    onSave: {
        Connector.save_file(filename, full_text)
    }

    // Runner
    onRunSingleFile: {
        var fileName = file_names[current_tab];
        Connector.run_single_file(fileName);
    }

    onRunProject: {
        Connector.run_project(mainFile);
    }



    FontLoader {
        id: font_mat
        source: "fonts/materialdesignicons-webfont.ttf"
    }

    Comp.Settings { id: settings }

    menuBar: Comp.MainMenu {}

    header: Rectangle {
        width: parent.width
        height: 36
        color: "transparent"

        Comp.Toolbar {}

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

                Rectangle {
                    Layout.preferredWidth: main_content_rect.width / 4
                    Layout.fillHeight: true
                    border.color: "#45777777"
                    /*Comp.PropertiesBlock {
                        Layout.preferredWidth: main_content_rect.width / 4
                        Layout.fillHeight: true
                        visible: false
                    }*/

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

    Comp.OpenDialog { id: o_Dialog }
    Comp.SaveDialog { id: s_Dialog }


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
            var tComp = textComp[current_tab]
            tComp.insert(tComp.cursorPosition, ret)
            Connector.wake_enter_up(tComp.getText(0, tComp.length), tComp.cursorPosition, breaks)
        }

        onBackspace_return: {
            var ret = return_backspace
            var tComp = textComp[current_tab]
            tComp.remove(ret[0], ret[1])
            Connector.wake_enter_up(tComp.getText(0, tComp.length), tComp.cursorPosition, breaks)
        }

        onBacktab_return: {
            var ret = return_backtab
            textComp[current_tab].remove(ret[0], ret[1])
        }

        onWakeUp: {
            var ret = _pressed_mouse
            Connector.wake_me_up(textComp[current_tab].cursorPosition)
        }

        onCompletedProcess: {
            var ret = return_completed
            if(ret === "save") {
                saved = true
            }
        }

        onOpenedFile: {
            var conts = return_contents
            // Start New Document
            startNewDocument(conts)
        }

        onCheckedVocab: {
            var ret = return_vocab
            textComp[current_tab].text = ret
            count()
        }

    }

}
