#include <iostream>
#include <bitset>
#include <cmath>
#include <fstream>
#include <string>
#include <sstream>
#include <string_view>
#include <vector>

const std::string WHITESPACE = " \n\r\t\f\v";

std::string rtrim(const std::string &s)
{
    size_t end = s.find_last_not_of(WHITESPACE);
    return (end == std::string::npos) ? "" : s.substr(0, end + 1);
}

std::vector<std::string> readLines(std::string const &filename)
{
    std::fstream inputFile;
    inputFile.open(filename, std::ios::in);

    std::vector<std::string> lines;

    if (!inputFile.is_open())
    {

        std::cout << "FAILURE" << std::endl;
        return lines;
    }

    std::string line;

    while (std::getline(inputFile, line))
    {
        lines.push_back(rtrim(line));
    }

    return lines;
}

void printLines(std::vector<std::string> const &lines)
{
    for (auto const &line : lines)
    {
        std::cout << line << std::endl;
    }
}

void printVector(std::vector<int> const &a)
{
    std::cout << "[ ";
    for (auto v : a)
    {
        std::cout << v << ' ';
    }

    std::cout << "]" << std::endl;
}

void printBoard(std::vector<int> const &board)
{
    for (int row = 0; row < 5; row++)
    {
        for (int col = 0; col < 5; col++)
        {
            std::cout << board[row * 5 + col] << ' ';
        }
        std::cout << std::endl;
    }
}
class BingoBoard
{
public:
    std::vector<int> board;

    BingoBoard(std::vector<int> const &board) : board(board) {}

    void markNumber(int number)
    {
        for (int i = 0; i < board.size(); i++)
        {
            if (board[i] == number)
            {
                board[i] = -1;
                break;
            }
        }
    }

    bool hasWon()
    {

        for (int row = 0; row < 5; row++)
        {

            bool hasWon = true;

            for (int col = 0; col < 5; col++)
            {
                if (board[row * 5 + col] != -1)
                {
                    hasWon = false;
                }
            }

            if (hasWon)
            {
                return true;
            }
        }

        for (int col = 0; col < 5; col++)
        {

            bool hasWon = true;

            for (int row = 0; row < 5; row++)
            {
                if (board[row * 5 + col] != -1)
                {
                    hasWon = false;
                }
            }

            if (hasWon)
            {
                return true;
            }
        }

        return false;
    }

    int calculateScore()
    {
        int score = 0;

        for (int row = 0; row < 5; row++)
        {
            for (int col = 0; col < 5; col++)
            {
                if (board[row * 5 + col] != -1)
                {
                    score += board[row * 5 + col];
                }
            }
        }

        return score;
    }
};

int main(int argc, char const *argv[])
{
    std::vector<std::string> lines = readLines("./input.txt");

    bool parsingBoards = false;

    std::vector<int> draws;

    std::vector<int> tokens;

    std::vector<BingoBoard> boards;

    for (auto const &line : lines)
    {

        if (not parsingBoards)
        {
            std::istringstream f(line);
            std::string s;
            while (getline(f, s, ','))
            {
                draws.push_back(std::stoi(s));
            }

            parsingBoards = true;
        }
        else
        {
            std::istringstream iss(line);
            int value;
            while (iss >> value)
            {
                tokens.push_back(value);
            }

            if (line.size() == 0 and tokens.size() > 0)
            {

                boards.push_back(BingoBoard(tokens));
                tokens = {};
            }
        }
    }

    boards.push_back(BingoBoard(tokens));

    bool p1Solved = false;
    bool p2Start = false;
    int last_called = 0;

    for (int draw_index = 0; draw_index < draws.size(); draw_index++)
    {
        auto draw = draws[draw_index];

        int losers = 0;

        for (int board_index = 0; board_index < boards.size(); board_index++)
        {
            auto &board = boards[board_index];

            board.markNumber(draw);

            if (board.hasWon() && not p1Solved)
            {
                std::cout << "P1: WINNER " << board.calculateScore() * draw << std::endl;
                p1Solved = true;
            }

            if (!board.hasWon())
            {
                losers++;
                last_called = board_index;
            };
        }

        if (losers == 1)
        {
            p2Start = true;
        }

        if (p2Start)
        {

            boards[last_called].markNumber(draws[draw_index]);

            if (boards[last_called].hasWon())
            {
                std::cout << "P2: WINNER " << boards[last_called].calculateScore() * draw << std::endl;
                return 0;
            }
        }
    }

    return 0;
}