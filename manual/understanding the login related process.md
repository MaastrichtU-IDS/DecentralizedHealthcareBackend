# Understanding the Login Related Process

## 1. Registration

1.1 **Initial Setup**

> To initiate the login process, new users must first complete the registration. Essential details required are username, email, and password. For a more comprehensive profile, additional information outlined in the [create_user](https://maastrichtu-ids.github.io/DecentralizedHealthcareBackend/accounts.html#accounts.models.UserManager.create_user) interface may be provided.

1.2 **Submission and Account Creation**

> The collected registration data should be submitted to the endpoint: `http://ip_address:port/user/register`. Upon submission, LUCE processes this information to establish a [User](https://maastrichtu-ids.github.io/DecentralizedHealthcareBackend/accounts.html#accounts.models.User) instance in the database. Concurrently, an Ethereum account, comprising a private and public key, is created for each user, facilitating interactions with the Ethereum blockchain.

## 2. Login

2.1 **Accessing the System**
Post-registration, users are enabled to log in. The login credentials, specifically the username (which is the registered email address) and password, must be sent to `http://ip_address:port/user/login`. LUCE authenticates these credentials and, upon successful validation, issues a token to the user.

## 3. Updating user profile

3.1 **Profile Modification**

> Users can update their profile by sending a request to `http://ip_address:port/user/authenticated/update`. This request should include the details intended for modification.
