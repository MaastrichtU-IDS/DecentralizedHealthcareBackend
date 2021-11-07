alias   alice-cli="sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://alice-node:7770"
alias     bob-cli="sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://bob-node:7770"
alias charlie-cli="sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://charlie-node:7770"

printf "\n========= ALICE'S NODE ========="
printf "\nAlice's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://alice-node:7770 accounts balance alice --auth hi_alice
printf "Bob's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://alice-node:7770 accounts balance bob --auth hi_alice

printf "\n========= BOB'S NODE ========="
printf "\nAlice's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://bob-node:7770 accounts balance alice --auth hi_bob
printf "Charlie's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://bob-node:7770 accounts balance charlie --auth hi_bob

printf "\n========= CHARLIE'S NODE ========="
printf "\nBob's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://charlie-node:7770 accounts balance bob --auth hi_charlie
printf "Charlie's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://charlie-node:7770 accounts balance charlie --auth hi_charlie

sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://alice-node:7770 pay alice \
  --auth alice_password \
  --amount 200000 \
  --to http://charlie-node:7770/accounts/charlie/spsp

# sudo docker run --rm --network local-ilp interledgerrs/ilp-cli \
#   --node http://alice-node:7770 pay alice \
#   --auth alice_password \
#   --amount 200000 \
#   --to http://charlie-node:7770/accounts/charlie/spsp

printf "\n========= ALICE'S NODE ========="
printf "\nAlice's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://alice-node:7770 accounts balance alice --auth hi_alice
printf "Bob's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://alice-node:7770 accounts balance bob --auth hi_alice

printf "\n========= BOB'S NODE ========="
printf "\nAlice's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://bob-node:7770 accounts balance alice --auth hi_bob
printf "Charlie's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://bob-node:7770 accounts balance charlie --auth hi_bob

printf "\n========= CHARLIE'S NODE ========="
printf "\nBob's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://charlie-node:7770 accounts balance bob --auth hi_charlie
printf "Charlie's balance: "
sudo docker run --rm --network local-ilp interledgerrs/ilp-cli --node http://charlie-node:7770 accounts balance charlie --auth hi_charlie

printf "\n==========================================================\n"