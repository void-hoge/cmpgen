# CMPGEN
- CMPGEN(Compressor Generator)は、一般化並列カウンタ(Generalized Parallel Counter; GPC)を用いた多入力加算器(コンプレッサ)を効率的にFPGAに実装するためのツール群です。
- IBM ILOG CPLEXを用いて、コンプレッサの最小化問題を解き、その結果をVerilog HDLのモジュールとして出力します。
- これにより、Vivado等の合成系で自動生成したときに比べ、クリティカルパス遅延をほぼ犠牲にすることなく、半分ほどの回路的コストで実装することができます。(問題によりますが)


## コンプレッサ
- コンプレッサとは2進数整数の多入力加算器です。
- 最もわかりやすい例として、ポップカウンタや乗算器に使われています。(NxNビットの乗算は、N回のシフト演算と、N個の数を足し合わせる演算によって構成されます。)
- また、最近ではBNN(Binary Neural Network)のニューロンの実装でも用いられます。(もともと、このプロジェクトはBNNで用いるためのものです。)


## 要件
- IBM ILOG CPLEX
- C++11以上に対応したコンパイラ
- GNU Make
- Python3 (辞書の順序が固定されることを前提として書いているところがあるかもしれないので、3.7以上を推奨)


## ビルド
```
$ git clone https://github.com/void-hoge/cmpgen.git
$ cd cmpgen
$ mkdir build
$ make
c++ -m64 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG -I/opt/ibm/ILOG/CPLEX_Studio221/cplex/include -I/opt/ibm/ILOG/CPLEX_Studio221/concert/include -L/opt/ibm/ILOG/CPLEX_Studio221/cplex/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio221/concert/lib/x86-64_linux/static_pic src/problem.cpp -c -o c -o build/problem.o -lconcert -lilocplex -lcplex -lm -lpthread -ldl -std=c++11 -O3 -mtune=native -march=native
c++ -m64 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG -I/opt/ibm/ILOG/CPLEX_Studio221/cplex/include -I/opt/ibm/ILOG/CPLEX_Studio221/concert/include -L/opt/ibm/ILOG/CPLEX_Studio221/cplex/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio221/concert/lib/x86-64_linux/static_pic src/solution.cpp -c -o build/solution.o -lconcert -lilocplex -lcplex -lm -lpthread -ldl -std=c++11 -O3 -mtune=native -march=native
c++ -m64 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG -I/opt/ibm/ILOG/CPLEX_Studio221/cplex/include -I/opt/ibm/ILOG/CPLEX_Studio221/concert/include -L/opt/ibm/ILOG/CPLEX_Studio221/cplex/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio221/concert/lib/x86-64_linux/static_pic src/utils.cpp -c -o build/utils.o -lconcert -lilocplex -lcplex -lm -lpthread -ldl -std=c++11 -O3 -mtune=native -march=native
c++ -m64 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG -I/opt/ibm/ILOG/CPLEX_Studio221/cplex/include -I/opt/ibm/ILOG/CPLEX_Studio221/concert/include -L/opt/ibm/ILOG/CPLEX_Studio221/cplex/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio221/concert/lib/x86-64_linux/static_pic src/solver.cpp -c -o build/solver.o -lconcert -lilocplex -lcplex -lm -lpthread -ldl -std=c++11 -O3 -mtune=native -march=native
c++ -m64 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG -I/opt/ibm/ILOG/CPLEX_Studio221/cplex/include -I/opt/ibm/ILOG/CPLEX_Studio221/concert/include -L/opt/ibm/ILOG/CPLEX_Studio221/cplex/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio221/concert/lib/x86-64_linux/static_pic src/main.cpp -c -o build/main.o -lconcert -lilocplex -lcplex -lm -lpthread -ldl -std=c++11 -O3 -mtune=native -march=native
c++ -m64 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG -I/opt/ibm/ILOG/CPLEX_Studio221/cplex/include -I/opt/ibm/ILOG/CPLEX_Studio221/concert/include -L/opt/ibm/ILOG/CPLEX_Studio221/cplex/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio221/concert/lib/x86-64_linux/static_pic build/problem.o build/solution.o build/utils.o build/solver.o build/main.o -o build/cmpgen -lconcert -lilocplex -lcplex -lm -lpthread -ldl -std=c++11 -O3 -mtune=native -march=native
$
```


## 実行例
- 下の例は、32個の32bit整数を足し合わせるコンプレッサを構成し、GPCの実装と結合してiverilogで動作確認をしています。
- `#`より右はコメントです。
- また、simple_gpcs.vはiverlogなどで動作のテストを行うための、極めて単純な実装です。論理的には正しい動作をしますが、これをVivadoなどのツールで実装しても効率は低いです。

```
$ ./square.py gpclist.txt 32 2 5 | build/cmpgen --objective=none -o initial_solution.txt # コンプレッサ構成問題をソルバーに渡して初期解を計算
...
$ build/cmpgen initial_solution.txt --objective=mincost --timelimit=120 -o optimized_solution.txt # 初期解を120秒掛けて最適化
...
$ ./solutionconv.py < optimized_solution.txt | ./cmpcodegen.py > comp32.v # 解を変換してテスト(correctが入力、simulateが出力)、verilogを出力
correct: 61097481087, simulate: 61097481087
correct: 65246360341, simulate: 65246360341
correct: 59502265228, simulate: 59502265228
correct: 61091934663, simulate: 61091934663
correct: 71032078428, simulate: 71032078428
correct: 74103422503, simulate: 74103422503
correct: 67705343742, simulate: 67705343742
correct: 66031894880, simulate: 66031894880
correct: 64895608538, simulate: 64895608538
correct: 73261521590, simulate: 73261521590
correct: 58659332956, simulate: 58659332956
correct: 69781284720, simulate: 69781284720
correct: 61290858103, simulate: 61290858103
correct: 77008920417, simulate: 77008920417
correct: 73542555034, simulate: 73542555034
correct: 70093789785, simulate: 70093789785
correct: 81696337662, simulate: 81696337662
correct: 63219576915, simulate: 63219576915
correct: 60868091025, simulate: 60868091025
correct: 67001723076, simulate: 67001723076
PASS
$ cat simple_gpcs.v >> comp32.v # GPCの実装と結合
$ iverilog comp32.v -o comp32 # iverilogでコンパイル
$ ./comp32 # テストを実行(左側が入力、右側が出力)
0ec1c8176b => 0ec1c8176b
0fa56ea05f => 0fa56ea05f
1224ad0f7e => 1224ad0f7e
0f01d827a9 => 0f01d827a9
0df8a639ed => 0df8a639ed
0ebd33db94 => 0ebd33db94
0fe822bcc6 => 0fe822bcc6
1012d35a5d => 1012d35a5d
126f381892 => 126f381892
0f31e74610 => 0f31e74610
10a2039f1b => 10a2039f1b
1100fef234 => 1100fef234
1019f2fe9e => 1019f2fe9e
0e9b62a156 => 0e9b62a156
1044e25f0c => 1044e25f0c
0ee7245025 => 0ee7245025
0e4518d1bd => 0e4518d1bd
0e8b2108c8 => 0e8b2108c8
0f41caa576 => 0f41caa576
12c262d4db => 12c262d4db
$
```

## パフォーマンス
- 32x32の正方形の入力
  - cmpgen(7200秒の最適化): 142スライス
  - naive(上と同じ出力になるように記述した上でVivadoで合成): 174スライス


## プログラムの構成

### GPC list
- 使用するGPCのリスト
- GPCの形の横の数はコスト
- 例
  - `GPC(3;2)`は、1の位に3ビット入力して2ビット出力するGPC(全加算器)
  - `GPC(6,1,5;5)`は、1の位に5ビット、2の位に1ビット、3の位に6ビット入力するGPC
  - `GPC(6,1,5,5) 4`は、このGPCのコストが4であることを表す。
#### parsegpc.py
- gpclistのパーサ
#### testgpcgen.py
- `./testgpcgen.py <gpclist>`
- GPCの単純な実装を得る。
- iverilogなどのシミュレータで動かすためのテスト用GPCを生成する。
#### allgpcs.v
- GPCのXilinx社のFPGA向けの実装

### Problem Generator
- ILPとしてソルバーに入力する各種定数を生成し、標準出力に出力する。
- problem classは下の2つの基底クラス
#### square.py
- NxNの正方形の形に入力する。
- `./square.py <gpclist> <N> <stagemin> <stagemax>`
- gpclistはGPCを論理的な形状を記述したファイル(gpclist.txt)
- stageminは探索を開始するステージ数、stagemaxは探索を終了するステージ数
#### popcounter.py
- Nビットのポップカウンタ
- `./popcounter.py <gpclist> <N> <stagemin> <stagemax>`

### Solver(cmpgen)
- `build/cmpgen --help`でコマンドラインオプションに関するhelpが表示される。
#### 問題/解の入力
- ファイルまたは標準入力から解か問題を入力できる。
- 問題か解かは、入力から自動的に判定される。
#### 解の出力
- 何も指定しない場合、標準出力に解を出力する。
- `-o <filename>`で出力先ファイルを指定できる。
- ステージ数が小さすぎるか、タイムアウトして解が見つからなかった場合は`std::logic_error`を投げて終了する。
#### 目的関数の設定
- `--objective=(mingpcnum|mincost|none)`で目的関数を設定できる。
  - `mingpcnum`は(1;1)を除いたGPCの数を最小化する。
  - `mincost`はgpclistに記述されたGPCのコストの和を最小化する。
  - `none`は目的関数なし。
- デフォルトでは`mincost`が選択される。
- 解が存在するときは`none`が速く1つ目の解を発見し、解が存在しないときは`mingpcnum`が解の非存在性を高速に証明する傾向にあることが分かっている。
#### 制限時間の設定
- `--timelimit=<time>`で制限時間を設定できる。
- 問題を入力した場合、それぞれのステージ数でこの制限時間が適用される。
#### 問題を入力した場合
- stageminから始めてstagemaxまで探索を行い、1つ目の解を発見したら終了する。
#### 解を入力した場合
- 入力された解を初期解として最適化を行う。


### Solution Parser/Converter
- ソルバーの解をパースし、変換する。
- solution classはproblemを継承している。
#### solutionconv.py
- 標準入力からcmpgenの出力を入力すると、cmpcodegen.pyで読み込める形式に変換し、標準出力に表示する。
- `cat solution.txt | solutionconv.py`
#### margegpcs.py
- ある解のGPCリストにGPCを追加する。
- これの出力をさらに`cmpgen`に入力して最適化を行える。
- 結果は標準出力に表示される。
- `./margegpcs.py <solution> <gpclist_added>`
- もとのGPCリストは、`<gpclist_added>`のサブセットである必要がある。
- `<solution>`は、`solutionconv.py`で変換したものではなく、`cmpgen`で出力される解


### Code Generator
#### cmpcodegen.py
- `solutionconv.py`の出力を標準入力に入力し、コンプレッサのVerilog moduleを標準出力に出力する。
- `compressor.gen_behavioral_test()`で、動作テスト用のモジュールを出力できる。
- `compressor.gen_implement_test()`で、シフトレジスタを用いた実装テスト用のモジュールを出力できる。(正方形の入力しか対応していない。)
- 入力をパースした結果から回路をシミュレーションしてテストを行える。その結果は標準エラー出力に表示される。

## バグ検出
- このプロジェクトはcmpcodegen.pyとその出力モジュールの2箇所でテストを行える。
### cmpcodegen.pyのテストが通らないとき
- コンプレッサーのモデル(解)と、`cmpcodegen.py`でパースされるモデルが食い違っている可能性が高い。
### behavioral_testが通らないとき
- 出力されたモジュールによる和が異なるとき、GPCの実装かコードジェネレータにバグを含んでいる。
- simple_gpcs.vのような可能な限りシンプルなGPCの実装をコンプレッサに結合してテストすることで、GPCの実装のバグかどうかが分かるはず。

## Author
- Mugi Noda(void-hoge)

## LICENSE
- LGPLv3
