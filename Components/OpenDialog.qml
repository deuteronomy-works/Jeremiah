import QtQuick 2.10
import QtQuick.Dialogs 1.3

FileDialog {
    id: diag
    title: "Choose a file"
    nameFilters: ["Python files (*.py)", "All files (*)"]

    onAccepted: {
        openFile(diag.fileUrl)
    }


}
