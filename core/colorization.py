import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsqr
from skimage.color import rgb2yiq, yiq2rgb

from utils.logger import setup_logger

log = setup_logger(__name__)

INPUT_DIR = "./input/"
OUTPUT_DIR = "./output/"
PRECISION = 0.01
WINDOW_SIZE = 3
VARIANCE_MULTIPLIER = 0.6
MIN_SIGMA = 0.000002


def preprocess(original_filepath, marked_filepath):
    original_file = cv2.imread(original_filepath)
    marked_file = cv2.imread(marked_filepath)

    marked_file = cv2.cvtColor(marked_file, cv2.COLOR_BGR2RGB)

    original_file = original_file / 255.
    marked_file = marked_file / 255.

    marks = np.sum(np.abs(original_file - marked_file), axis=2) > PRECISION
    marks = marks.astype('double')

    # convert to YIQ
    original_ntsc = rgb2yiq(original_file)
    marked_ntsc = rgb2yiq(marked_file)

    # creating output image
    height, width, channels = original_ntsc.shape
    output_image = np.empty((height, width, channels))
    output_image[:, :, 0] = original_ntsc[:, :, 0]
    output_image[:, :, 1] = marked_ntsc[:, :, 1]
    output_image[:, :, 2] = marked_ntsc[:, :, 2]

    return output_image, marks


def get_neighbours(row, col, height, width):
    half_window = WINDOW_SIZE // 2

    # will be inclusive on lower bound
    min_row = max(0, row - half_window)
    min_col = max(0, col - half_window)

    # will be exclusive on upper bound
    max_row = min(row + half_window + 1, height)
    max_col = min(col + half_window + 1, width)

    neighbors = [
        (n_row, n_col)
        for n_row in range(min_row, max_row)
        for n_col in range(min_col, max_col)
    ]

    # don't count (r, c) itself as a neighbor
    neighbors.remove((row, col))

    return neighbors


def _colorize(image, marks):
    height, width, channels = image.shape
    image_size = height * width
    window_size = WINDOW_SIZE ** 2
    full_length = image_size * window_size
    image_indices = np.arange(image_size).reshape((height, width), order="F")

    absolute_index = 0
    pixel_index = 0
    row_indices = np.zeros((full_length, 1))
    col_indices = np.zeros((full_length, 1))
    values = np.zeros((full_length, 1))

    for col in range(width):
        for row in range(height):
            global_values = np.zeros((1, window_size))

            if not marks[row, col]:
                neighbour_index = 0
                neighbours = get_neighbours(row, col, height, width)

                for (neighbour_row, neighbour_col) in neighbours:
                    row_indices[absolute_index] = pixel_index
                    col_indices[absolute_index] = image_indices[
                        neighbour_row, neighbour_col]
                    global_values[0, neighbour_index] = image[
                        neighbour_row, neighbour_col, 0]
                    absolute_index += 1
                    neighbour_index += 1

                current_pixel_val = image[row, col, 0]
                global_values[0, neighbour_index] = current_pixel_val

                inclusive_global_values = global_values[:,
                                          0: neighbour_index + 1]
                noninclusive_global_values = global_values[:,
                                             0: neighbour_index]

                variance = np.mean((inclusive_global_values - np.mean(
                    inclusive_global_values)) ** 2)
                sigma = variance * VARIANCE_MULTIPLIER
                min_global_variance = np.min(
                    (noninclusive_global_values - current_pixel_val) ** 2)

                if sigma < -min_global_variance / np.log(0.01):
                    sigma = -min_global_variance / np.log(0.01)
                sigma = max(sigma, MIN_SIGMA)

                something = np.exp(-(
                                            noninclusive_global_values - current_pixel_val) ** 2 / sigma)
                something = something / np.sum(something)
                values[absolute_index - neighbour_index: absolute_index] = - (
                    something.T)

            row_indices[absolute_index] = pixel_index
            col_indices[absolute_index] = image_indices[row, col]
            values[absolute_index] = 1
            pixel_index += 1
            absolute_index += 1

    values = values[0: absolute_index].T[0]
    col_indices = col_indices[0: absolute_index].T[0]
    row_indices = row_indices[0: absolute_index].T[0]

    marked_indices = np.nonzero(marks)
    sparse_matrix = csr_matrix(
        (values, (row_indices, col_indices)), shape=(pixel_index, image_size))

    result = np.copy(image)
    for i in range(1, 3):
        current_slice = image[:, :, i]
        b = np.zeros((height, width))
        b[marked_indices] = current_slice[marked_indices]
        b = b.reshape((sparse_matrix.shape[0]), order="F")
        solution = lsqr(sparse_matrix, b)[0]
        result[:, :, i] = solution.reshape((height, width), order="F")

    return result


def colorize(original_filepath, marked_filepath, output_filepath):
    (output_image, marks) = preprocess(original_filepath, marked_filepath)
    output_image = _colorize(output_image, marks)

    output_image = yiq2rgb(output_image)
    output_image = np.clip(output_image, 0, 1)

    # write to outfile
    plt.imsave(output_filepath, output_image)


# def main():
#     args = sys.argv
#     if len(args) > 1:
#         filename = args[1]
#         original_filepath = f"{INPUT_DIR}/{filename}"
#         marked_filepath = f"{INPUT_DIR}/marked_{filename}"
#         output_filepath = f"{OUTPUT_DIR}/{filename}"
#
#         # todo check files and dirs existence
#         colorize(original_filepath, marked_filepath, output_filepath)
#
#     else:
#         print("Please, write filename as argument")
#
#
# if __name__ == '__main__':
#     main()

async def colorize_file(params):
    log.info("Colorization has started")
    original_filename = params.get("original_filename")
    if not original_filename:
        return

    painted_filename = params.get("painted_filename")
    if not painted_filename:
        return

    # part for image colorization
    # todo should pass new filename
    log.info("Colorization has finished")
    return original_filename
