from psychopy import visual, core, event, parallel

parallel_port = None

win = visual.Window([1024, 768])

triggers = range(1, 256)

addresses = [u"0xD010"]

for address in addresses:
    parallel_port = parallel.ParallelPort(address=address)
    for trigger in triggers:
        print("{}\t{}".format(address, trigger))
        win.flip()
        parallel_port.setData(0)
        core.wait(0.5)
        win.flip()
        parallel_port.setData(trigger)

win.flip()
parallel_port.setData(0)
win.close()
core.quit()
