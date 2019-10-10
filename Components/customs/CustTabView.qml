import QtQuick 2.10

Rectangle {
    id: basev

    signal addChild(url ur_l, QtObject tab_id, string tv_id)

    onAddChild: {
        var comp
        var mComp
        var obj

        function finiCreate() {
            if(comp.status === Component.Ready) {
                obj = comp.createObject(mComp)
            }
        }

        var ind = basev.count
        mComp = Qt.createQmlObject('import QtQuick 2.10; Rectangle {property int index:' + ind +';anchors.fill: parent; color: "transparent"; visible: index == parent.currentIndex;}', basev)
        basev.count += 1
        comp = Qt.createComponent(ur_l)
        if(comp.status === Component.Ready) {
            obj = comp.createObject(mComp)
        } else {
            comp.statusChanged.connect(finiCreate)
        }

        var ss = 'import QtQuick 2.10; CustTabButton{text: qsTr("Untitled"); onClicked: {'+ tv_id +'.currentIndex=' + ind +' }}'
        var btnc = Qt.createQmlObject(ss, tab_id)
    }

    property int currentIndex: 0
    property QtObject currentItem: this.children[currentIndex]
    property int count: 0

    Component.onCompleted: {
        var child = this.children
        var lent = child.length
        if(lent > 0) {
            for(var i=0; i<lent; i++) {
                this.children[i].index = i
                count++
            }
        }
    }

}
