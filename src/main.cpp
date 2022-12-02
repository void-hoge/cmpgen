#include "solver.hpp"
#include "utils.hpp"

int main(const int argc, const char **argv) {
	auto opt = option(argc, argv);
	auto slv = solver();
	auto sol = slv.solve(opt);
	sol.print(std::cerr);
	auto ofs = std::ofstream(opt.dstfilename());
	if (ofs.is_open()) {
		sol.dump(ofs);
	}else {
		sol.dump(std::cout);
	}
	return 0;
}
