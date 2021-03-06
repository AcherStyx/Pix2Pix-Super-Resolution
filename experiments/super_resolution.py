import logging
import cv2
import numpy as np
from data_loaders.video_sample import VideoSampler
from models.pix2pix import Pix2Pix64 as Pix2PixModel

logger = logging.getLogger(__name__)


def combine_view(image_1, image_2, image_3):
    combine_output = np.concatenate([image_1, image_2, image_3], axis=1)
    shape = np.array(combine_output.shape) * 1920
    cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
    while shape[0] > 1080 or shape[1] > 1920:
        shape = (shape / 1.1).astype(int)
    cv2.resizeWindow("Result", shape[1], shape[0])
    cv2.imshow("Result", combine_output)
    # print(combine_output, combine_output.min(), combine_output.max())
    cv2.waitKey(0)


def lr_scheduler(step):
    if step <= 20:
        return 0.001
    if step <= 40:
        return 0.0005
    else:
        return 0.0001


if __name__ == '__main__':
    EXPERIMENT_NAME = "pix2pix64"

    logging.basicConfig(level=logging.DEBUG)
    dataset = VideoSampler(video_file="../data/film.flv",
                           batch_size=2,
                           prefetch=10,
                           shuffle=1000,
                           output_image_size=(128, 128),
                           blur_kernel_size=(6, 6),
                           blur_kernel_size_delta=3).get_dataset()
    model = Pix2PixModel(learning_rate_scheduler=lr_scheduler,
                         tf_board_path="../logs/"+EXPERIMENT_NAME+"/tf_board/record")

    try:
        model.load("../logs/"+EXPERIMENT_NAME+"/save_weight/generator.h5",
                   "../logs/"+EXPERIMENT_NAME+"/save_weight/discriminator.h5")
    except OSError:
        pass
    model.train(dataset, epoch=1, with_preview=True)
    model.save("../logs/"+EXPERIMENT_NAME+"/save_weight/generator.h5",
               "../logs/"+EXPERIMENT_NAME+"/save_weight/discriminator.h5")

    sample_image = cv2.imread("../data/origin/019.jpg")
    gen_output = sample_image

    target_output, gen_input, gen_output = model.predict_sample(gen_output)
    # for _ in range(2):
    #     gen_output = model.predict(gen_output)

    combine_view(gen_input, gen_output, target_output)
    cv2.imwrite("../logs/"+EXPERIMENT_NAME+"/target.jpg", target_output)
    cv2.imwrite("../logs/"+EXPERIMENT_NAME+"/generate_in.jpg", gen_input)
    cv2.imwrite("../logs/"+EXPERIMENT_NAME+"/generate_out.jpg", gen_output)
    cv2.waitKey(0)
