const circomlibjs = require("circomlibjs")
const ff = require('ffjavascript')
const crypto = require('crypto')
const snarkjs = require('snarkjs')
const Web3 = require('web3')
const fs = require('fs')
const bigInt = require("big-integer");

const SECRET = "secret"
/** BigNumber to hex string of specified length */
function toHex(number, length = 32) {
    const str = number instanceof Buffer ? number.toString('hex') : ff.utils.leBuff2int(number).toString(16)

    return '0x' + str.padStart(length * 2, '0')
}
async function pedersenHash(data) {
    pedersen = await circomlibjs.buildPedersenHash()

    h = pedersen.hash(data)
    // console.log(buff2hex(h))
    return h
}

const rbigint = nbytes => ff.utils.leBuff2int(crypto.randomBytes(nbytes))

function Print(info, description = "") {
    console.log(description + ":")
    console.log(`Array: ${info}`);
    const info_text = (new TextDecoder()).decode(info)
    console.log(`Text: ${info_text}`)
    const info_bigint = ff.utils.leBuff2int(info)
    console.log("BigInt: ");
    console.log(info_bigint)
    const info_string = ff.utils.stringifyBigInts(info_bigint)
    console.log(`String: \n${info_string}`);
    const info_hex = buff2hex(info)
    console.log(`Hex: \n${info_hex}`)
}

async function createDeposit({ secret }) {

    wasm = __dirname + '/../build/circuits/commitment_js/commitment.wasm'
    zkey = __dirname + '/../commitment_final.zkey'
    // secret = (new TextEncoder()).encode("Hello");

    const deposit = { secret }
    Print(deposit.secret, "deposit.secret")

    deposit.commitment = await pedersenHash(deposit.secret)

    Print(deposit.commitment, "deposit.commitment")
    // console.log(buff2hex(deposit.commitment))
    deposit.commitmentHex = toHex(deposit.commitment)

    return deposit
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

function toSolidityInput(proof) {
    const flatProof = ff.utils.unstringifyBigInts(
        [
            proof.pi_a[0], proof.pi_a[1],
            proof.pi_b[0][1], proof.pi_b[0][0],
            proof.pi_b[1][1], proof.pi_b[1][0],
            proof.pi_c[0], proof.pi_c[1],
        ]);
    const result = {
        proof: "0x" + flatProof.map(x => toHex32(x)).join("")
    };
    if (proof.publicSignals) {

        result.publicSignals = ff.utils.hexifyBigInts(ff.utils.unstringifyBigInts(proof.publicSignals));
    }
    return result;
}

function buff2hex(buff) {
    function i2hex(i) {
        return ('0' + i.toString(16)).slice(-2);
    }
    return Array.from(buff).map(i2hex).join('');
}
let hello = "Hello"
let hash_of_hello = "0e90d7d613ab8b5ea7f4f8bc537db6bb0fa2e5e97bbac1c1f609ef9e6a35fd8b"

async function main() {

    const deposit = await createDeposit({
        secret: (new TextEncoder()).encode(hello)
    })


    const input = {
        secret: ff.utils.leBuff2int(deposit.secret)
    }

    const { proof, publicSignals } = await snarkjs.plonk.fullProve(input, wasm, zkey)
    // console.log(typeof ff.utils.unstringifyBigInts(publicSignals[0]))
    console.log("publicSignals[0]: ")
    console.log(publicSignals[0])
    console.log(ff.utils.unstringifyBigInts(publicSignals[0]))
    console.log(ff.utils.leInt2Buff(ff.utils.unstringifyBigInts(publicSignals[0])))
    Print(ff.utils.leInt2Buff(ff.utils.unstringifyBigInts(publicSignals[0])))

    // console.log(toSolidityInputPlonkPublicSignals(publicSignals[0]))

    const vKey = JSON.parse(fs.readFileSync("verification_key.json"));
    const res = await snarkjs.plonk.verify(vKey, publicSignals, proof)
    if (res === true) {
        console.log("Verification OK");
    } else {
        console.log("Invalid proof");
    }

    // console.log("Proof: ")
    // console.log(proof)
    // console.log("publicSignals: ")
    // console.log(publicSignals)

    var contractJson = require(__dirname + '/../build/contracts/Commitment.json')
    // var contractJsonFile = fs.readFileSync(__dirname + '/../build/contracts/Commitment.json')
    // const contractJson = JSON.parse(contractJsonFile)

    // console.log(contractJson)
    web3 = new Web3('http://127.0.0.1:8545')
    var netId = await web3.eth.net.getId()
    console.log(netId)

    // console.log(contractJson.networks)

    commitmentAddress = contractJson.networks[netId.toString()].address
    // console.log(commitmentAddress)
    senderAccount = (await web3.eth.getAccounts())[0]
    // console.log(senderAccount)

    var commitment = new web3.eth.Contract(contractJson.abi, commitmentAddress)
    await commitment.methods.Verify(toSolidityInputPlonkProof(proof), toSolidityInputPlonkPublicSignals(publicSignals)).send({
        from: senderAccount
    }).on('transactionHash', function (txHash) {
        console.log(`The transaction hash is ${txHash}`)
    })

}

main().then(
    () => {
        process.exit(0)
    }
)