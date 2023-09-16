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

    // console.log(publicSignals)
    // console.log(proof)

    const r = {
        proof: proof,
        public_signals: publicSignals
    }

    ctx.body = r
}

router.post('/compute_commitment', compute_commitment)
app.use(router.routes())

// app.use(route.post('/compute_commitment', compute_commitment))


app.listen(8888)