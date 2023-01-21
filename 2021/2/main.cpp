#include <iostream>
#include <fstream>
#include <string>
#include <string_view>

int main(int argc, char const *argv[])
{
    std::fstream inputFile;
    inputFile.open("./input.txt", std::ios::in);

    // x,y
    int point[2] = {0, 0};
    // x,y,aim
    int pointTwo[3] = {0, 0, 0};

    if (inputFile.is_open())
    {

        std::string line;

        while (std::getline(inputFile, line))
        {

            int split = line.find(" ");
            std::string command = line.substr(0, split);

            int param = std::stoi(line.substr(split + 1, line.length()));

            if (command == "forward")
            {
                point[0] = point[0] + param;

                // p2: X += param; Y += param * aim
                pointTwo[0] = pointTwo[0] + param;
                pointTwo[1] = pointTwo[1] + pointTwo[2] * param;
            }
            else if (command == "down")
            {
                point[1] = point[1] + param;
                // p2: aim += param
                pointTwo[2] = pointTwo[2] + param;
            }
            else
            {
                point[1] = point[1] - param;
                // p2: aim -= param
                pointTwo[2] = pointTwo[2] - param;
            }
        }

        std::cout << "P1: " << point[0] * point[1] << std::endl;
        std::cout << "P2: " << pointTwo[0] * pointTwo[1] << std::endl;

        inputFile.close();
    }

    return 0;
}