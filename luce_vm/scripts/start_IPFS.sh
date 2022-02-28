wget https://dist.ipfs.io/go-ipfs/v0.7.0/go-ipfs_v0.7.0_linux-amd64.tar.gz
tar -xvzf go-ipfs_v0.7.0_linux-amd64.tar.gz
cd go-ipfs
sudo bash install.sh
cd ..
rm go-ipfs_v0.7.0_linux-amd64.tar.gz
ipfs init
ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080
ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001
ipfs daemon &

    