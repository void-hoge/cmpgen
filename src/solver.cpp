#include "problem.hpp"
#include "solution.hpp"
#include "solver.hpp"
#include "utils.hpp"

#include <ilcplex/ilocplex.h>
#include <vector>
#include <regex>
#include <iostream>
#include <fstream>
#include <string>
#include <chrono>

solver::solver() {}

void solver::init_vars() {
	// gpcusage
	this->gpcusage = IloNumVar3Matrix(this->prob.env, this->prob.stagenum-1);
	for (auto i = 0; i < this->gpcusage.getSize(); i++) {
		this->gpcusage[i] =  IloNumVarMatrix(this->prob.env, this->prob.colnum);
		for (auto j = 0; j < this->gpcusage[i].getSize(); j++) {
			this->gpcusage[i][j] = IloNumVarArray(this->prob.env, this->prob.gpcnum);
			for (auto k = 0; k < this->gpcusage[i][j].getSize(); k++) {
				this->gpcusage[i][j][k] = IloIntVar(this->prob.env, 0, this->prob.gpclimit);
			}
		}
	}
	// stages
	this->stages = IloNumVarMatrix(this->prob.env, this->prob.stagenum);
	for (auto i = 0; i < this->stages.getSize(); i++) {
		stages[i] = IloNumVarArray(this->prob.env, this->prob.colnum);
		for (auto j = 0; j < this->stages[i].getSize(); j++) {
			this->stages[i][j] = IloIntVar(this->prob.env, 0, this->prob.collimit);
		}
	}
}

void solver::add_constraint_init_stage(IloModel& model) {
	for (auto col = 0; col < this->prob.colnum; col++) {
		model.add(this->stages[0][col] == this->prob.initialstage[col]);
	}
}

void solver::add_constraint_final_stage(IloModel& model) {
	for (auto col = 0; col < this->prob.colnum; col++) {
		model.add(this->stages[this->prob.stagenum-1][col] <= this->prob.finalstage);
	}
}

void solver::add_constraint_gpcinput(IloModel& model) {
	for (auto stg = 0; stg < this->prob.stagenum-1; stg++) {
		for (auto col = 0; col < this->prob.colnum; col++) {
			auto src = IloExpr(this->prob.env);
			for (auto e = 0; e < this->prob.gpcnum; e++) {
				for (auto c = 0; c < this->prob.gpcinwidth[e]; c++) {
					if (col-c >= 0) {
						src += this->gpcusage[stg][col-c][e]*this->prob.gpcin[e][c];
					}
				}
			}
			model.add(src >= this->stages[stg][col]);
			src.end();
		}
	}
}

void solver::add_constraint_gpcoutput(IloModel& model) {
	for (auto stg = 1; stg < this->prob.stagenum; stg++) {
		for (auto col = 0; col < this->prob.colnum; col++) {
			auto dst = IloExpr(this->prob.env);
			for (auto e = 0; e < this->prob.gpcnum; e++) {
				if (this->prob.gpcout[e] != 0) {
					for (auto c = col-this->prob.gpcout[e]+1; c <= col; c++) {
						if (c >= 0) {
							dst += this->gpcusage[stg-1][c][e];
						}
					}
				}
			}
			model.add(dst == this->stages[stg][col]);
			dst.end();
		}
	}
}

void solver::add_constraint_gpcio(IloModel& model) {
	for (auto stg = 0; stg < this->prob.stagenum-1; stg++) {
		for (auto col = 0; col < this->prob.colnum; col++) {
			auto gpcsrc = IloExpr(this->prob.env);
			for (auto gpc = 0; gpc < this->prob.gpcnum; gpc++) {
				for (auto c = 0; c < this->prob.gpcinwidth[gpc]; c++) {
					if (col-c >= 0) {
						gpcsrc += this->gpcusage[stg][col-c][gpc]*this->prob.gpcin[gpc][c];
					}
				}
			}
			auto gpcdst = IloExpr(this->prob.env);
			for (auto gpc = 0; gpc < this->prob.gpcnum; gpc++) {
				for (auto c = col-this->prob.gpcout[gpc]+1; c <= col; c++) {
					if (c >= 0) {
						gpcdst += this->gpcusage[stg][c][gpc];
					}
				}
			}
			model.add(IloIfThen(this->prob.env, (this->stages[stg][col]-gpcsrc) > 0, this->stages[stg][col]-gpcsrc+gpcdst == this->stages[stg+1][col]));
			model.add(IloIfThen(this->prob.env, (this->stages[stg][col]-gpcsrc) <= 0, gpcdst == this->stages[stg+1][col]));
		}
	}
}

void solver::build_constraints(IloModel& model) {
	this->init_vars();
	this->add_constraint_init_stage(model);
	this->add_constraint_final_stage(model);
//	this->add_constraint_gpcio(model);
	this->add_constraint_gpcinput(model);
	this->add_constraint_gpcoutput(model);
}

void solver::add_objective_mincost(IloModel& model) {
	auto cost = IloExpr(this->prob.env);
	for (auto stg = 0; stg < this->prob.stagenum-1; stg++) {
		for (auto col = 0; col < this->prob.colnum; col++) {
			for (auto e = 0; e < this->prob.gpcnum; e++) {
				cost += this->prob.gpccost[e]*this->gpcusage[stg][col][e];
			}
		}
	}
	model.add(IloMinimize(this->prob.env, cost));
	cost.end();
}

void solver::add_objective_mingpcnum(IloModel& model) {
	auto cost = IloExpr(this->prob.env);
	for (auto stg = 0; stg < this->prob.stagenum-1; stg++) {
		for (auto col = 0; col < this->prob.colnum; col++) {
			for (auto e = 1; e < this->prob.gpcnum; e++) {
				cost += this->gpcusage[stg][col][e];
			}
		}
	}
	model.add(IloMinimize(this->prob.env, cost));
	cost.end();
}

void solver::add_objective_minbits(IloModel& model) {
	auto bits = IloExpr(this->prob.env);
	for (auto stg = 1; stg < this->prob.stagenum-1; stg++) {
		for (auto col = 0; col < this->prob.colnum; col++) {
			bits += this->stages[stg][col];
		}
	}
	model.add(IloMinimize(this->prob.env, bits));
	bits.end();
}

solution solver::get_solution(IloCplex& cplex) {
	solution sol(this->prob);
	sol.stagemin = sol.stagenum;
	sol.stagemax = sol.stagenum;
	for (auto i = 0; i < this->gpcusage.getSize(); i++) {
		for (auto j = 0; j < this->gpcusage[i].getSize(); j++) {
			for (auto k = 0; k < this->gpcusage[i][j].getSize(); k++) {
				sol.gpcusage[i][j][k] = std::lround(cplex.getValue(this->gpcusage[i][j][k]));
			}
		}
	}
	for (auto i = 0; i < this->stages.getSize(); i++) {
		for (auto j = 0; j < this->stages[i].getSize(); j++) {
			sol.stages[i][j] = std::lround(cplex.getValue(this->stages[i][j]));
		}
	}
	return sol;
}

void solver::add_mipstart(IloCplex& cplex, solution sol) {
	IloNumVarArray vars(this->prob.env);
	IloNumArray vals(this->prob.env);
	for (auto i = 0; i < this->gpcusage.getSize(); i++) {
		for (auto j = 0; j < this->gpcusage[i].getSize(); j++) {
			for (auto k = 0; k < this->gpcusage[i][j].getSize(); k++) {
				vars.add(this->gpcusage[i][j][k]);
				vals.add(sol.gpcusage[i][j][k]);
			}
		}
	}
	for (auto i = 0; i < this->stages.getSize(); i++) {
		for (auto j = 0; j < this->stages[i].getSize(); j++) {
			vals.add(sol.stages[i][j]);
		}
	}
	cplex.addMIPStart(vars, vals);
	vars.end();
	vals.end();
}

solution solver::presolve(IloCplex& cplex, IloModel& model, int objective, double timelimit) {
	std::vector<double> elapsed;
	cplex.setParam(IloCplex::Param::TimeLimit, timelimit);
	cplex.setParam(IloCplex::Param::MIP::Limits::Solutions, 1);
	for (this->prob.stagenum = this->prob.stagemin; this->prob.stagenum <= this->prob.stagemax; this->prob.stagenum++) {
		model = IloModel(this->prob.env);
		this->build_constraints(model);
		std::cerr << "stagenum: " << this->prob.stagenum << std::endl;
		cplex.extract(model);
		if (objective == MINGPCNUM) {
			this->add_objective_mingpcnum(model);
		}else if (objective == MINCOST) {
			this->add_objective_mincost(model);
		}else {
			// no objective
		}
		auto start = std::chrono::system_clock::now();
		auto is_solved = cplex.solve();
		auto end = std::chrono::system_clock::now();
		auto duration = (double)std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count()/1000;
		std::cerr << "elapsed: " << duration << std::endl;
		elapsed.push_back(duration);
		if (is_solved) {
			std::cerr << "a feasible solution found." << std::endl;
			auto sol = this->get_solution(cplex);
			sol.elapsed = elapsed;
			return sol;
		}
	}
	throw std::logic_error("no solution found(in the presolve phase, timeout or infeasible).");
}

solution solver::optimize(IloCplex& cplex, IloModel& model, solution initsol, int objective, double timelimit) {
	cplex.setParam(IloCplex::Param::TimeLimit, timelimit);
	this->build_constraints(model);
	cplex.extract(model);
	this->add_mipstart(cplex, initsol);
	if (objective == MINGPCNUM) {
		this->add_objective_mingpcnum(model);
	}else if (objective == MINCOST) {
		this->add_objective_mincost(model);
	}else {
		// no objective
	}
	auto start = std::chrono::system_clock::now();
	auto is_solved = cplex.solve();
	auto end = std::chrono::system_clock::now();
	auto duration = (double)std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count()/1000;
	if (is_solved) {
		std::cerr << "solution(s) found." << std::endl;
		auto sol = this->get_solution(cplex);
		sol.elapsed.push_back(duration);
		return sol;
	}
	throw std::logic_error("no solution found(in the optimize phase, timeout or infeasible).");
}

solution solver::solve(option& opt) {
	opt.dump();
	auto ifs = std::ifstream(opt.srcfilename());
	auto& ist = ifs.is_open() ? ifs : std::cin;
	this->prob = problem(ist);
	auto sol = solution(this->prob);
	std::string separator;
	std::getline(ist, separator);
	std::getline(ist, separator);
	if (separator.find("elapsed") != std::string::npos) {
		// a solution entered
		sol = solution(this->prob, ist);
		auto cplex = IloCplex(this->prob.env);
		cplex.setOut(std::cerr);
		auto model = IloModel(this->prob.env);
		sol = this->optimize(cplex, model, sol, opt.objective(), opt.timelimit());
	}else {
		// no solution entered
		auto cplex = IloCplex(this->prob.env);
		cplex.setOut(std::cerr);
		auto model = IloModel(this->prob.env);
		sol = this->presolve(cplex, model, opt.objective(), opt.timelimit());
	}
	return sol;
}
