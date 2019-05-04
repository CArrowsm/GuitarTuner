# Remember to hold the references to QTimeLine and QGraphicsItemAnimation instances.
# They are not kept anywhere, even if you invoke QTimeLine.start().
self.tl = QtCore.QTimeLine(1000)
self.tl.setFrameRange(0, 100)
self.a = QtGui.QGraphicsItemAnimation()
self.a.setItem(self.item)
self.a.setTimeLine(self.tl)

# Each method determining an animation state (e.g. setPosAt, setRotationAt etc.)
# takes as a first argument a step which is a value between 0 (the beginning of the
# animation) and 1 (the end of the animation)
self.a.setPosAt(0, QtCore.QPointF(0, -10))
self.a.setRotationAt(1, 360)

self.tl.start()
