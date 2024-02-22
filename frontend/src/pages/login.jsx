import React from 'react';
import { Modal, Text, Image, TextInput, View, TouchableOpacity, SafeAreaView, Pressable } from 'react-native';

// import { API_URL, API_TOKEN } from "react-native-dotenv";
import AsyncStorage from '@react-native-async-storage/async-storage';
// import Config from 'react-native-config';
import service from '../utils/request';
import styles from '../utils/style-sheet';
import DHButton from '../utils/dh-button';
import DHModal from '../utils/DHModal';

const emailReg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
const TOKEN_KEY = '@token'

const saveToken = async (token) => {
    try {
        await AsyncStorage.setItem(TOKEN_KEY, token);
    } catch (e) {
        alert('Failed to save the data to the storage')
    }
}

function LoginPage({ navigation }) {

    const [username, onChangeUsername] = React.useState("");
    const [password, onChangePassword] = React.useState("");
    const [modalVisible, setModalVisible] = React.useState(false);
    const [modalContent, setModalContent] = React.useState("");
    // const [token, save]

    const saveToken = async (token) => {
        try {
            await AsyncStorage.setItem("@token", token)
        } catch (err) {
            console.log(err)
        }
    }

    const retrieveToken = async (token) => {
        try {
            const token = await AsyncStorage.getItem("@token");
            console.log("weird==="+token)
            return token
        } catch (e) {
            console.log(e)
        }
    }

    return (
        <View style={[styles.container, {
            justifyContent: 'center',
        }]}>

            <DHModal
                modalVisible={modalVisible}
                setModalVisible={setModalVisible}
                message={modalContent}
            />

            <View style={{
                alignItems: "center",
                margin: 12
            }}>
                <Image style={{
                    width: 195,
                    height: 47,
                }}
                    source={require('../../assets/luce.png')}
                />
            </View>

            <View>
                <TextInput style={
                    styles.textInput
                }

                    placeholder="Username: "

                    onChangeText={
                        onChangeUsername
                    }
                />

                <TextInput style={
                    styles.textInput
                }

                    placeholder="Password:"

                    onChangeText={
                        onChangePassword
                    }

                    secureTextEntry={true}
                />
            </View>

            <DHButton title="Login"
                onPress={() => {
                    // Config.API_URL;
                    // console.log(Config.API_URL)
                    if (0 === username.length || 0 === password.length) {
                        setModalVisible(true)
                        setModalContent("Please type username AND password")
                        return
                    }

                    if (!emailReg.test(username)) {
                        setModalVisible(true)
                        setModalContent("Please type correct username (Email address)")
                        return
                    }

                    var loginData = {
                        "username": username,
                        "password": password
                    }

                    service.post(
                        "/user/login/",
                        loginData
                    ).then(response => {
                        if (200 === response.data.error.code) {
                            saveToken(response.data.data.token);
                            retrieveToken().then((tok) => {
                                console.log("token ==== "+tok)
                                var token = tok
                            })
                            navigation.navigate("What do you want to do?")
                        } else {
                            setModalVisible(true)
                            setModalContent(response.data.error.message)
                            return
                        }
                    }).catch(error => {
                        alert(error)
                    })
                }}
            />

            <View style={{ alignItems: "flex-end" }}>
                <Text style={{
                    textDecorationLine: "underline",
                    padding: 10,
                    margin: 12
                }}
                    onPress={() => navigation.navigate("Register")}
                >
                    No account? register!
                </Text>
            </View>
        </View >
    );
}

export default LoginPage;