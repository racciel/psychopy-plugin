from psychopy import visual, core


win = visual.Window()
msg = visual.TextStim(win, text=u"Hello world!")

msg.draw()
win.flip()
core.wait(1)
win.close()