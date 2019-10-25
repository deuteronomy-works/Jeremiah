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
        var full = dial.fileUrl.toString()
        var splits = full.split('/')
        var filename = splits[splits.length - 1]
        updateList(0, current_tab, filename)
        updateList(1, current_tab, dial.fileUrl)
        save(dial.fileUrl)
    }

    onRejected: {
        //
    }

}
