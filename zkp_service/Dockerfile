FROM node:20
WORKDIR /usr/src/js

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# # Add Rust to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

RUN git clone https://github.com/iden3/circom.git
RUN cd circom && git checkout tags/v2.1.6 && cargo build --release
RUN cd circom && cargo install --path circom

# COPY package*.json ./

# RUN npm install

COPY . .
RUN npm install


EXPOSE 8888

CMD ["node", "src/koa/koa.js"]
