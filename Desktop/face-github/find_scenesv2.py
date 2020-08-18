from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
import csv

THRESHOLD = 30.0
VIDEO = "roermond.mp4"
RESULTS_FILE = "results/scene.txt"
validation = []
results = []

def find_scene(video, results):
    video_manager = VideoManager([video])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=THRESHOLD))
    base_timecode = video_manager.get_base_timecode()
    video_manager.set_downscale_factor()
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list(base_timecode)
            # Each scene is a tuple of (start, end) FrameTimecodes.
    for i, scene in enumerate(scene_list):
        #scene[0].get_timecode(), scene[0].get_frames(),
        #scene[1].get_timecode(), scene[1].get_frames(),))
        results.append((scene[0].get_timecode()))
    video_manager.release()

# Read csv and save results to a list
def read_csv(RESULTS_FILE, list_name):
    with open(RESULTS_FILE) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        line = 0
        for row in reader:
            if line == 0:
                line += 1
            else:
                validation.append(row)

def change_time_format(time_list):
    j = 0
    for i in time_list:
        time_list[j] = sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(i[0:8].split(":"))))
        j += 1
    return time_list

def calculate_accuracy(validation, results):
    score = 0
    j = 0
    for i in validation:
        if i[1] == results[j]:
            score += 1
    return score/len(validation)

read_csv(RESULTS_FILE, validation)
find_scene(VIDEO, results)

print(validation)
print(results)

final_results = change_time_format(results)
print(final_results)
print(calculate_accuracy(validation, final_results))
