import { Link, TabRouter } from "@react-navigation/native";
import React from "react";

import { TouchableOpacity, View, ScrollView, Text } from "react-native";
import BouncyCheckbox from "react-native-bouncy-checkbox";
import styles from "../utils/style-sheet";
import DHButton from "../utils/dh-button";
import service from "../utils/request";
import DHModal from '../utils/DHModal';


function Dataset(props) {
    const [checkState, onChangeCheckState] = React.useState(false);
    return (
        <View style={{
            flexDirection: "row",
            margin: 10,
            padding: 12,
            backgroundColor: "cornsilk",
            borderRadius: 32

        }} >
            <BouncyCheckbox
                style={{ flex: 1 }}
                onPress={
                    () => {
                        props.onSelected(!checkState);
                        onChangeCheckState(!checkState)
                    }

                }
            ></BouncyCheckbox>

            <Text
                style={{
                    // padding: 12,
                    // margin: 10,
                    // textAlign: "auto",
                    // borderWidth: 1,
                    flex: 6

                }}
            >
                {"contract id: "}
                {props.id}
                {"\n\n"}
                {"contract address: "}
                {props.contract_address}
                {"\n\n"}
                {"data description:\n"}
                {props.description}
            </Text>
        </View >
    )
}

function PageElements(props) {

    const [token, setToken]  = React.useState(props.token)
    const [searchContent, setSearcher] = React.useState(props.searchContent)
    const [modalVisible, setModalVisible] = React.useState(false);
    const [modalContent, setModalContent] = React.useState("");
    const [link, setLink] = React.useState("")

    var multiIsSelected = Object.fromEntries(
        props.data.map(
            (value) => ([value.id, false])
        )
    )

    var selectedResult = [];

    const retrieveToken = async (token) => {
        try {
            return await AsyncStorage.getItem("@token");
        } catch (e) {
            console.log(e)
        }
    }

    return (
        <View>
            <DHModal
                modalVisible={modalVisible}
                setModalVisible={setModalVisible}
                message={modalContent}
            />
            
            <ScrollView
                onPress={props.onPress}
            >
                {
                    props.data.map(
                        (value) => {
                            return (
                                <Dataset
                                    key={value.id}
                                    description={value.description}
                                    id={value.id}
                                    contract_address={value.contract_address}
                                    onSelected={
                                        (state) => {
                                            multiIsSelected[value.id] = state;

                                            if (state) {
                                                selectedResult.push(value);
                                            } else {
                                                selectedResult.splice(selectedResult.findIndex(v => v.id === value.id), 1)
                                            }
                                        }
                                    }
                                />
                            );
                        }
                    )
                }
            </ ScrollView>

            <DHButton
                title="Request"
                onPress={
                    () => {
                        if (0 === selectedResult.length) {
                            return;
                        }

                        var submitData = {"general_research_purpose": searchContent["general_research_purpose"], "HMB_research_purpose":searchContent["HMB_research_purpose"],"clinical_purpose":searchContent["clinical_purpose"]}
                        var addresses = []                        
                        for (var i = 0; i < selectedResult.length; i++){
                            console.log(selectedResult[i])
                            addresses.push(selectedResult[i]["contract_address"])

                        }
                        submitData["dataset_addresses"] = addresses
                        console.log(submitData)
                        service.defaults.headers.common["Authorization"] = "Token " + token;
                        service.post(
                            "/contract/requestAccess/",
                            submitData
                        ).then(response => {
                            if (200 === response.data.error.code) {
                                setModalVisible(true)
                                setModalContent("You were granted access to the data") 
                            }
                            else{
                                setModalVisible(true)
                                setModalContent(response.data.error.message)
                            }
                        }).catch(err => {

                            alert(err);
                        })

                     

                    }
                }
            ></DHButton>
            <DHButton
                title="Get Link"
                onPress={
                    () => {
                        if (0 === selectedResult.length) {
                            return;
                        }
                        if(selectedResult.length > 1){
                            return;
                        }

                        var submitData = {"dataset_address":selectedResult[0]["contract_address"]}
                        service.defaults.headers.common["Authorization"] = "Token " + token;
                        service.post(
                            "/contract/getLink/",
                            submitData
                        ).then(response => {
                            if (200 === response.data.error.code) {
                                setLink(response.data.data["link"])
                            }
                            else{
                                setModalVisible(true)
                                setModalContent("you do not have permission to access this dataset")
                            }
                        }).catch(err => {
                            setModalVisible(true)
                            setModalContent("you do not have permission to access this dataset")
                        })

                     

                    }
                }
            ></DHButton>
            <div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '5vh'}}>
                <a href={link}>{link}</a>        
            </div>
            </View>
    );
}

function DatasetPage({ route }) {

    const paramsFromPreviousPage = route.params;

    return (
        <PageElements
            data={paramsFromPreviousPage.data}
            token={paramsFromPreviousPage.token}
            searchContent={paramsFromPreviousPage.searchContent}
        />
    );
}

export default DatasetPage;