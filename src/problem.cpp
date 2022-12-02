#include "problem.hpp"

problem::problem(){
	this->env = IloEnv();
	this->stagenum = 1;
	this->stagemin = 1;
	this->stagemax = 1;
	this->colnum = 0;
	this->finalstage = 0;
	this->gpcnum = 0;
	this->gpcincolnum = 0;
	this->gpclimit = 0;
	this->collimit = 0;
	this->gpcinwidth = IloNumArray(this->env);
	this->gpcin = IloNumMatrix(this->env);
	this->gpcout = IloNumArray(this->env);
	this->gpccost = IloNumArray(this->env);
	this->initialstage = IloNumArray(this->env);
}

problem::problem(std::istream& ist) {
	this->env = IloEnv();
	this->gpcinwidth = IloNumArray(this->env);
	this->gpcin = IloNumMatrix(this->env);
	this->gpcout = IloNumArray(this->env);
	this->gpccost = IloNumArray(this->env);
	this->initialstage = IloNumArray(this->env);
	ist >> this->stagemin
		>> this->stagemax
		>> this->colnum
		>> this->finalstage
		>> this->gpcnum
		>> this->gpcincolnum
		>> this->gpcinwidth
		>> this->gpcin
		>> this->gpcout
		>> this->gpccost
		>> this->initialstage
		>> this->gpclimit
		>> this->collimit;
	this->stagenum = this->stagemin;
}

problem::problem(const problem& prob) {
	this->env = prob.env;
	this->stagemin = prob.stagemin;
	this->stagemax = prob.stagemax;
	this->stagenum = prob.stagenum;
	this->colnum = prob.colnum;	
	this->finalstage = prob.finalstage;
	this->gpcnum = prob.gpcnum;
	this->gpcincolnum = prob.gpcincolnum;
	this->gpcinwidth = prob.gpcinwidth;
	this->gpcin = prob.gpcin;
	this->gpcout = prob.gpcout;
	this->gpccost = prob.gpccost;
	this->initialstage = prob.initialstage;
	this->gpclimit = prob.gpclimit;
	this->collimit = prob.collimit;
}

void problem::dump(std::ostream& ost) {
	std::cerr << "stagemin:       " ; ost << this->stagemin       << std::endl;
	std::cerr << "stagemax:       " ; ost << this->stagemax       << std::endl;
	std::cerr << "colnum:         " ; ost << this->colnum         << std::endl;
	std::cerr << "finalstage:     " ; ost << this->finalstage     << std::endl;
	std::cerr << "gpcnum:         " ; ost << this->gpcnum         << std::endl;
	std::cerr << "gpcincolnum:    " ; ost << this->gpcincolnum    << std::endl;
	std::cerr << "gpcinwidth:     " ; ost << this->gpcinwidth     << std::endl;
	std::cerr << "gpcin:          " ; ost << this->gpcin          << std::endl;
	std::cerr << "gpcout:         " ; ost << this->gpcout         << std::endl;
	std::cerr << "goccost:        " ; ost << this->gpccost        << std::endl;
	std::cerr << "initialstage:   " ; ost << this->initialstage   << std::endl;
	std::cerr << "gpclimit:       " ; ost << this->gpclimit       << std::endl;
	std::cerr << "collimit:       " ; ost << this->collimit       << std::endl;
}
