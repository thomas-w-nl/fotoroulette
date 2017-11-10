#include <zconf.h>
#include <opencv2/opencv.hpp>


std::vector<cv::Rect> getFace(cv::Mat img) {
    cv::CascadeClassifier face_cascade;
    cv::Mat imgGrey;
    cv::cvtColor(img, imgGrey, cv::COLOR_BGR2GRAY);
    std::vector<cv::Rect> faces;

    if (!face_cascade.load("haarCascades/haarcascade_frontalface_alt.xml")) {
        printf("ERROR: haarcascades failed to load.\n");
        return {};
    };

    face_cascade.detectMultiScale(imgGrey, faces, 1.1, 2, 0 | cv::CASCADE_SCALE_IMAGE, cv::Size(30, 30));
    return faces;
}

cv::Mat drawRectangle(cv::Mat img, std::vector<cv::Rect> rect) {
    for (cv::Rect face : rect) {
        int x1 = face.x;
        int x2 = (face.x + face.width);
        int y1 = face.y;
        int y2 = (face.y + face.height);

        cv::rectangle(img, cv::Point_(x1, y1), cv::Point_(x2, y2), cv::Scalar_(0, 255, 0), 1);
    }
    return img;
}

void videoCapture() {
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cout << "camera failed!";
    }
    cv::namedWindow("cam", 1);
    while (1) {
        cv::Mat frame;
        cap >> frame;
        frame = drawRectangle(frame, getFace(frame));
        cv::imshow("cam", frame);
        if (cv::waitKey(27) >= 0) break;
    }

}

void imgRecon() {
    std::string imgName = "arnold.jpg";
    cv::Mat img = cv::imread("img/" + imgName);
    img = drawRectangle(img, getFace(img));

    cv::imshow("OpenCV", img);
//    cv::imwrite("out/" + imgName, img);
    cv::waitKey(0);
}

int main() {
    chdir("/home/noeel/Documents/git/pi-fys");
    videoCapture();
//    imgRecon();
    return 1;
}
