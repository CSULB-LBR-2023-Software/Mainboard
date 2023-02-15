/*
 * Author: Nick Fan
 * Date: Feb 2023
 * Description: Logs command line arguments to a csv file.
*/

#include <fstream>

std::fstream fout;

int main(int argc, char *argv[]) {
    fout.open("log.csv", std::ios::out|std::ios::app);
    fout << argv[1] << "\n";
    fout.close();
}
