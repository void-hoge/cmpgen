module gpc1_1(
        input wire [0:0] src0,
        output wire [0:0] dst);
    assign dst[0:0] = 
        (src0[0]<<0);
endmodule

module gpc3_2(
        input wire [2:0] src0,
        output wire [1:0] dst);
    assign dst[1:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0);
endmodule

module gpc7_3(
        input wire [6:0] src0,
        output wire [2:0] dst);
    assign dst[2:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+(src0[5]<<0)+(src0[6]<<0);
endmodule

module gpc15_3(
        input wire [4:0] src0,
        input wire [0:0] src1,
        output wire [2:0] dst);
    assign dst[2:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+
        (src1[0]<<1);
endmodule

module gpc23_3(
        input wire [2:0] src0,
        input wire [1:0] src1,
        output wire [2:0] dst);
    assign dst[2:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+
        (src1[0]<<1)+(src1[1]<<1);
endmodule

module gpc623_5(
        input wire [2:0] src0,
        input wire [1:0] src1,
        input wire [5:0] src2,
        output wire [4:0] dst);
    assign dst[4:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+
        (src1[0]<<1)+(src1[1]<<1)+
        (src2[0]<<2)+(src2[1]<<2)+(src2[2]<<2)+(src2[3]<<2)+(src2[4]<<2)+(src2[5]<<2);
endmodule

module gpc606_5(
        input wire [5:0] src0,
        input wire [5:0] src2,
        output wire [4:0] dst);
    assign dst[4:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+(src0[5]<<0)+
        (src2[0]<<2)+(src2[1]<<2)+(src2[2]<<2)+(src2[3]<<2)+(src2[4]<<2)+(src2[5]<<2);
endmodule

module gpc615_5(
        input wire [4:0] src0,
        input wire [0:0] src1,
        input wire [5:0] src2,
        output wire [4:0] dst);
    assign dst[4:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+
        (src1[0]<<1)+
        (src2[0]<<2)+(src2[1]<<2)+(src2[2]<<2)+(src2[3]<<2)+(src2[4]<<2)+(src2[5]<<2);
endmodule

module gpc1415_5(
        input wire [4:0] src0,
        input wire [0:0] src1,
        input wire [3:0] src2,
        input wire [0:0] src3,
        output wire [4:0] dst);
    assign dst[4:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+
        (src1[0]<<1)+
        (src2[0]<<2)+(src2[1]<<2)+(src2[2]<<2)+(src2[3]<<2)+
        (src3[0]<<3);
endmodule

module gpc1406_5(
        input wire [5:0] src0,
        input wire [3:0] src2,
        input wire [0:0] src3,
        output wire [4:0] dst);
    assign dst[4:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+(src0[5]<<0)+
        (src2[0]<<2)+(src2[1]<<2)+(src2[2]<<2)+(src2[3]<<2)+
        (src3[0]<<3);
endmodule

module gpc1325_5(
        input wire [4:0] src0,
        input wire [1:0] src1,
        input wire [2:0] src2,
        input wire [0:0] src3,
        output wire [4:0] dst);
    assign dst[4:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+
        (src1[0]<<1)+(src1[1]<<1)+
        (src2[0]<<2)+(src2[1]<<2)+(src2[2]<<2)+
        (src3[0]<<3);
endmodule

module gpc1343_5(
        input wire [2:0] src0,
        input wire [3:0] src1,
        input wire [2:0] src2,
        input wire [0:0] src3,
        output wire [4:0] dst);
    assign dst[4:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+
        (src1[0]<<1)+(src1[1]<<1)+(src1[2]<<1)+(src1[3]<<1)+
        (src2[0]<<2)+(src2[1]<<2)+(src2[2]<<2)+
        (src3[0]<<3);
endmodule

module gpc2135_5(
        input wire [4:0] src0,
        input wire [2:0] src1,
        input wire [0:0] src2,
        input wire [1:0] src3,
        output wire [4:0] dst);
    assign dst[4:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+
        (src1[0]<<1)+(src1[1]<<1)+(src1[2]<<1)+
        (src2[0]<<2)+
        (src3[0]<<3)+(src3[1]<<3);
endmodule

module gpc135_4(
        input wire [4:0] src0,
        input wire [2:0] src1,
        input wire [0:0] src2,
        output wire [3:0] dst);
    assign dst[3:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+
        (src1[0]<<1)+(src1[1]<<1)+(src1[2]<<1)+
        (src2[0]<<2);
endmodule

module gpc223_4(
        input wire [2:0] src0,
        input wire [1:0] src1,
        input wire [1:0] src2,
        output wire [3:0] dst);
    assign dst[3:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+
        (src1[0]<<1)+(src1[1]<<1)+
        (src2[0]<<2)+(src2[1]<<2);
endmodule

module gpc207_4(
        input wire [6:0] src0,
        input wire [1:0] src2,
        output wire [3:0] dst);
    assign dst[3:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+(src0[5]<<0)+(src0[6]<<0)+
        (src2[0]<<2)+(src2[1]<<2);
endmodule

module gpc215_4(
        input wire [4:0] src0,
        input wire [0:0] src1,
        input wire [1:0] src2,
        output wire [3:0] dst);
    assign dst[3:0] = 
        (src0[0]<<0)+(src0[1]<<0)+(src0[2]<<0)+(src0[3]<<0)+(src0[4]<<0)+
        (src1[0]<<1)+
        (src2[0]<<2)+(src2[1]<<2);
endmodule

