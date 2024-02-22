import React from "react";

import {
    Text,
    TouchableOpacity,
    View
} from "react-native";
import DHButton from "../utils/dh-button";

import styles from "../utils/style-sheet";

function RolePage({ navigation }) {
    return (
        <View style={
            styles.container
        }>
            <DHButton
                title="Upload data"
                onPress={
                    () => {
                        navigation.navigate("Provide dataset")
                    }
                }
            />

            <DHButton
                title="Search data"
                onPress={
                    () => {
                        navigation.navigate("Request dataset")
                    }
                }
            />
        </View>
    );
}

export default RolePage;