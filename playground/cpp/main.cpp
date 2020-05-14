#include <iostream>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;


string INPUT_DIR = "./input/";
string OUTPUT_DIR = "./output/";
double PRECISION = 0.01;
int WINDOW_SIZE = 3;
double VARIANCE_MULTIPLIER = 0.6;
double MIN_SIGMA = 0.000002;


vector<int> preprocess(string original_filepath, string marked_filepath) {
    Mat original_file = imread(original_filepath, CV_LOAD_IMAGE_COLOR);
    Mat marked_file = imread(marked_filepath, CV_LOAD_IMAGE_COLOR);
    OutputArray marked_array
}


void colorize(string original_filepath, string marked_filepath, string output_filepath) {

}

int main(int argc, char** argv) {
    if (argc > 1) {
        string filename = argv[1];
        string original_filepath = INPUT_DIR + "/" + filename;
        string marked_filepath = INPUT_DIR + "/marked_" + filename;
        string output_filepath = OUTPUT_DIR + "/" + filename;
        colorize(original_filepath, marked_filepath, output_filepath);
    } else {
        cout << "Please, write filename as argument\n";
    }
    return 0;
}
