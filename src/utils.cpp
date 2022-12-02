#include "utils.hpp"

#include <iostream>
#include <regex>
#include <iostream>
#include <string>

void usage(const char *progname) {
	std::cerr << "Usage: " << progname << " [options]" << std::endl
			  << "    <file>                                Set input the initial solution from <file>." << std::endl
			  << "                                          If this option is not presented, input is taken from standard input." << std::endl
			  << "    --help                                Print the usage." << std::endl
			  << "    --timelimit=<time in seconds>         Set time limit for solving." << std::endl
			  << "    --objective=(mingpcnum|mincost|none)  Select an objective function." << std::endl
			  << "    -o <file>                             Place the output into <file>." << std::endl
			  << "                                          If this option is not presented, the output is written to standard output." << std::endl;
}

option::option(const int argc, const char **argv) {
	std::string str;
	for (auto i = 1; i < argc; i++) {
		str += std::string(" ")+argv[i];
	}
	const std::regex re_help(" --help");
	const std::regex re_timelimit(" --timelimit=([0-9]+)");
	const std::regex re_objective(" --objective=([^ ]+)");
	const std::regex re_dstfilename(" -o ([^ ]+)");
	const std::regex re_srcfilename("([^ ]+)");
	std::smatch match;
	if (std::regex_search(str, match, re_help)) {
		usage(argv[0]);
		exit(0);
	}

	if (std::regex_search(str, match, re_objective)) {
		if (match.str(1) == "mingpcnum") {
			this->_objective = MINGPCNUM;
		}else if (match.str(1) == "mincost") {
			this->_objective = MINCOST;
		}else if (match.str(1) == "none") {
			this->_objective = NONE;
		}else {
			auto err = "Invalid objective \"" + match.str(1) + "\".";
			throw std::invalid_argument(err);
		}
		str.erase(match.position(), match.length());
	}else {
		this->_objective = MINCOST;
	}

	if (std::regex_search(str, match, re_dstfilename)) {
		this->_dstfilename = match.str(1);
		str.erase(match.position(), match.length());
	}else {
		this->_dstfilename = "";
	}

	if (std::regex_search(str, match, re_timelimit)) {
		this->_timelimit = std::stoi(match.str(1));
		str.erase(match.position(), match.length());
	}else {
		this->_timelimit = maxtime;
	}

	if (std::regex_search(str, match, re_srcfilename)) {
		this->_srcfilename = match.str();
		str.erase(match.position(), match.length());
	}else {
		this->_srcfilename = "";
	}

	if (std::regex_search(str, match, std::regex("([^ ]+)"))) {
		auto err = "Invalid command line argument \"" + match.str() + "\"";
		throw std::invalid_argument(err);
	}
}

void option::dump(std::ostream& ost) const{
	ost << std::boolalpha;
	ost << "--------------solver options--------------" << std::endl
		<< "timelimit   :  " << this->timelimit() << std::endl
		<< "objective   :  ";
	if (this->objective() == MINGPCNUM) {
		ost << "mingpcnum" << std::endl;
	}else if (this->objective() == MINCOST) {
		ost << "mincost" << std::endl;
	}else if (this->objective() == NONE) {
		ost << "none" << std::endl;
	}

	if (this->srcfilename() == "") {
		ost << "source      :  " << "standard input" << std::endl;
	}else {
		ost << "source      :  " << this->srcfilename() << std::endl;
	}
	if (this->dstfilename() == "") {
		ost << "destination :  " << "standard output" << std::endl;
	}else {
		ost << "destination :  " << this->dstfilename() << std::endl;
	}
	ost << "------------------------------------------" << std::endl;
}
