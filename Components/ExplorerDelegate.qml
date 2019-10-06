import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

Component {

    Rectangle {
        anchors.left: parent.left
        anchors.leftMargin: 4
        width: parent.width - 4
        height: 24
        color: "transparent"

        Settings {id: settings}

        RowLayout {
            height: parent.height

            Text {
                id: arrow
                font.family: font_mat.name
                font.pixelSize: 16
                text: settings.arrow_icon
                visible: folder
            }

            Rectangle {
                Layout.preferredWidth: folder ? 0 : 21
                Layout.fillHeight: true
                color: "transparent"
            }

            Text {
                id: fold_icon
                font.family: font_mat.name
                font.pixelSize: 16
                text: folder ? settings.fold_o : settings.doc_icon
            }

            Text {
                text: title
            }


        }
    }
}
