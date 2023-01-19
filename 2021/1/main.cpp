#include <iostream>
#include <fstream>
#include <climits>
#include <string>
#include <queue>

int main(int argc, char const *argv[])
{
    std::fstream inputFile;
    inputFile.open("./input.txt", std::ios::in);

    int retOne = 0;
    int retTwo = 0;

    int i = INT_MAX;
    std::queue<int> valQueue;
    int prevSum = 0;

    if (inputFile.is_open())
    {

        std::string line;
        int lineValue = 0;

        while (std::getline(inputFile, line))
        {

            lineValue = std::stoi(line);

            if (i < lineValue)
            {
                retOne++;
            }

            if (valQueue.size() == 3)
            {

                if (prevSum < lineValue + prevSum - valQueue.front())
                {
                    retTwo++;
                }

                prevSum = prevSum - valQueue.front();
                valQueue.pop();
            }

            prevSum = prevSum + lineValue;
            valQueue.push(lineValue);

            i = lineValue;
        }

        inputFile.close();
    }

    std::cout << "P1: " << retOne << std::endl;
    std::cout << "P2: " << retTwo << std::endl;

    return 0;
}