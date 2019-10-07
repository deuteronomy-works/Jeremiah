import QtQuick 2.10
import QtQuick.Dialogs 1.3

FileDialog {
    id: dial
    title: qsTr("Save File")
    selectExisting: false
    nameFilters: ["Py files (*.py)", "All files (*)"]
    //defaultSuffix: "py"
    //folder: ""

    onAccepted: {
        save(dial.fileUrl)
    }

    onRejected: {
        //
    }

}
