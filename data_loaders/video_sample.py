__package__ = "data_loaders"

import cv2
from .image_sample import ImageSampler


class VideoSampler(ImageSampler):
    def __init__(self,
                 video_file,
                 batch_size,
                 output_image_size,
                 blur_kernel_size,
                 blur_kernel_size_delta=0,
                 shuffle=10,
                 prefetch=1):
        self._VIDEO = video_file

        super(VideoSampler, self).__init__(None, batch_size, output_image_size, blur_kernel_size,
                                           blur_kernel_size_delta, shuffle, prefetch,
                                           skip_small_image=False)

    def _read_image(self):
        capture = cv2.VideoCapture(self._VIDEO)

        success, frame = capture.read()
        while success:
            success, frame = capture.read()
            # cv2.imshow("film", frame)
            # cv2.waitKey(1)
            yield frame


if __name__ == '__main__':
    sampler = VideoSampler("../data/film.flv",
                           batch_size=1,
                           output_image_size=(256, 256),
                           blur_kernel_size=(6, 6))
    print(sampler.get_dataset())
    for a, b in sampler.get_dataset():
        print(a)
        print(b)
        cv2.imshow("a", a.numpy()[0])
        cv2.imshow("b", b.numpy()[0])
        cv2.waitKey(1)
