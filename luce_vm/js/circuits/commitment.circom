pragma circom 2.0.0;
include "../node_modules/circomlib/circuits/pedersen.circom";
// computes Pedersen(nullifier + secret)

template Claim() {
    signal input secret;
    // log("circuit secret:");
    log(secret);
    signal output commitment[2];

    component commitmentHasher = Pedersen(256);

    component secretBits = Num2Bits(256);
    secretBits.in <== secret;

    for (var i = 0; i < 256; i++) {
        commitmentHasher.in[i] <== secretBits.out[i];
    }

    commitment[0] <== commitmentHasher.out[0];
    commitment[1] <== commitmentHasher.out[1];
    // log("circuit commitment:");
    // log(commitment);
}

component main = Claim();