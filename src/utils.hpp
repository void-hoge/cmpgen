#ifndef UTILS_HPP
#define UTILS_HPP

#include <string>
#include <iostream>

const double maxtime = 31536000; // one year

const int MINGPCNUM = 1;
const int MINCOST = 2;
const int NONE = 3;

class option {
private:
	int _objective;
	double _timelimit;
	std::string _srcfilename;
	std::string _dstfilename;
public:
	option(const int argc, const char **argv);
	int objective() const {
		return this->_objective;
	}
	double timelimit() const {
		return this->_timelimit;
	}
	std::string srcfilename() const {
		return this->_srcfilename;
	}
	std::string dstfilename() const {
		return this->_dstfilename;
	}
	void dump(std::ostream& ost=std::cerr) const;
};

#endif // include guard of UTILS_HPP
