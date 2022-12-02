#ifndef SOLUTION_HPP
#define SOLUTION_HPP

#include "problem.hpp"

#include <vector>
#include <iostream>

class solution: public problem {
public:
	std::vector<std::vector<std::vector<int>>> gpcusage;
	std::vector<std::vector<int>> stages;
	std::vector<double> elapsed;
	solution(std::istream& ist);
	solution(const problem& prob);
	solution(const problem& prob, std::istream& ist);
	solution(const solution& sol);
	void dump(std::ostream& ost);
	void print(std::ostream& ost);
};

#endif // include guard of SOLUTION_HPP
