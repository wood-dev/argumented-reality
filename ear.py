import cv2
import numpy as np
import os
import utils
from time import time

def get_corners_list(image):
    """Returns a ist of image corner coordinates used in warping.

    These coordinates represent four corner points that will be projected to
    a target image.

    Args:
        image (numpy.array): image array of float64.

    Returns:
        list: List of four (x, y) tuples
            in the order [top-left, bottom-left, top-right, bottom-right].
    """

    h = image.shape[0]
    w = image.shape[1]

    corners = np.zeros((4, 1, 2), dtype=np.float32)
    corners[0] = [0, 0]
    corners[1] = [0, h-1]
    corners[2] = [w-1, 0]
    corners[3] = [w-1, h-1]

    return np.asarray(corners, dtype=np.float)


def find_four_point_transform(src_points, dst_points):
    """Solves for and returns a perspective transform.

    Each source and corresponding destination point must be at the
    same index in the lists.

    Do not use the following functions (you will implement this yourself):
        cv2.findHomography
        cv2.getPerspectiveTransform

    Hint: You will probably need to use least squares to solve this.

    Args:
        src_points (list): List of four (x,y) source points.
        dst_points (list): List of four (x,y) destination points.

    Returns:
        numpy.array: 3 by 3 homography matrix of floating point values.
    """

    m1 = []
    m2 = []
    for i in range(len(src_points)):
        x = src_points[i][0][0]
        y = src_points[i][0][1]
        u = dst_points[i][0][0]
        v = dst_points[i][0][1]
        m1.append([x, y, 1, 0, 0, 0, -u*x, -u*y])
        m1.append([0, 0, 0, x, y, 1, -v*x, -v*y])
        m2.append([u])
        m2.append([v])

    H = np.linalg.lstsq(np.asarray(m1), np.asarray(m2), rcond=None)[0]
    H = np.append(H, np.array([1]))
    H = H.reshape(3, 3)
    return H


def identify_matching_features(image1, image2, feature_number, detect_method='ORB', match_method='BF'):

    kp1 = None; des1 = None
    kp2 = None; des2 = None

    if detect_method == 'ORB':
        #orb = cv2.ORB_create(2500) # used by Q1
        orb = cv2.ORB_create(feature_number)
        kp1, des1 = orb.detectAndCompute(image1, None)
        kp2, des2 = orb.detectAndCompute(image2, None)

    elif detect_method == 'SIFT':
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(image1, None)
        kp2, des2 = sift.detectAndCompute(image2, None)

    elif detect_method == 'SURF':
        surf = cv2.xfeatures2d.SURF_create(400)
        kp1, des1 = surf.detectAndCompute(image1, None)
        kp2, des2 = surf.detectAndCompute(image2, None)

    elif detect_method == 'BRIEF':
        star = cv2.xfeatures2d_StarDetector.create()
        brief = cv2.xfeatures2d_BriefDescriptorExtractor.create()
        kp1 = star.detect(image1, None)
        kp1, des1 = brief.compute(image1, kp1)
        kp2 = star.detect(image2, None)
        kp2, des2 = brief.compute(image2, kp2)


    matches = None
    if match_method == 'BF':
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

    elif match_method == 'FLANN':
        FLANN_INDEX_LSH =  6
        index_params = dict(algorithm = FLANN_INDEX_LSH, table_number = 6, key_size = 12, multi_probe_level = 1)
        search_params = dict(checks = 50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        #if m.distance < 0.75*n.distance:
        if m.distance < 0.9*n.distance:
            good.append(m)

    src_pts = [kp1[i.queryIdx].pt for i in good]
    dst_pts = [kp2[i.trainIdx].pt for i in good]

    return np.float32(src_pts).reshape(-1,1,2), np.float32(dst_pts).reshape(-1,1,2)


def insert_input_into_video(input_video_name, input_file_name, p1, p2, p3, p4, output_video_name, fps, frame_ids, feature_number, detect_method='ORB', match_method='BF'):

    # for benchmarking
    time_matching_features = 0.0
    time_finding_homography_features = 0.0
    time_finding_homography_4points = 0.0
    time_transform = 0.0
    time_io = 0.0

    image_gen = utils.video_frame_generator(input_video_name)
    video_image = image_gen.__next__()

    h, w, _ = video_image.shape
    video_out = utils.mp4_video_writer(output_video_name + '.mp4', (w, h), fps)

    input_file = utils.read_image(input_file_name)
    input_file_points = get_corners_list(input_file)

    output_counter = 1
    frame_num = 1
    initial_markers = [[p1], [p2], [p3], [p4]]
    initial_markers = np.asarray(initial_markers, dtype=np.float)
    previous_video_image = None
    current_markers = None
    feature_count = []

    time_total = time()

    while video_image is not None:

        # print("Processing fame {}".format(frame_num))
        print('.', end='')
        updated_video_image = None
        gray_video_image = cv2.cvtColor(video_image, cv2.COLOR_BGR2GRAY)
        #gray_video_image = video_image

        if previous_video_image is None:

            # initialize first mapping
            before_process = time()
            M = find_four_point_transform(input_file_points, initial_markers)
            time_finding_homography_4points += time() - before_process

            before_process = time()
            updated_video_image = cv2.warpPerspective(input_file, M, (w, h), video_image, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)
            time_transform += time() - before_process

            current_markers = initial_markers

        else:

            # find matching features
            before_process = time()
            src_pts, dst_pts = identify_matching_features(previous_video_image, gray_video_image, feature_number, detect_method, match_method)
            feature_count.append(len(src_pts))
            time_matching_features += time() - before_process

            # find homography from how matching features move
            before_process = time()
            M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)
            time_finding_homography_features += time() - before_process

            # use the homography to update markers (defined by previous / initial coord)
            current_markers = cv2.perspectiveTransform(current_markers, M)

            # find transform between new markers and input
            before_process = time()
            M = cv2.getPerspectiveTransform(np.float32(input_file_points), np.float32(current_markers))
            time_finding_homography_4points += time() - before_process

            # use the transform to insert image
            before_process = time()
            updated_video_image = cv2.warpPerspective(input_file, M, (w, h), video_image, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)
            time_transform += time() - before_process

        updated_video_image = cv2.putText(updated_video_image, str(frame_num), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        # save frames according to the given frame ID list
        frame_id = frame_ids[output_counter % len(frame_ids) - 1]
        if frame_num == frame_id:
            out_str = output_video_name + "-{}.png".format(output_counter)
            output_counter += 1
            utils.save_image(out_str, updated_video_image)

        previous_video_image = gray_video_image
        frame_num += 1

        before_process = time()
        video_out.write(updated_video_image)
        video_image = image_gen.__next__()
        time_io += time() - before_process

    before_process = time()
    video_out.release()
    time_io += time() - before_process

    time_total = time() - time_total

    print('completed')
    print('output stat --------- feature number: {0}, detect_method: {1}, match_method: {2} '.format(feature_number, detect_method, match_method))
    print('average number of features between frames: {:.2f}'.format(np.average(feature_count)))
    print('time on matching features: {:.2f}'.format(time_matching_features))
    print('time on finding homography of features: {:.2f}'.format(time_finding_homography_features))
    print('time on finding homography between input and markers: {:.2f}'.format(time_finding_homography_4points))
    print('time on warping image: {:.2f}'.format(time_transform))
    print('time on io: {:.2f}'.format(time_io))
    print('total time: {:.2f}'.format(time_total))
    print('total frame: {}'.format(frame_num))
