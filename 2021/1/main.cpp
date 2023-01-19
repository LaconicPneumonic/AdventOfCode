#include <iostream>
#include <fstream>
#include <climits>
#include <string>

using namespace std;

int main(int argc, char const *argv[])
{
    fstream inputFile;
    inputFile.open("./input.txt", ios::in | ios::out);

    int i = INT_MAX;

    int ret = 0;
    int retTwo = 0;

    int a;
    int b;
    int c;
    int prevSum = INT_MAX;

    if (inputFile.is_open())
    {

        string line;

        while (getline(inputFile, line))
        {

            if (i < stoi(line))
            {

                ret = ret + 1;
            }

            if (!(a == 0 || b == 0 || c == 0))
            {

                if (prevSum < (a + b + c))
                {

                    retTwo = retTwo + 1;
                }

                prevSum = (a + b + c);
            }

            c = b;
            b = a;
            a = stoi(line);

            i = stoi(line);
        }

        if (i < stoi(line))
        {

            ret = ret + 1;
        }

        if (!(a == 0 || b == 0 || c == 0))
        {

            if (prevSum < (a + b + c))
            {

                retTwo = retTwo + 1;
            }

            prevSum = (a + b + c);
        }

        inputFile.close();
    }

    cout << ret << endl;
    cout << retTwo << endl;

    return 0;
}