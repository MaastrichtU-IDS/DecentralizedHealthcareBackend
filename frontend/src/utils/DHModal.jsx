import React from "react";

import {
    Modal,
    Pressable,
    Text,
    View,
} from 'react-native';


export default function DHModal(props) {
    return (
        <Modal
            animationType="fade"
            transparent={true}
            visible={props.modalVisible}
            onRequestClose={() => {
                props.setModalVisible(!props.modalVisible);
            }}
        >
            <View style={{
                flex: 1,
                justifyContent: "center",
            }}>
                <View style={{
                    margin: 20,
                    backgroundColor: "white",
                    borderRadius: 20,
                    padding: 35,
                    alignItems: "center",
                    shadowColor: "#000",
                    shadowOffset: {
                        width: 0,
                        height: 2
                    },
                    shadowOpacity: 0.25,
                    shadowRadius: 4,
                    elevation: 5,
                }}>
                    <Text style={{
                        marginBottom: 15,
                        textAlign: "center"
                    }}>
                        {props.message}
                    </Text>

                    <Pressable style={{
                        borderRadius: 20,
                        padding: 10,
                        elevation: 2,
                        backgroundColor: "#2196F3"
                    }}
                        onPress={
                            () => props.setModalVisible(!props.modalVisible)
                        }
                    >
                        <Text style={{
                            fontWeight: "bold",
                            textAlign: "center"
                        }}>
                            OK
                        </Text>
                    </Pressable>
                </View>
            </View>
        </Modal>
    )
}