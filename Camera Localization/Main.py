import glob
import cv2
import CorrespondenceMatcher as cm
import ProjectionEstimator as pe
import Renderer as rr


FOCAL_LENGTH = 32
PATTERN_SIZE = 88


pattern = cv2.imread('pattern.png', 0)     # trainImage
matcher = cm.CorrespondenceMatcher(pattern)
estimator = pe.ProjectionEstimator()
renderer = rr.Renderer()

target_files = glob.glob("*.JPG")

for img_file in target_files:
        print("loading image " + img_file)
        query = cv2.imread(img_file, 0)    # queryImage

        q_h, q_w = query.shape[:2]
        p_h, p_w = pattern.shape[:2]

        print("finding homography for " + img_file)
        h = matcher.find_homography(query)
        print("homography matrix " + str(h))

        print("finding extrinsic camera parameter for " + img_file)
        rx, ry, rz, px, py, pz, residual = estimator.compute_extrinsic(
            h, q_w / p_w, FOCAL_LENGTH, PATTERN_SIZE)
        print("rotation: " + str([rx, ry, rz]))
        print("position: " + str([px, py, pz]))
        print("parameter residual " + str(residual))

        print("rendering result")
        # renderer.render(img_file, rx, ry, rz, px, py, pz)
        break
