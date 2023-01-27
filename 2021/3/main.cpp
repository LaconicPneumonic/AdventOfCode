#include <iostream>
#include <bitset>
#include <cmath>
#include <fstream>
#include <string>
#include <string_view>
#include <vector>

template <class T>
void printVector(std::vector<T> const &a)
{
    std::cout << "[ ";
    for (auto v : a)
    {
        std::cout << v << ' ';
    }

    std::cout << "]" << std::endl;
}

int stringToInt(std::string const &str)
{

    int total = str.length();
    int ret = 0;
    int i = 0;

    bool handleCarriageReturn = false;

    for (auto v : str)
    {
        ret |= (v == '1') << (total - i - 1);
        i++;

        handleCarriageReturn = v == '\r';
    }

    if (handleCarriageReturn)
    {
        ret = ret >> 1;
    }
    return ret;
}

int main(int argc, char const *argv[])
{
    std::fstream inputFile;
    inputFile.open("./input.txt", std::ios::in);

    /**
     * Read line by line and for each bit use the Boyer-Moore majority vote algorithm
     * https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm
     */

    std::vector<bool> items;

    if (!inputFile.is_open())
    {

        std::cout << "FAILURE" << std::endl;
        return 1;
    }

    std::string line;
    std::getline(inputFile, line);

    int total = 1;

    for (size_t i = 0; i < line.size() - 1; i++)
    {
        items.push_back(line[i] == '1');
    }

    std::vector<int> scores(items.size(), 1);

    while (std::getline(inputFile, line))
    {
        total++;

        for (size_t i = 0; i < items.size(); i++)
        {
            bool val = line[i] == '1';

            if (scores[i] == 0)
            {
                items[i] = val;
                scores[i] = 1;
            }
            else if (items[i] == val)
            {
                scores[i]++;
            }
            else
            {
                scores[i]--;
            }
        }
    }

    int ret = 0;

    for (size_t i = 0; i < items.size(); i++)
    {
        ret |= items[i] << (items.size() - i - 1);
    }

    printVector(items);
    std::cout << "P1: " << ret * (((1 << items.size()) - 1) ^ ret) << std::endl;

    // problem 2
    int j = 0;
    std::vector<bool> oxygen(total, false);
    std::vector<bool> carbon(total, false);

    // iterating through entire file "items.size()" times
    // if i iterated by available index, this could be done in O(N)
    // since I am cutting my search space by half every time
    // N + N/2 + N/4 + ... + 1 roughly = 2n => O(N)

    for (size_t i = 0; i < items.size(); i++)
    {

        inputFile.clear();
        inputFile.seekg(0);

        int oxygenScore = 0;
        int carbonScore = 0;
        int oxygenTotal = 0;
        int carbonTotal = 0;

        j = 0;

        // printVector(carbon);

        while (std::getline(inputFile, line))
        {
            if (!oxygen[j])
            {

                oxygenScore += line[i] == '1';
                oxygenTotal++;
            }

            if (!carbon[j])
            {

                carbonScore += line[i] == '1';
                carbonTotal++;
            }

            j++;
        }

        inputFile.clear();
        inputFile.seekg(0);

        // favor one in tie breaker
        bool oxygenMajority = 2 * oxygenScore >= oxygenTotal;
        // favor zero in tie breaker
        bool carbonMinority = 2 * carbonScore < carbonTotal;

        // std::cout << "Minority for " << i << " is " << carbonMinority << std::endl;

        j = 0;

        while (std::getline(inputFile, line))
        {

            if ((line[i] == '1') != oxygenMajority && oxygenTotal != 1)
            {

                oxygen[j] = true;
            }

            if ((line[i] == '1') != carbonMinority && carbonTotal != 1)
            {

                carbon[j] = true;
            }

            j++;
        }
    }

    inputFile.clear();
    inputFile.seekg(0);

    j = 0;

    int p2 = 1;
    while (std::getline(inputFile, line))
    {

        if (!oxygen[j])
        {
            std::cout << "OXY: " << stringToInt(line) << std::endl;

            p2 *= stringToInt(line);
        }

        if (!carbon[j])
        {
            std::cout << "CO: " << stringToInt(line) << std::endl;
            p2 *= stringToInt(line);
        }

        j++;
    }

    inputFile.close();

    std::cout << "P2: " << p2 << std::endl;

    return 0;
}