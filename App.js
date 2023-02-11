import React, {useState, useEffect} from 'react';
import {
    StyleSheet,
    Button,
    View,
    SafeAreaView,
    Text,
    Alert,
    Dimensions,
    Pressable,
} from 'react-native';
import {Icon} from '@rneui/themed';
import {Camera, CameraType} from 'expo-camera';

export default function App() {
    const [hasPermission, setHasPermission] = useState(null);
    const [type, setType] = useState(CameraType.front);
    const winWidth = Dimensions.get('window').width;
    const winHeight = Dimensions.get('window').height;
    const styles = StyleSheet.create({
        container: {
            flex: 1,
            justifyContent: 'center',
            marginHorizontal: 0,
            padding: 2,
            backgroundColor: "black",
        },
        cam_button: {
            borderRadius: 20,
            position: 'absolute',
            bottom: 50,
            width: winWidth * 0.5,
            height: winHeight * 0.05,
            alignSelf: 'center',
            justifyContent: 'center',
            backgroundColor: 'orange',
        },
        house_button: {
            borderRadius: 30,
            margin: 15,
            width: winWidth * 0.15,
            height: winWidth * 0.15,
            alignSelf: 'flex-end',
            justifyContent: 'center',
            backgroundColor: 'white',
        },
    });

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
        return <Text>No access to camera</Text>;
    }
    return (
        <SafeAreaView style={styles.container}>
            <View style={{flex: 1}}>
                <Camera style={{flex: 1}} type={type}>
                    <View style={styles.cam_button}>
                        <Button title={"CHANGE CAMERA"} color={'black'}
                                onPress={toggleCameraType}>
                        </Button>
                    </View>
                    <View style={styles.house_button}>
                        <Icon
                            name='house' color='orange' size='40'
                            onPress={() => Alert.alert('Alert Title', 'My Alert Msg')}/>
                    </View>
                </Camera>
            </View>
        </SafeAreaView>
)
    ;
}