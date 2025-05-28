import requests
import random
import time
import numpy as np
import h5py

from psychopy import visual, core, event

win = visual.Window(fullscr=True, color=[1, 1, 1])
gaze_marker = visual.Circle(win, radius=0.02, fillColor='red', lineColor='red', units='norm')
shapes = [
    visual.Circle(win, radius=0.1, fillColor='blue', lineColor='blue', units='norm'),
    visual.Rect(win, width=0.2, height=0.2, fillColor='green', lineColor='green', units='norm')
]

def get_gaze_data():
    try:
        response = requests.get('http://localhost:5000/gaze')
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return None

gaze_samples = []
message_events = []

trial_clock = core.Clock()
while trial_clock.getTime() < 20:
    shape = random.choice(shapes)
    shape.pos = (random.uniform(-1, 1), random.uniform(-1, 1))
    shape.draw()
    win.flip()
    core.wait(1)

    gaze_data = get_gaze_data()
    print("Gaze data received:", gaze_data)  # Add this line
    timestamp = time.time()
    if gaze_data and gaze_data['x'] is not None and gaze_data['y'] is not None:
        screen_width, screen_height = win.size
        norm_gaze_x = (gaze_data['x'] / screen_width) * 2 - 1
        norm_gaze_y = -((gaze_data['y'] / screen_height) * 2 - 1)
        gaze_marker.pos = (norm_gaze_x, norm_gaze_y)
        gaze_samples.append((timestamp, gaze_data['x'], gaze_data['y']))
    else:
        gaze_samples.append((timestamp, None, None))

    message_events.append((timestamp, f"Shape at {shape.pos}"))

    gaze_marker.draw()
    win.flip()

    if event.getKeys():
        break

# This has to be here! Otherwise the window will close and for some reason we won't have the data saved.
with h5py.File("./webgazer_data.hdf5", "w") as f:
    gaze_dtype = np.dtype([
        ('timestamp', 'f8'),
        ('left_gaze_x', 'f8'),
        ('left_gaze_y', 'f8'),
        ('right_gaze_x', 'f8'),
        ('right_gaze_y', 'f8')
    ])
    gaze_array = np.array([
        (t, x if x is not None else np.nan, y if y is not None else np.nan,
         x if x is not None else np.nan, y if y is not None else np.nan)
        for t, x, y in gaze_samples
    ], dtype=gaze_dtype)
    f.create_dataset("data_collection/events/eyetracker/BinocularEyeSampleEvent", data=gaze_array)

    msg_dtype = h5py.string_dtype(encoding="utf-8")
    msg_array = np.array([(t, m) for t, m in message_events], dtype=[('timestamp', 'f8'), ('text', msg_dtype)])
    f.create_dataset("data_collection/events/experiment/MessageEvent", data=msg_array)

win.close()
core.quit()