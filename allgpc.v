module gpc1_1(input wire[0:0]src0, output wire[0:0]dst);
    assign dst[0] = src0[0];
endmodule

module gpc3_2(input wire[2:0]src0, output wire[1:0]dst);
    wire[1:0] lut0_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h66666666)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[1])
    );
    assign props[0] = lut0_out[0];
    assign genes[0] = lut0_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[2]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_carryout[0];
endmodule

module gpc6_3(input wire[5:0]src0, output wire[2:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .I5(src0[5]),
        .O6(lut0_out[0]),
        .O5(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = 0;
    assign props[3] = 0;
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = 0;
    assign genes[3] = 0;
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_carryout[1];
endmodule

module gpc7_3(input wire[6:0]src0, output wire[2:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .I5(src0[5]),
        .O6(lut0_out[0]),
        .O5(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[1])
    );
    assign props[0] = 0;
    assign props[1] = lut0_out[0];
    assign props[2] = lut1_out[0];
    assign props[3] = 0;
    assign genes[0] = src0[6];
    assign genes[1] = lut0_out[1];
    assign genes[2] = lut1_out[1];
    assign genes[3] = 0;
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[1];
    assign dst[1] = carry4_out[2];
    assign dst[2] = carry4_carryout[2];
endmodule

module gpc15_3(input wire[4:0]src0, input wire[0:0]src1, output wire[2:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h69966996)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h17e817e8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .O(lut1_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = 0;
    assign props[3] = 0;
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = 0;
    assign genes[3] = 0;
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[4]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_carryout[1];
endmodule

module gpc23_3(input wire[2:0]src0, input wire[1:0]src1, output wire[2:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h66666666)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h66666666)
    ) lut1_0_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut1_1_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .O(lut1_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[2]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_carryout[1];
endmodule

module gpc135_4(input wire[4:0]src0, input wire[2:0]src1, input wire[0:0]src2, output wire[3:0]dst);
    wire[1:0] lut0_out;
    wire[0:0] lut1_out;
    wire[0:0] lut2_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h69966996)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[1])
    );
    LUT6 #(
        .INIT(64'h17e8e817e81717e8)
    )lut1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .I4(src1[1]),
        .I5(src1[2]),
        .O(lut1_out[0])
    );
    LUT6 #(
        .INIT(64'h  1717ffffe8e800)
    )lut2_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .I4(src1[1]),
        .I5(src2[0]),
        .O(lut2_out[0])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = src1[2];
    assign genes[2] = src2[0];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[4]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_carryout[2];
endmodule

module gpc206_4(input wire[5:0]src0, input wire[1:0]src2, output wire[3:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .I5(src0[5]),
        .O6(lut0_out[0]),
        .O5(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[1])
    );
    LUT5 #(
        .INIT(32'h66666666)
    ) lut2_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .O(lut2_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut2_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .O(lut2_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = 0;
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    assign genes[3] = 0;
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_carryout[2];
endmodule

module gpc207_4(input wire[6:0]src0, input wire[1:0]src2, output wire[3:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .I5(src0[5]),
        .O6(lut0_out[0]),
        .O5(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[1])
    );
    LUT5 #(
        .INIT(32'h66666666)
    ) lut2_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .O(lut2_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut2_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .O(lut2_out[1])
    );
    assign props[0] = 0;
    assign props[1] = lut0_out[0];
    assign props[2] = lut1_out[0];
    assign props[3] = lut2_out[0];
    assign genes[0] = src0[6];
    assign genes[1] = lut0_out[1];
    assign genes[2] = lut1_out[1];
    assign genes[3] = lut2_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[1];
    assign dst[1] = carry4_out[2];
    assign dst[2] = carry4_out[3];
    assign dst[3] = carry4_carryout[3];
endmodule

module gpc215_4(input wire[4:0]src0, input wire[0:0]src1, input wire[1:0]src2, output wire[3:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h69966996)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h17e817e8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .O(lut1_out[1])
    );
    LUT5 #(
        .INIT(32'h66666666)
    ) lut2_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .O(lut2_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut2_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .O(lut2_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[4]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_carryout[2];
endmodule

module gpc223_4(input wire[2:0]src0, input wire[1:0]src1, input wire[1:0]src2, output wire[3:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h66666666)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h66666666)
    ) lut1_0_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut1_1_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .O(lut1_out[1])
    );
    LUT5 #(
        .INIT(32'h66666666)
    ) lut2_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .O(lut2_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut2_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .O(lut2_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[2]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_carryout[2];
endmodule

module gpc606_5(input wire[5:0]src0, input wire[5:0]src2, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[1:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .I5(src0[5]),
        .O6(lut0_out[0]),
        .O5(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[1])
    );
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut2_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .I5(src2[5]),
        .O6(lut2_out[0]),
        .O5(lut2_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut3_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .O(lut3_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut3_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .O(lut3_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    assign genes[3] = lut3_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

module gpc607_5(input wire[6:0]src0, input wire[5:0]src2, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[1:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .I5(src0[5]),
        .O6(lut0_out[0]),
        .O5(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[1])
    );
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut2_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .I5(src2[5]),
        .O6(lut2_out[0]),
        .O5(lut2_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut3_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .O(lut3_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut3_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .O(lut3_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    assign genes[3] = lut3_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[6]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

module gpc615_5(input wire[4:0]src0, input wire[0:0]src1, input wire[5:0]src2, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[1:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h69966996)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h17e817e8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .O(lut1_out[1])
    );
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut2_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .I5(src2[5]),
        .O6(lut2_out[0]),
        .O5(lut2_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut3_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .O(lut3_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut3_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .O(lut3_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    assign genes[3] = lut3_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[4]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

module gpc623_5(input wire[2:0]src0, input wire[1:0]src1, input wire[5:0]src2, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[1:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h66666666)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h66666666)
    ) lut1_0_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut1_1_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .O(lut1_out[1])
    );
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut2_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .I5(src2[5]),
        .O6(lut2_out[0]),
        .O5(lut2_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut3_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .O(lut3_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut3_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .I4(src2[4]),
        .O(lut3_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    assign genes[3] = lut3_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[2]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

module gpc1325_5(input wire[4:0]src0, input wire[1:0]src1, input wire[2:0]src2, input wire[0:0]src3, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[1:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h69966996)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'he81717e8)
    ) lut1_0_inst (
        .I0(src0[1]),
        .I1(src0[2]),
        .I2(src0[3]),
        .I3(src1[0]),
        .I4(src1[1]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut1_1_inst (
        .I0(src0[1]),
        .I1(src0[2]),
        .I2(src0[3]),
        .I3(src1[0]),
        .I4(src1[1]),
        .O(lut1_out[1])
    );
    LUT5 #(
        .INIT(32'h78878778)
    ) lut2_0_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .I2(src2[0]),
        .I3(src2[1]),
        .I4(src2[2]),
        .O(lut2_out[0])
    );
    LUT5 #(
        .INIT(32'hf00f0ff0)
    ) lut2_1_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .I2(src2[0]),
        .I3(src2[1]),
        .I4(src2[2]),
        .O(lut2_out[1])
    );
    LUT5 #(
        .INIT(32'h17e817e8)
    ) lut3_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src3[0]),
        .O(lut3_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut3_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src3[0]),
        .O(lut3_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    assign genes[3] = lut3_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[4]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

module gpc1343_5(input wire[2:0]src0, input wire[3:0]src1, input wire[2:0]src2, input wire[0:0]src3, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[0:0] lut2_out;
    wire[0:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h66666666)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h69966996)
    ) lut1_0_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .I2(src1[2]),
        .I3(src1[3]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut1_1_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .I2(src1[2]),
        .I3(src1[3]),
        .O(lut1_out[1])
    );
    LUT6 #(
        .INIT(64'h17e8e817e81717e8)
    )lut2_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .I2(src1[2]),
        .I3(src2[0]),
        .I4(src2[1]),
        .I5(src2[2]),
        .O(lut2_out[0])
    );
    LUT6 #(
        .INIT(64'h  1717ffffe8e800)
    )lut3_inst (
        .I0(src1[0]),
        .I1(src1[1]),
        .I2(src1[2]),
        .I3(src2[0]),
        .I4(src2[1]),
        .I5(src3[0]),
        .O(lut3_out[0])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = src2[2];
    assign genes[3] = src3[0];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[2]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

module gpc1406_5(input wire[5:0]src0, input wire[3:0]src2, input wire[0:0]src3, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[1:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT6_2 #(
        .INIT(64'h6996966996696996)
    ) lut0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .I5(src0[5]),
        .O6(lut0_out[0]),
        .O5(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h177e7ee8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'he8e8e8e8)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .I4(src0[4]),
        .O(lut1_out[1])
    );
    LUT5 #(
        .INIT(32'h69966996)
    ) lut2_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .O(lut2_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut2_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .O(lut2_out[1])
    );
    LUT5 #(
        .INIT(32'h17e817e8)
    ) lut3_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src3[0]),
        .O(lut3_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut3_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src3[0]),
        .O(lut3_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    assign genes[3] = lut3_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

module gpc1415_5(input wire[4:0]src0, input wire[0:0]src1, input wire[3:0]src2, input wire[0:0]src3, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[1:0] lut1_out;
    wire[1:0] lut2_out;
    wire[1:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h69966996)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[1])
    );
    LUT5 #(
        .INIT(32'h17e817e8)
    ) lut1_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .O(lut1_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut1_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .O(lut1_out[1])
    );
    LUT5 #(
        .INIT(32'h69966996)
    ) lut2_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .O(lut2_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut2_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src2[3]),
        .O(lut2_out[1])
    );
    LUT5 #(
        .INIT(32'h17e817e8)
    ) lut3_0_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src3[0]),
        .O(lut3_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut3_1_inst (
        .I0(src2[0]),
        .I1(src2[1]),
        .I2(src2[2]),
        .I3(src3[0]),
        .O(lut3_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = lut1_out[1];
    assign genes[2] = lut2_out[1];
    assign genes[3] = lut3_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[4]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

module gpc2135_5(input wire[4:0]src0, input wire[2:0]src1, input wire[0:0]src2, input wire[1:0]src3, output wire[4:0]dst);
    wire[1:0] lut0_out;
    wire[0:0] lut1_out;
    wire[0:0] lut2_out;
    wire[1:0] lut3_out;
    wire[3:0] genes;
    wire[3:0] props;
    wire[3:0] carry4_out;
    wire[3:0] carry4_carryout;
    LUT5 #(
        .INIT(32'h69966996)
    ) lut0_0_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[0])
    );
    LUT5 #(
        .INIT(32'hff00ff00)
    ) lut0_1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src0[3]),
        .O(lut0_out[1])
    );
    LUT6 #(
        .INIT(64'h17e8e817e81717e8)
    )lut1_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .I4(src1[1]),
        .I5(src1[2]),
        .O(lut1_out[0])
    );
    LUT6 #(
        .INIT(64'h  1717ffffe8e800)
    )lut2_inst (
        .I0(src0[0]),
        .I1(src0[1]),
        .I2(src0[2]),
        .I3(src1[0]),
        .I4(src1[1]),
        .I5(src2[0]),
        .O(lut2_out[0])
    );
    LUT5 #(
        .INIT(32'h66666666)
    ) lut3_0_inst (
        .I0(src3[0]),
        .I1(src3[1]),
        .O(lut3_out[0])
    );
    LUT5 #(
        .INIT(32'haaaaaaaa)
    ) lut3_1_inst (
        .I0(src3[0]),
        .I1(src3[1]),
        .O(lut3_out[1])
    );
    assign props[0] = lut0_out[0];
    assign props[1] = lut1_out[0];
    assign props[2] = lut2_out[0];
    assign props[3] = lut3_out[0];
    assign genes[0] = lut0_out[1];
    assign genes[1] = src1[2];
    assign genes[2] = src2[0];
    assign genes[3] = lut3_out[1];
    CARRY4 CARRY4_inst (
        .CO(carry4_carryout),
        .O(carry4_out),
        .CI(0),
        .CYINIT(src0[4]),
        .DI(genes),
        .S(props)
    );
    assign dst[0] = carry4_out[0];
    assign dst[1] = carry4_out[1];
    assign dst[2] = carry4_out[2];
    assign dst[3] = carry4_out[3];
    assign dst[4] = carry4_carryout[3];
endmodule

