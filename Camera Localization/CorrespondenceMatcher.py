import numpy as np
import cv2

MIN_MATCH_COUNT = 10
FLANN_INDEX_KDTREE = 0


class CorrespondenceMatcher:

        def __init__(self, pattern):
                # Initiate SIFT detector
                self.sift = cv2.xfeatures2d.SIFT_create()
                kp, desc = self.sift.detectAndCompute(pattern, None)
                self.pattern_kp = kp
                self.pattern_desc = desc

        def find_homography(self, query):
                query_kp, query_desc = self.sift.detectAndCompute(query, None)

                index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
                search_params = dict(checks=50)
                flann = cv2.FlannBasedMatcher(index_params, search_params)
                matches = flann.knnMatch(query_desc, self.pattern_desc, k=2)

                # store all the good matches as per Lowe's ratio test.
                good = []
                for m, n in matches:
                        if m.distance < 0.7 * n.distance:
                                good.append(m)

                if len(good) > MIN_MATCH_COUNT:
                        dst_pts = np.float32(
                            [query_kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                        src_pts = np.float32(
                            [self.pattern_kp[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                        M, mask = cv2.findHomography(
                            src_pts, dst_pts, cv2.RANSAC, 5.0)

                        return M
                else:
                        return None
