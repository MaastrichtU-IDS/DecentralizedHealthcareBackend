const path = require("path");

const Scalar = require("ffjavascript").Scalar;

const buildPedersenHash = require("circomlibjs").buildPedersenHash;
const buildBabyJub = require("circomlibjs").buildBabyjub;

const wasm_tester = require("circom_tester").wasm;

function buffer2bits(buff) {
    const res = new Array(buff.length * 8);
    for (let i = 0; i < buff.length; i++) {
        const b = buff[i];
        res[i * 8] = (b & 0x01);
        res[i * 8 + 1] = (b & 0x02) >> 1;
        res[i * 8 + 2] = (b & 0x04) >> 2;
        res[i * 8 + 3] = (b & 0x08) >> 3;
        res[i * 8 + 4] = (b & 0x10) >> 4;
        res[i * 8 + 5] = (b & 0x20) >> 5;
        res[i * 8 + 6] = (b & 0x40) >> 6;
        res[i * 8 + 7] = (b & 0x80) >> 7;
    }
    return res;
}

describe("Commitment test", function () {
    let babyJub
    let pedersen;
    let F;
    let circuit;
    this.timeout(100000);

    before(async () => {

        babyJub = await buildBabyJub();
        F = babyJub.F;
        pedersen = await buildPedersenHash();

        circuit_path = __dirname + '/../circuits/commitment.circom'
        // console.log(circuit_path)
        circuit = await wasm_tester(circuit_path);
    });

    it("Should pedersen with hello", async () => {
        let w;

        const b = Buffer.from("hello");
        console.log(b);

        const o = F.toObject(b);
        console.log(o);



        w = await circuit.calculateWitness({ secret: o }, true);
        // console.log(w);

        // bit = buffer2bits(b);
        // const hello = (new TextEncoder()).encode("hello");
        console.log(buffer2bits(b));
        const h = pedersen.hash("hello");

        // console.log(h);

        const hP = babyJub.unpackPoint(h);
        // console.log([F.toObject(hP[0]), F.toObject(hP[1])]);

        await circuit.assertOut(w, { commitment: [F.toObject(hP[0]), F.toObject(hP[1])] });

    });
});