#ifndef SOLVER_HPP
#define SOLVER_HPP

#include "problem.hpp"
#include "solution.hpp"
#include "utils.hpp"

#include <ilcplex/ilocplex.h>

class solver {
private:
	problem prob;

	IloNumVar3Matrix gpcusage;
	IloNumVarMatrix stages;

	void init_vars();
	void add_constraint_init_stage(IloModel& model);
	void add_constraint_final_stage(IloModel& model);
	void add_constraint_gpcinput(IloModel& model);
	void add_constraint_gpcoutput(IloModel& model);
	void add_constraint_gpcio(IloModel& model);
	void build_constraints(IloModel& model);
	void add_objective_mincost(IloModel& model);
	void add_objective_minbits(IloModel& model);
	void add_objective_mingpcnum(IloModel& model);

	solution get_solution(IloCplex& cplex);
	void add_mipstart(IloCplex& cplex, solution sol);
	solution presolve(IloCplex& cplex, IloModel& model, int objective, double timelimit);
	solution optimize(IloCplex& cplex, IloModel& model, solution initsol, int objective, double timelimit);
	solution iterative_optimize(IloCplex& cplex, IloModel& model, double timelimit);
public:
	solver();
	solution solve(option& opt);
};

#endif // include guard of SOLVER_HPP
