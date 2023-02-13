# CMPGEN
- CMPGEN(Compressor Generator)は、一般化並列カウンタ(Generalized Parallel Counter; GPC)を用いた多入力加算器(コンプレッサ)を効率的にFPGAに実装するためのツール群です。
- IBM ILOG CPLEXを用いて、コンプレッサの最小化問題を解き、その結果をVerilog HDLのモジュールとして出力します。

## SEE ALSO
- GPCGEN: https://github.com/void-hoge/gpcgen
  - このコンプレッサツリーで用いる一般化並列カウンタを自動生成するプロジェクトです。

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
- また、`simple_gpcs.v`はiverlogなどで動作のテストを行うための、極めて単純な実装です。論理的には正しい動作をしますが、これをVivadoなどのツールで実装しても効率は低いです。

```
$ ./square.py gpclist.txt 32 2 5 | build/cmpgen --objective=none -o initial32.txt # コンプレッサ構成問題をソルバーに渡して実行可能解を計算
...
$ build/cmpgen initial32.txt --objective=mincost --timelimit=120 -o optimized32.txt # 初期解を120秒かけて最適化
...
$ ./cmpsim.py < optimized32.txt # シミュレータでランダムテスト
src: 0x11317f53cd, dst: 0x11317f53cd
src: 0x101fda15a8, dst: 0x101fda15a8
src: 0x12407105ce, dst: 0x12407105ce
src: 0x11c2e79555, dst: 0x11c2e79555
src: 0x12225bd5f9, dst: 0x12225bd5f9
src: 0x120cb2c4e1, dst: 0x120cb2c4e1
src: 0x1105e975ad, dst: 0x1105e975ad
src: 0x0f89accc3c, dst: 0x0f89accc3c
src: 0x0e6779bae5, dst: 0x0e6779bae5
src: 0x119dc3c823, dst: 0x119dc3c823
src: 0x103200ad0f, dst: 0x103200ad0f
src: 0x10786c8dd6, dst: 0x10786c8dd6
src: 0x0e7c9ec11c, dst: 0x0e7c9ec11c
src: 0x0d7aa31b3c, dst: 0x0d7aa31b3c
src: 0x0bc39e506f, dst: 0x0bc39e506f
src: 0x0d76ed9cdb, dst: 0x0d76ed9cdb
src: 0x11ce17302d, dst: 0x11ce17302d
src: 0x109cc82d17, dst: 0x109cc82d17
src: 0x10775084a4, dst: 0x10775084a4
src: 0x119cd04b57, dst: 0x119cd04b57
PASS
$ ./cmpcodegen.py < optimized32.txt > comp32.v # メインのコンプレッサモジュール(compressor)と、動作テストモジュール(behavioral_tester)を生成
$ iverilog comp32.v simple_gpcs.v -s behavioral_tester -o comp32 # 単純なGPCの記述とリンクしてコンパイル
$ ./comp32 # シミュレーション (test = (src==dst))
src: 0x0000000000, dst: 0x0000000000, test: 1
src: 0x1fffffffe0, dst: 0x1fffffffe0, test: 1
src: 0x0e39b1937f, dst: 0x0e39b1937f, test: 1
src: 0x0f2cc66d8f, dst: 0x0f2cc66d8f, test: 1
src: 0x0f90734560, dst: 0x0f90734560, test: 1
src: 0x11f1d93b44, dst: 0x11f1d93b44, test: 1
src: 0x100a99394b, dst: 0x100a99394b, test: 1
src: 0x137e34bd84, dst: 0x137e34bd84, test: 1
src: 0x0e787840d5, dst: 0x0e787840d5, test: 1
src: 0x125b0e1c5e, dst: 0x125b0e1c5e, test: 1
src: 0x0fcfd7f39e, dst: 0x0fcfd7f39e, test: 1
src: 0x0c54fd597d, dst: 0x0c54fd597d, test: 1
$ ./pipelined_cmpcodegen.py < optimized32.txt > pipelined_comp32.v # パイプライン化バージョン
$ iverilog pipelined_comp32.v simple_gpcs.v -s behavioral_tester -o pipelined_comp32
$ ./pipelined_comp32 # シミュレーション testはステージ数分戻ったsrcと等しいかどうか
src: 0xxxxxxxxxxx, dst: 0xxxxxxxxxxx, test: x
src: 0x0000000000, dst: 0xxxxxxxxxxx, test: x
src: 0x1fffffffe0, dst: 0xxxxxxxxxxx, test: x
src: 0x0e39b1937f, dst: 0xxxxxxxxxxx, test: x
src: 0x0f2cc66d8f, dst: 0x0000000000, test: 1
src: 0x0f90734560, dst: 0x1fffffffe0, test: 1
src: 0x11f1d93b44, dst: 0x0e39b1937f, test: 1
src: 0x100a99394b, dst: 0x0f2cc66d8f, test: 1
src: 0x137e34bd84, dst: 0x0f90734560, test: 1
src: 0x0e787840d5, dst: 0x11f1d93b44, test: 1
src: 0x125b0e1c5e, dst: 0x100a99394b, test: 1
src: 0x0fcfd7f39e, dst: 0x137e34bd84, test: 1
src: 0x0c54fd597d, dst: 0x0e787840d5, test: 1
src: 0x0c54fd597d, dst: 0x125b0e1c5e, test: 1
src: 0x0c54fd597d, dst: 0x0fcfd7f39e, test: 1
src: 0x0c54fd597d, dst: 0x0c54fd597d, test: 1
$
```

## パフォーマンスの例
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
  - `GPC(6,1,5,5) 4`は、このGPCのコストが4であることを表します。
#### parsegpc.py
- gpclistのパーサ
#### testgpcgen.py
- `./testgpcgen.py <gpclist>`
- GPCの単純な実装を出力します。
- iverilogなどのシミュレータで動かすためのテスト用GPCを生成します。
#### allgpcs.v
- GPCのXilinx社のFPGA向けの実装

### Problem Generator
- ILPとしてソルバーに入力する各種定数を生成し、標準出力に出力します。
- problem classは下の2つの基底クラス
#### square.py
- NxNの正方形の形に入力するコンプレッサの問題を生成します。
- `./square.py <gpclist> <N> <stagemin> <stagemax>`
- gpclistはGPCを論理的な形状を記述したファイル(gpclist.txt)です。
- `stagemin`は探索を開始するステージ数、`stagemax`は探索を終了するステージ数です。
#### popcounter.py
- Nビットのポップカウンタ
- `./popcounter.py <gpclist> <N> <stagemin> <stagemax>`

### Solver(cmpgen)
- `build/cmpgen --help`でコマンドラインオプションに関するhelpが表示されます。
#### 問題/解の入力
- ファイルまたは標準入力から解か問題を入力できます。
- 問題か解かは、入力から自動的に判定されます。
#### 解の出力
- 何も指定しない場合、標準出力に解を出力します。
- `-o <filename>`で出力先ファイルを指定します。
- ステージ数が小さすぎるか、タイムアウトして解が見つからなかった場合は`std::logic_error`を投げて終了します。
#### 目的関数の設定
- `--objective=(mingpcnum|mincost|none)`で目的関数を設定できます。
  - `mingpcnum`は(1;1)を除いたGPCの数を最小化します。
  - `mincost`はgpclistに記述されたGPCのコストの和を最小化します。
  - `none`は目的関数なしです。
- デフォルトでは`mincost`が選択されます。
- 解が存在するときは`none`が速く1つ目の解を発見し、解が存在しないときは`mingpcnum`が解の非存在性を高速に証明する傾向にあることが分かっています。
#### 制限時間の設定
- `--timelimit=<time>`で制限時間を設定できます。
- 問題を入力した場合、それぞれのステージ数でこの制限時間が適用されます。
#### 問題を入力した場合
- `stagemin`から始めて`stagemax`まで探索を行い、1つ目の解を発見したら終了します。
#### 解を入力した場合
- 入力された解を初期解として最適化を行います。


### mergegpcs.py
- ある解のGPCリストにGPCを追加します。
- これの出力をさらに`cmpgen`に入力して最適化を行えます。
- 結果は標準出力に表示されます。
- `./mergegpcs.py <solution file> <gpclist_added>`
- もとのGPCリストは、`<gpclist_added>`のサブセットである必要があります。
- `<solution>`は、`cmpgen`で出力される解です。


### Simulator
#### cmpsim.py
- 標準入力から得られた解を元に、回路をシミュレーションしてその結果を標準出力に表示します。
- 解に含まれる不要なGPC(1;1)を削除する機能も持ちます。(`cmpsim.remove_unnecessary_wires()`)
- `cmpsim.randomtest`の引数の`iteration`に回数を与えることで、テスト回数を変更できます。
- `cat <solution file> | ./cmpsim.py`

### Code Generator
- コンプレッサツリーのVerilog HDLによる実装と、そのテストベンチを出力します。
- テストベンチには全てのビットに0を入力した場合と1を入力した場合が含まれます。

#### cmpcodegen.py
- 解を標準入力に入力し、Verilog HDLのコンプレッサモジュール(`compressor`)と、そのテストベンチ(`behavioral_tester`)を出力します。
- `cat <solution file> | ./cmpcodegen.py`

#### pipelined_cmpcodegen.py
- `cmpcodegen.py`のパイプライン化バージョンです。
- 解のステージごとにレジスタを挿入してパイプライン化を行います。
- n段ごとにパイプラインすることもできるはずですが、実装していません。
- `cat <solution file> | ./pipelined_cmpcodegen.py`
- 入出力段を含めて5段のコンプレッサツリーのパイプラインレジスタの構造は以下のようになっています。
- 番号が同じ`stage wire`と`pipeline regs`は同じビット数です。
```
stage wire 0 <- src
gpc stage 0
stage wire 1
---clk---
pipeline regs 1
gpc stage 1
stage wire 2
---clk---
pipeline regs 2
gpc stage 2
stage wire 3
---clk---
pipeline regs 3
gpc stage 3
stage wire 4 -> dst
```

## バグ検出
- このプロジェクトは`cmpsm.py`と`cmpcodegen.py`の出力モジュールの2箇所でテストを行えます。
### cmpsim.pyのテストが通らないとき
- コンプレッサツリーの定式化に誤りがある可能性と、`cmpsim.py`が誤っている可能性があります。
### behavioral_testerの出力が通らないとき
- 出力されたモジュールによる和が異なるとき、GPCの実装かコードジェネレータにバグを含んでいます。
- `simple_gpcs.v`のような可能な限りシンプルなGPCの実装をコンプレッサに結合してテストすることで、GPCの実装のバグかどうかが分かるはずです。

## Author
- Mugi Noda(void-hoge)

## LICENSE
- LGPLv3
