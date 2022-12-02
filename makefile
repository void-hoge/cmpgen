CC = c++
FLAG = -m64 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG
CPLEX = /opt/ibm/ILOG/CPLEX_Studio221
CPLEX_INCLUDE = -I$(CPLEX)/cplex/include -I$(CPLEX)/concert/include
CPLEX_LIB = -L$(CPLEX)/cplex/lib/x86-64_linux/static_pic -L$(CPLEX)/concert/lib/x86-64_linux/static_pic
LFLAG = -lconcert -lilocplex -lcplex -lm -lpthread -ldl
RELEASE = -O3 -mtune=native -march=native
STD = -std=c++11
DIR = build

$(DIR)/cmpgen: $(DIR)/problem.o $(DIR)/solution.o $(DIR)/utils.o $(DIR)/solver.o $(DIR)/main.o
	$(CC) $(FLAG) $(CPLEX_INCLUDE) $(CPLEX_LIB) $(DIR)/problem.o $(DIR)/solution.o $(DIR)/utils.o $(DIR)/solver.o $(DIR)/main.o -o $(DIR)/cmpgen $(LFLAG) $(STD) $(RELEASE)

$(DIR)/problem.o: src/problem.cpp
	$(CC) $(FLAG) $(CPLEX_INCLUDE) $(CPLEX_LIB) src/problem.cpp -c -o c -o $(DIR)/problem.o $(LFLAG) $(STD) $(RELEASE)

$(DIR)/solution.o: src/solution.cpp
	$(CC) $(FLAG) $(CPLEX_INCLUDE) $(CPLEX_LIB) src/solution.cpp -c -o $(DIR)/solution.o $(LFLAG) $(STD) $(RELEASE)

$(DIR)/utils.o: src/utils.cpp
	$(CC) $(FLAG) $(CPLEX_INCLUDE) $(CPLEX_LIB) src/utils.cpp -c -o $(DIR)/utils.o $(LFLAG) $(STD) $(RELEASE)

$(DIR)/solver.o: src/solver.cpp
	$(CC) $(FLAG) $(CPLEX_INCLUDE) $(CPLEX_LIB) src/solver.cpp -c -o $(DIR)/solver.o $(LFLAG) $(STD) $(RELEASE)

$(DIR)/main.o: src/main.cpp
	$(CC) $(FLAG) $(CPLEX_INCLUDE) $(CPLEX_LIB) src/main.cpp -c -o $(DIR)/main.o $(LFLAG) $(STD) $(RELEASE)


clean:
	rm $(DIR)/*
