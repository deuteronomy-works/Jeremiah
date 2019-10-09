import QtQuick 2.10

Rectangle {
    id: basev

    signal addChild(url ur_l, QtObject tab_id, QtObject tv_id)

    onAddChild: {
        var comp
        var mComp
        var obj

        function finiCreate() {
            print('called')
            if(comp.status === Component.Ready) {
                obj = comp.createObject(mComp)
            } else {
                print(comp.status)
            }
        }

        mComp = Qt.createQmlObject('import QtQuick 2.10; Rectangle {property int index:' + basev.count +';anchors.fill: parent; color: "transparent"; visible: index == parent.currentIndex;}', basev)
        basev.count += 1
        comp = Qt.createComponent(ur_l)
        if(comp.status === Component.Ready) {
            obj = comp.createObject(mComp)
        } else {
            print(comp.errorString())
            comp.statusChanged.connect(finiCreate)
        }

        print(obj)
        var btnc = Qt.createQmlObject('import QtQuick 2.10; CustTabButton{text: qsTr("something"); onClicked: {tv.currentIndex = 1 }}', tab_id)
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
