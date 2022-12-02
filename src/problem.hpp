#ifndef PROBLEM_HPP
#define PROBLEM_HPP

#include <ilcplex/ilocplex.h>
#include <iostream>

using IloNumVarMatrix = IloArray<IloNumVarArray>;
using IloNumVar3Matrix = IloArray<IloNumVarMatrix>;
using IloNumMatrix = IloArray<IloNumArray>;
using IloNum3Matrix = IloArray<IloNumMatrix>;

class problem {
public:
	IloEnv env;
	IloInt stagenum;
	IloInt stagemin;
	IloInt stagemax;
	IloInt colnum;
	IloInt finalstage;
	IloInt gpcnum;
	IloInt gpcincolnum;
	IloNumArray gpcinwidth;
	IloNumMatrix gpcin;
	IloNumArray gpcout;
	IloNumArray gpccost;
	IloNumArray initialstage;
	IloInt gpclimit;
	IloInt collimit;
	problem();
	problem(std::istream& ist);
	problem(const problem& prob);
	void dump(std::ostream& ost);
};

#endif // include guard of PROBLEM_HPP
