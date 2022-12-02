#include "solution.hpp"

solution::solution(std::istream& ist): problem(ist) {
	this->gpcusage.resize(this->stagenum-1);
	for (auto i = 0; i < this->gpcusage.size(); i++) {
		this->gpcusage[i].resize(this->colnum);
		for (auto j = 0; j < this->gpcusage[i].size(); j++) {
			this->gpcusage[i][j].resize(this->gpcnum);
			for (auto k = 0; k < this->gpcusage[i][j].size(); k++) {
				this->gpcusage[i][j][k] = 0;
			}
		}
	}
	this->stages.resize(this->stagenum);
	for (auto i = 0; i < this->stages.size(); i++) {
		this->stages[i].resize(this->colnum);
		for (auto j = 0; j < this->stages[i].size(); j++) {
			this->stages[i][j] = 0;
		}
	}
	for (auto i = 0; i < this->gpcusage.size(); i++) {
		for (auto j = 0; j < this->gpcusage[i].size(); j++) {
			for (auto k = 0; k < this->gpcusage[i][j].size(); k++) {
				int a, b, c, n;
				if (ist.eof()) {
					throw std::invalid_argument("too few inputs.");
				}
				ist >> a >> b >> c >> n;
				this->gpcusage[a][b][c] = n;
			}
		}
	}
	for (auto i = 0; i < this->stages.size(); i++) {
		for (auto j = 0; j < this->stages[i].size(); j++) {
			int a, b, n;
			if (ist.eof()) {
				throw std::invalid_argument("too few inputs.");
			}
			ist  >> a >> b >> n;
			this->stages[a][b] = n;
		}
	}
}

solution::solution(const problem& prob, std::istream& ist): problem(prob) {
	this->gpcusage.resize(this->stagenum-1);
	for (auto i = 0; i < this->gpcusage.size(); i++) {
		this->gpcusage[i].resize(this->colnum);
		for (auto j = 0; j < this->gpcusage[i].size(); j++) {
			this->gpcusage[i][j].resize(this->gpcnum);
			for (auto k = 0; k < this->gpcusage[i][j].size(); k++) {
				this->gpcusage[i][j][k] = 0;
			}
		}
	}
	this->stages.resize(this->stagenum);
	for (auto i = 0; i < this->stages.size(); i++) {
		this->stages[i].resize(this->colnum);
		for (auto j = 0; j < this->stages[i].size(); j++) {
			this->stages[i][j] = 0;
		}
	}
	for (auto i = 0; i < this->gpcusage.size(); i++) {
		for (auto j = 0; j < this->gpcusage[i].size(); j++) {
			for (auto k = 0; k < this->gpcusage[i][j].size(); k++) {
				int a, b, c, n;
				if (ist.eof()) {
					throw std::invalid_argument("too few inputs.");
				}
				ist >> a >> b >> c >> n;
				this->gpcusage[a][b][c] = n;
			}
		}
	}
	for (auto i = 0; i < this->stages.size(); i++) {
		for (auto j = 0; j < this->stages[i].size(); j++) {
			int a, b, n;
			if (ist.eof()) {
				throw std::invalid_argument("too few inputs.");
			}
			ist  >> a >> b >> n;
			this->stages[a][b] = n;
		}
	}
}

solution::solution(const problem& prob): problem(prob) {
	this->gpcusage.resize(this->stagenum-1);
	for (auto i = 0; i < this->gpcusage.size(); i++) {
		this->gpcusage[i].resize(this->colnum);
		for (auto j = 0; j < this->gpcusage[i].size(); j++) {
			this->gpcusage[i][j].resize(this->gpcnum);
			for (auto k = 0; k < this->gpcusage[i][j].size(); k++) {
				this->gpcusage[i][j][k] = 0;
			}
		}
	}
	this->stages.resize(this->stagenum);
	for (auto i = 0; i < this->stages.size(); i++) {
		this->stages[i].resize(this->colnum);
		for (auto j = 0; j < this->stages[i].size(); j++) {
			this->stages[i][j] = 0;
		}
	}
}

solution::solution(const solution& sol): problem(sol) {
	this->gpcusage = sol.gpcusage;
	this->stages = sol.stages;
	this->elapsed = sol.elapsed;
}

void solution::dump(std::ostream& ost) {
	problem::dump(ost);
	ost << "elapsed: [";
	if (this->elapsed.size() != 0) {
		ost << elapsed[0];
		for (auto i = 1; i < this->elapsed.size(); i++) {
			ost << ", " << this->elapsed[i];
		}
	}
	ost << "]" << std::endl;
	// gpcusage
	for (auto i = 0; i < this->gpcusage.size(); i++) {
		for (auto j = 0; j < this->gpcusage[i].size(); j++) {
			for (auto k = 0; k < this->gpcusage[i][j].size(); k++) {
				ost << i << " "
					<< j << " "
					<< k << " "
					<< this->gpcusage[i][j][k] << std::endl;
			}
		}
	}
	// stages
	for (auto i = 0; i < this->stages.size(); i++) {
		for (auto j = 0; j < this->stages[i].size(); j++) {
			ost << i << " "
				<< j << " "
				<< this->stages[i][j] << std::endl;
		}
	}
}

void solution::print(std::ostream& ost) {
	ost << "STAGENUM: " << this->stagenum << std::endl
		<< "COLNUM: " << this->colnum << std::endl;
	for (auto i = 0; i < this->stages.size(); i++) {
		ost << "stage " << i << ":";
		for (auto j = 0; j < this->stages[i].size(); j++) {
			ost << " " << this->stages[i][j];
		}
		ost << std::endl;
	}
	for (auto i = 0; i < this->gpcusage.size(); i++) {
		ost << "stage " << i << " -> " << i+1 << ": ";
		auto cnt = 0;
		for (auto col = 0; col < this->gpcusage[i].size(); col++) {
			for (auto e = 0; e < this->gpcusage[i][col].size(); e++) {
				if (this->gpcusage[i][col][e] != 0) {
					cnt++;
				}
			}
		}
		ost << cnt << std::endl;
		for (auto col = 0; col < this->gpcusage[i].size(); col++) {
			for (auto e = 0; e < this->gpcusage[i][col].size(); e++) {
				if (this->gpcusage[i][col][e] != 0) {
					ost << "    (col: " << col << ", num: "
						<< this->gpcusage[i][col][e]
						<< ", GPC(";
					for (auto c = 0; c < this->gpcinwidth[e]-1; c++) {
						ost << this->gpcin[e][this->gpcinwidth[e]-1-c] << ",";
					}
					ost << this->gpcin[e][0] << ";" << this->gpcout[e] << "))" << std::endl;
				}
			}
		}
	}
	auto total_cost = 0;
	for (auto e = 0; e < this->gpcnum; e++) {
		ost << "GPC(";
		for (auto c = 0; c < this->gpcinwidth[e]-1; c++) {
			ost << this->gpcin[e][this->gpcinwidth[e]-1-c] << ",";
		}
		ost << this->gpcin[e][0] << ";" << this->gpcout[e] << ")";
		auto cnt = 0;
		auto cost = 0;
		auto tmp = 0;
		for (auto s = 0; s < this->stagenum-1; s++) {
			for (auto col = 0; col < this->colnum; col++) {
				if (this->gpcusage[s][col][e] != 0) {
					cnt += this->gpcusage[s][col][e];
					cost += this->gpcusage[s][col][e]*this->gpccost[e];
				}
			}
		}
		ost << " num: " << cnt << ", cost: " << cost << std::endl;
		total_cost += cost;
	}
	ost << "total cost: " << total_cost << std::endl;
}
