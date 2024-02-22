const Koa = require('koa')
const Router = require("koa-router")

const circomlibjs = require("circomlibjs")
const ff = require('ffjavascript')
const crypto = require('crypto')
const snarkjs = require('snarkjs')
const Web3 = require('web3')
const fs = require('fs')
const bigInt = require("big-integer");

const bodyParser = require('koa-bodyparser')
const wasm_tester = require("circom_tester").wasm;

const app = new Koa()
app.use(bodyParser())

const router = new Router()
function hexifyBigInts(o) {
    if (typeof (o) === "bigint" || (o instanceof bigInt)) {
        let str = o.toString(16);
        while (str.length < 64) str = "0" + str;
        str = "0x" + str;
        return str;
    } else if (Array.isArray(o)) {
        return o.map(hexifyBigInts);
    } else if (typeof o == "object") {
        const res = {};
        for (let k in o) {
            res[k] = hexifyBigInts(o[k]);
        }
        return res;
    } else {
        return o;
    }
}
function toSolidityInputPlonkPublicSignals(public_signals) {
    return hexifyBigInts(ff.utils.unstringifyBigInts(public_signals))
}

function toHex32(number) {
    let str = number.toString(16);
    while (str.length < 64) str = "0" + str;
    return str;
}

function toSolidityInputPlonkProof(proof) {
    const flatProof = ff.utils.unstringifyBigInts(
        [
            proof.A[0], proof.A[1],
            proof.B[0], proof.B[1],
            proof.C[0], proof.C[1],
            proof.Z[0], proof.Z[1],
            proof.T1[0], proof.T1[1],
            proof.T1[0], proof.T2[0],
            proof.T3[0], proof.T3[1],
            proof.eval_a, proof.eval_b,
            proof.eval_c, proof.eval_s1, proof.eval_s2, proof.eval_zw, proof.eval_r,
            proof.Wxi[0], proof.Wxi[1],
            proof.Wxiw[0], proof.Wxiw[1]
        ]
    )

    return "0x" + flatProof.map(x => toHex32(x)).join("");
}

const compute_commitment = async ctx => {
    // const secret = ctx.request.body.secret;
    const secret = (new TextEncoder()).encode(ctx.request.body.secret)

    console.log("received secret: " + secret)
    const input = {
        secret: ff.utils.leBuff2int(secret)
    }

    wasm = __dirname + '/../../build/circuits/commitment_js/commitment.wasm'
    zkey = __dirname + '/../commitment_final.zkey'
    circuit_path = __dirname + '/../../circuits/commitment.circom'
    circuit = await wasm_tester(circuit_path)


    const { proof, publicSignals } = await snarkjs.plonk.fullProve(input, wasm, zkey)

    call_data = await snarkjs.plonk.exportSolidityCallData(proof, publicSignals)
    console.log(call_data)

    // console.log(publicSignals)
    // console.log(proof)

    const r = {
        proof: proof,
        public_signals: publicSignals,
        solidity_proof: toSolidityInputPlonkProof(proof),
        solidity_public_signals: toSolidityInputPlonkPublicSignals(publicSignals),
        call_data: call_data
    }

    ctx.body = r
}

router.post('/compute_commitment', compute_commitment)
app.use(router.routes())

// app.use(route.post('/compute_commitment', compute_commitment))


app.listen(8888)