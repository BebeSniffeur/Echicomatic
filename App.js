import React, {useState, useEffect} from 'react';
import {
    StyleSheet,
    Button,
    View,
    SafeAreaView,
    Alert,
    Dimensions,
    Pressable,
} from 'react-native';
import { Center, Icon, IconButton } from 'native-base';
import {NativeRouter, Route, Link} from "react-router-native";
import {Camera, CameraType} from 'expo-camera';
import Ionicons from 'react-native-vector-icons/Ionicons';
import { NativeBaseProvider } from "native-base";

const winWidth = Dimensions.get('window').width,
    winHeight = Dimensions.get('window').height;

function ViewCamera() {
    const [hasPermission, setHasPermission] = useState(null);
    const [type, setType] = useState(CameraType.front);

    function toggleCameraType() {
        setType(current => (current === CameraType.back ? CameraType.front : CameraType.back));
    }

    useEffect(() => {
        (async () => {
            const {status} = await Camera.requestCameraPermissionsAsync();
            setHasPermission(status === 'granted');
        })();
    }, []);

    if (hasPermission === null) {
        return <View/>;
    }
    if (hasPermission === false) {
        return <></>;
    }

    return (
        <Camera style={{flex: 1}} type={type}>
                <Center style={{marginTop: 20, borderRadius: 20}} mx={90}>
                    <IconButton onPress={() => Alert.alert('Bonjour!', 'SALUT')} icon={<Icon as={Ionicons} name="home" />} borderRadius="full" _icon={{
      color: "orange.500",
      size: "xl"
    }} _hover={{
      bg: "orange.600:alpha.20"
    }} _pressed={{
      bg: "orange.600:alpha.20",
      _ios: {
        _icon: {
          size: "2xl"
        }
      }
    }} _ios={{
      _icon: {
        size: "2xl"
      }
    }} />
                </Center>
            <View style={styles.cam_button}>
                <Button title="CHANGE CAMERA" color="black"
                        onPress={toggleCameraType}>
                </Button>
            </View>
        </Camera>
    )
}

export default function App() {
    return (
        <NativeBaseProvider>
        <SafeAreaView style={styles.container}>
            <View style={{flex: 1}}>
                <ViewCamera>
                </ViewCamera>
            </View>
        </SafeAreaView>
        </NativeBaseProvider>
    );
}


const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        marginHorizontal: 0,
        padding: 2,
        backgroundColor: "black",
    },
    cam_button: {
        borderRadius: 20,
        position: "absolute",
        bottom: 50,
        width: winWidth * 0.5,
        height: winHeight * 0.05,
        alignSelf: "center",
        justifyContent: "center",
        backgroundColor: "orange",
    },
    house_button: {
        borderRadius: 30,
        margin: 40,
        width: winWidth * 0.15,
        height: winWidth * 0.15,
        alignSelf: "flex-end",
        justifyContent: "center",
        backgroundColor: "white",
    },
});