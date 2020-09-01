import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import "customs" as Cust

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
            model: FreezerModel {}
        }

        Cust.CustomComboBox {
            model: RunPlatformModel {}
        }

        Cust.CustomComboBox {
            model: RunTypeModel {}
        }

        Cust.CustToolSeparator {}

        Cust.CustToolButton {
            Layout.preferredHeight: 24
            text: settings.run_icon

            onClicked: runProject();
        }

        Cust.CustToolButton {
            Layout.preferredHeight: 24
            text: settings.run_icon

            onClicked: runSingleFile();
        }


    }
}
