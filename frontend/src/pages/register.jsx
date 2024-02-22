import React from "react";

import {
    Text,
    TextInput,
    View
} from "react-native";

import { Picker } from "@react-native-picker/picker";

import service from "../utils/request";
import DHButton from "../utils/dh-button";
import DHModal from "../utils/DHModal";

class RegisterItemClass extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: {}
        };
        this.textInput = React.createRef();

        if ("gender" === this.props.data["key"]) {
            this.props.dataTracker(this.props.data["key"], "male")
        }
    }

    clear() {
        // console.log(this.props.data["key"])
        if (this.props.data["key"] == "gender") {
            return
        }

        this.textInput.current.clear()
    }

    render() {


        if (this.props.data["key"] === "gender") {
            return (
                <View
                    style={{
                        flexDirection: "row",

                    }}
                >
                    <Text
                        style={{
                            marginHorizontal: 12,
                            marginVertical: 10,
                            flex: 1,
                            alignContent: "center",
                            justifyContent: "center"
                        }}
                    >
                        {
                            this.props.data["description"] + ":"
                        }
                    </Text>

                    <Picker
                        style={{
                            flex: 2,
                            borderWidth: 0,
                            marginRight: 12,
                        }}

                        onValueChange={
                            (itemValue, itemIndex) => {
                                this.setState({ state: itemValue })
                                this.props.dataTracker(this.props.data["key"], itemValue)
                            }
                        }
                    >
                        <Picker.Item label="Male" value="0" />
                        <Picker.Item label="Female" value="1" />
                    </Picker>
                </View>
            )

        } else if (this.props.data["key"] === "password") {
            // TODO add a eye icon for controling password presentation
            return (
                <View
                    style={{ flexDirection: "row" }}
                >
                    <Text
                        style={{
                            marginHorizontal: 12,
                            marginVertical: 10,
                            flex: 1,
                        }}
                    >
                        {
                            this.props.data["description"] + ":"
                        }
                    </Text>

                    <TextInput
                        style={
                            [{
                                flex: 2,
                                borderBottomWidth: 1,
                                marginRight: 12,
                            }]
                        }
                        ref={this.textInput}
                        secureTextEntry={this.props.hidden}
                        placeholder={this.props.data["description"]}
                        onChangeText={
                            (_text) => {
                                this.setState({ state: _text })
                                this.props.dataTracker(this.props.data["key"], _text)
                            }
                        }
                    />
                </View>
            )
        }
        else {
            return (
                <View
                    style={{ flexDirection: "row" }}
                >
                    <Text
                        style={{
                            marginHorizontal: 12,
                            marginVertical: 10,
                            flex: 1,
                        }}
                    >
                        {
                            this.props.data["description"] + ":"
                        }
                    </Text>

                    <TextInput
                        style={
                            [{
                                flex: 2,
                                borderBottomWidth: 1,
                                marginRight: 12,
                            }]
                        }
                        ref={this.textInput}
                        secureTextEntry={this.props.hidden}
                        placeholder={this.props.data["description"]}
                        onChangeText={
                            (_text) => {
                                this.setState({ state: _text })
                                this.props.dataTracker(this.props.data["key"], _text)
                            }
                        }
                    />
                </View>
            )
        }

    }
}

function RegisterPage({ navigation }) {
    // const items = ["tom", "jerry"]
    const items = require("./page_config.json").pageConfig.registerDetailItems

    // hooks
    const [modalVisible, setModalVisible] = React.useState(false);
    const [modalContent, setModalContent] = React.useState("");
    var registerItemRefs = Object.fromEntries(
        items.map(
            (value) => ([value["key"], React.useRef(null)])
        )
    )

    // {"tom":"", "jerry":""}, for tracking the details of each fields
    var registerDetails = Object.fromEntries(
        items.map(
            (item) => ([item["key"], ""])
        )
    )

    const clearContent = (registerItemRefs) => {
        for (var key in registerItemRefs) {
            registerItemRefs[key].current.clear();
        }
    }



    const hasEmptyField = (fields) => {
        var empty_field = false;

        for (let key in fields) {
            if (fields[key].length === 0) {
                empty_field = true;
                break;
            }
        }
        return empty_field;
    }

    function dataTrace(item, value) {
        registerDetails[item] = value;

        // console.log(registerDetails)
    }

    const handlePress = (registerDetails) => {
        console.log(registerDetails)
        if (hasEmptyField(registerDetails)) {
            setModalVisible(true);
            setModalContent("Fields required but empty");
            clearContent(registerItemRefs)
            return
        }
        registerDetails["create_wallet"] = true

        if (registerDetails["gender"] == "male") {
            registerDetails["gender"] = 0
        }
        else {
            registerDetails["gender"] = 0
        }
        registerDetails["user_type"] = 1


        service.post(
            "/user/register/",
            registerDetails
        ).then(response => {
            if (200 === response.data.error.code) {
                navigation.navigate("Login")
            }
            else {
                alert(response.data.error.message)
            }
        }).catch(error => {
            alert(error)
        })
    }


    return (
        <View>
            <DHModal
                modalVisible={modalVisible}
                setModalVisible={setModalVisible}
                message={modalContent}
            />

            <View>
                {
                    items.map(
                        (value) => {
                            return (
                                <RegisterItemClass
                                    hidden={value["key"] === "password" ? true : false}
                                    ref={registerItemRefs[value["key"]]}

                                    key={value["key"]}
                                    // name={value["description"]}


                                    data={value}
                                    dataTracker={dataTrace}
                                />
                            )
                        }
                    )
                }
            </View>

            <DHButton title="Register" onPress={
                () => {
                    handlePress(registerDetails)
                }}
            />
        </View >
    )
}

export default RegisterPage;