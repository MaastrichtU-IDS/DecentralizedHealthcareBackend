import { StyleSheet } from "react-native";

const styles = StyleSheet.create(
    {
        container: {
            flex: 1,
            backgroundColor: '#fff',
            // alignItems: 'center', // align children along the cross axis.
            // justifyContent: 'center', // align children within the main axis
        },

        textInput: {
            padding: 10,
            margin: 12,
            height: 40,
            borderWidth: 1,
            borderRadius: 150,
        },

        touchableOpacityStyle: {
            padding: 10,
            margin: 12,
            backgroundColor: '#1E6738',
            borderRadius: 10,
        },
    }
);

export default styles;