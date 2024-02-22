import React from 'react';

import { Text, TouchableOpacity, View } from "react-native"
import styles from './style-sheet'


const DHButton = (props) => {
    return (
        <TouchableOpacity
            style={[styles.touchableOpacityStyle, props.style]}
            onPress={props.onPress}
        >
            <Text
                style={{
                    color: '#fff',
                    textAlign: "center"
                }}

            >
                {props.title}
            </Text>

        </TouchableOpacity>
    );
}

export default DHButton;