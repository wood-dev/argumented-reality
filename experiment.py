import ear

def run_testing1():

    print("testing 1 ------")

    input_video_name = 'ear_movie3.mp4'
    input_file_name = 'my-image.png'
    output_video_name = 'ear_output3'
    fps = 30

    initial_top_left = [850, 310]
    initial_bottom_left = [850, 490]
    initial_top_right = [1100, 310]
    initial_bottom_right = [1100, 490]

    frame_ids = [1, 120, 290, 325, 420, 450]

    ear.insert_input_into_video(input_video_name, input_file_name, \
        initial_top_left, initial_bottom_left, initial_top_right, initial_bottom_right, output_video_name, fps, frame_ids, 2500, 'ORB', 'FLANN')


def run_testing2():

    print("testing 2 ------")

    input_video_name = 'ear_movie5.mp4'
    input_file_name = 'my-image.png'
    output_video_name = 'ear_output5'
    fps = 30

    initial_top_left = [800, 542]
    initial_bottom_left = [823, 760]
    initial_top_right = [1038, 496]
    initial_bottom_right = [1062, 729]

    frame_ids = [1, 87, 126, 308, 315, 374, 420]

    ear.insert_input_into_video(input_video_name, input_file_name, \
        initial_top_left, initial_bottom_left, initial_top_right, initial_bottom_right, output_video_name, fps, frame_ids, 1500, 'ORB', 'FLANN')

    # ear.insert_input_into_video(input_video_name, input_file_name, \
    #     initial_top_left, initial_bottom_left, initial_top_right, initial_bottom_right, output_video_name, fps, frame_ids, 2000, 'ORB', 'BF')

    # ear.insert_input_into_video(input_video_name, input_file_name, \
    #     initial_top_left, initial_bottom_left, initial_top_right, initial_bottom_right, output_video_name, fps, frame_ids, 2000, 'BRIEF', 'BF')


def run_testing3():

    print("testing 3 ------")

    input_video_name = 'ear_movie6.mp4'
    input_file_name = 'my-image.png'
    output_video_name = 'ear_output6'
    fps = 30

    initial_top_left = [1180, 451]
    initial_bottom_left = [1190, 624]
    initial_top_right = [1479, 447]
    initial_bottom_right = [1485, 610]

    frame_ids = [1, 120, 290, 325, 420, 450]

    # ear.insert_input_into_video(input_video_name, input_file_name, \
    #     initial_top_left, initial_bottom_left, initial_top_right, initial_bottom_right, output_video_name, fps, frame_ids, 1000, 'ORB', 'FLANN')

    ear.insert_input_into_video(input_video_name, input_file_name, \
        initial_top_left, initial_bottom_left, initial_top_right, initial_bottom_right, output_video_name, fps, frame_ids, 500, 'ORB', 'BF')

    # ear.insert_input_into_video(input_video_name, input_file_name, \
    #     initial_top_left, initial_bottom_left, initial_top_right, initial_bottom_right, output_video_name, fps, frame_ids, 500, 'BRIEF', 'BF')



if __name__ == '__main__':

    run_testing1()      # input ear_movie3.mp4, output to ear_output3.mp4 and ear_output3-N.png
    run_testing2()      # input ear_movie5.mp4, output to ear_output5.mp4 and ear_output5-N.png
    run_testing3()      # input ear_movie6.mp4, output to ear_output6.mp4 and ear_output6-N.png