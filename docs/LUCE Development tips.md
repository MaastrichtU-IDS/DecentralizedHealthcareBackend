## 1. Introduction

To facilitate a comprehensive understanding, it's essential to explain the technical implementation of LUCE.

LUCE is developed using [Brownie](https://eth-brownie.readthedocs.io/en/stable/) for managing smart contracts and [Django](https://www.djangoproject.com/) for handling user interactions with these contracts.

In LUCE, we've streamlined the process so developers can effortlessly create, manage, and interact with smart contracts, enabling them to build their business solutions efficiently.

## 2. Steps

> Note: This guide assumes that you have already cloned this repository into your development environment.

### 2.1 Create smart contracts

1. Change Directory. Navigate to the contracts folder using the command:

```
cd luce_vm/brownie/contracts
```

2. Create Your Smart Contract File. Generate a new smart contract file with:

```
touch your_own_smart_contract.sol
```

3. Start Coding: Begin developing your smart contract.

### 2.2 (Optional) Compile Your Smart Contract

LUCE automatically compiles smart contracts during launch or within a Docker container. However, if you wish to manually compile and experiment with your smart contracts using Brownie, follow the [Brownie Instructions](https://eth-brownie.readthedocs.io/en/stable/quickstart.html)

### 2.3 Model Your Smart Contract

LUCE adopts a modular architecture. We recommend organizing smart contracts within a single [Django app](https://docs.djangoproject.com/en/5.0/intro/tutorial01/), specifically the `blockchain` app located at `luce_vm/luce_django/luce`.

To integrate your smart contract, create a model that typically inherits from [Django Models](https://docs.djangoproject.com/en/5.0/topics/db/models/). You can find examples in the `blockchain` app.

### 2.4 Test Your Smart Contract

> TODO: Elaborate on the differences between these two testing methods.

Once you've developed your smart contracts and modeled them using [Django Models](https://docs.djangoproject.com/en/5.0/topics/db/models/), you can proceed to test them. We offer two distinct testing methods:

1. Test with Brownie

If you prefer testing within Brownie, ensure you've completed step 2.2.
Follow the guide on [Writing Unit Tests](https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html#pytest) for Brownie and test your smart contracts with the development network. For example, in the `luce_vm/brownie` directory, run:
```
brownie test --network development -s
```

2. Test with Django
   For testing within Django, consult this [tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial05/) for detailed instructions.
