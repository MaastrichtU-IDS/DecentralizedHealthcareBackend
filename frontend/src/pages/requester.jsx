import React from "react";
import AsyncStorage from '@react-native-async-storage/async-storage';

import {
    ScrollView,
    View,
    Text,
    TextInput,
} from "react-native";

import Checkbox from "expo-checkbox";
import { Ionicons } from '@expo/vector-icons';

import styles from "../utils/style-sheet";
import DHButton from "../utils/dh-button";
import DHModal from "../utils/DHModal";

import service from "../utils/request";

const DATA = [
    {
        id: 'bd7acbea-c1b1-46c2-aed5-3ad53abb28baaaaaaaaaaaaaaaaaaaaaaa',
        title: 'First Item',
        description: "first desfirst desfirst desfirst desfirst desfirst desfirst desfirst desfirst desfirst desfirst desfirst desfirst desfirst desfirst desfirst des"
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-fbd91aa97f63',
        title: 'Second Item',
        description: "second des"

    },
    {
        id: '58694a0f-3da1-471f-bd96-145571e29d72',
        title: 'Third Item',
        description: "third des"
    },
];

class DHCheckbox extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isChecked: false,
            disabled: props.disabled
        }
    }

    change(status) {
        this.setState(status)
    }

    check() {
        this.change({ isChecked: true })
    }

    uncheck() {
        this.change({ isChecked: false })
    }

    clear() {
        this.uncheck()
        this.props.onSelected(this.props.keyText, false)
    }

    render() {
        return (
            <Checkbox
                value={this.state.isChecked}
                disabled={this.props.disabled}
                onValueChange={
                    () => {
                        this.setState(
                            {
                                isChecked: !(this.state.isChecked)
                            }
                        )

                        // update to next rendering
                        this.props.onSelected(this.props.keyText, !(this.state.isChecked))
                    }
                }
            />
        )
    }
}

class StatementItemClass extends React.Component {
    constructor(props) {
        super(props)
        this.checkbox = React.createRef()
    }

    clear() {
        this.checkbox.current.clear()
    }

    render() {
        return (
            <View
                style={
                    [
                        this.props.style,
                        {
                            flexDirection: "row"
                        }
                    ]
                }
            >
                <DHCheckbox
                    ref={this.checkbox}
                    text={this.props.text}
                    keyText={this.props.keyText}
                    disabled={this.props.disabled}
                    onSelected={this.props.onSelected}
                />

                <Text
                    style={{
                        marginLeft: 12
                    }}
                >
                    {this.props.text}
                </Text>

                <Ionicons
                    name="information-circle-outline"
                    onPress={
                        () => {
                            // alert("hello world")
                            this.props.modalControl(true, this.props.description)
                        }
                    }
                >

                </Ionicons>

            </View>
        )
    }
}

function MainCategory(props) {
    const [state, setState] = React.useState(false);

    var subcategoryRef = Object.fromEntries(
        props.data["Subcategories"].map(
            (value) => ([value["Name"], React.createRef()])
        )
    )

    var testRef = React.createRef();
    var subStatementStatus = Object.fromEntries(
        props.data["Subcategories"].map(
            (value) => ([value["Key"], false])
        )
    )

    const updateSubStatementStatus = (statement, status) => {
        subStatementStatus[statement] = status

        // console.log(subStatementStatus)
        props.onSelected(props.keyText, subStatementStatus)
    }

    const clearSubStatus = () => {
        for (var sub in subcategoryRef) {
            subcategoryRef[sub].current.clear()
        }
    }

    return (
        <View>
            <StatementItemClass
                modalControl={props.modalControl}

                ref={testRef}
                style={{
                    margin: 12
                }}
                text={props.data["Name"]}

                // No descripion for main category
                description={props.data["Name"]}
                disabled={false}
                onSelected={
                    () => {
                        if (state) {
                            clearSubStatus()
                        }
                        setState(!state)
                    }
                }
            />

            {
                props.data["Subcategories"].map(
                    (sub) => {
                        // console.log(sub)
                        return (
                            <StatementItemClass
                                style={{
                                    marginLeft: 24,
                                    margin: 12
                                }}
                                ref={subcategoryRef[sub["Name"]]}
                                modalControl={props.modalControl}

                                key={sub["Name"]}
                                text={sub["Name"]}
                                keyText={sub["Key"]}
                                description={sub["Description"]}

                                disabled={!state}
                                onSelected={updateSubStatementStatus}
                            />
                        )
                    }
                )
            }
        </View >
    )
}

function StatementItems(props) {
    var statementStatus = Object.fromEntries(
        props.items.map(
            (value) => ([value["Key"], {}])
        )
    )

    // console.log(statementStatus)

    const updateStatementStatus = (statement, status) => {
        statementStatus[statement] = status
        props.onUpdate(statementStatus)
    }

    return (
        <ScrollView style={{
            margin: 12
        }}>
            {
                props.items.map(
                    (value) => {
                        return (
                            <MainCategory
                                key={value["Name"]}
                                text={value["Name"]}
                                // subcategory={value["Subcategories"]}
                                keyText={value["Key"]}

                                data={value}
                                onSelected={updateStatementStatus}
                                modalControl={props.modalControl}
                            />
                        )
                    }
                )
            }
        </ScrollView >
    );
}

function RequesterPage({ navigation }) {

    const [searchContent, onChangeSearchContent] = React.useState("");
    const [modalVisible, setModalVisible] = React.useState(false);
    const [modalContent, setModalContent] = React.useState("");
    const modalControl = (visible, content) => {
        setModalVisible(visible)
        setModalContent(content)
    }

    const purposeStatements =
        require("./page_config.json").pageConfig.purposeStatementItemsPro;


    // for main categories
    var selectedPurposeStatements = Object.fromEntries(
        purposeStatements.map(
            (value) => ([value["Key"], []])
        )
    )

    // console.log(selectedPurposeStatements)

    const updateSelectedStatements = (statementStatus) => {
        selectedPurposeStatements = statementStatus
        console.log(selectedPurposeStatements)
    }

    const onPressButton = () => {

        // for debuging dataset page


        if (0 === searchContent.length) {
            setModalVisible(true)
            setModalContent("Please type the search content")
            return
        }

        var submitData = { "search_content": searchContent };
        submitData = Object.assign(submitData, selectedPurposeStatements)
        console.log(submitData)
        retrieveToken().then((tok) => {
            var token = tok

            service.defaults.headers.common["Authorization"] = "Token " + token;

            service.post(
                "/contract/search/",
                submitData
            ).then(response => {

                if (200 === response.data.error.code) {
                    navigation.navigate("Dataset", { data: response.data.data.contracts, token:token, searchContent:submitData});
                }
            }).catch(err => {
                alert(err)
            })
        })

    }



    const retrieveToken = async (token) => {
        try {
            const token = await AsyncStorage.getItem("@token");
            return token
        } catch (e) {
            console.log(e)
        }
    }

    return (
        <View style={styles.container}>

            <View style={{
                flexDirection: "row",
                margin: 12
            }} >

                <DHModal
                    modalVisible={modalVisible}
                    setModalVisible={setModalVisible}
                    message={modalContent}
                />

                <TextInput
                    style={[styles.textInput, { flex: 1 }]}
                    onChangeText={onChangeSearchContent}
                />

                <DHButton
                    title="Search"
                    onPress={onPressButton}
                />
            </View>

            <Text
                style={{
                    marginLeft: 12
                }}
            >
                Please choose for what purposes you would like to use the dataset:
            </Text>

            <StatementItems
                items={purposeStatements}
                // data={selectedPurposeStatements}
                onUpdate={updateSelectedStatements}
                modalControl={modalControl}

            />
        </View >
    );
}

export default RequesterPage;