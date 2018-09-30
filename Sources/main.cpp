#include "mainwindow.h"
#include <QApplication>

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;

int main(int argc, char *argv[])
{
    cv::Mat image = cv::Mat::zeros(100, 100, CV_8UC3);
        cv::imshow("image", image);
        cv::waitKey(10);

        cout << "Hello cout!" << endl;
        cerr << "Hello cerr!" << endl;
        printf("Hello printf!");
        cout << flush;


    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
