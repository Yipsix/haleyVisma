import React from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { ExpoLinksView } from '@expo/samples';
import Griddle from 'griddle-react';


const data = [
  { one: 'one', two: 'two', three: 'three' },
  { one: 'uno', two: 'dos', three: 'tres' },
  { one: 'ichi', two: 'ni', three: 'san' }
];



export default class LinksScreen extends React.Component {

  
  

  static navigationOptions = {
    title: 'user base', 
  };


  
  render() {
    return (
      <View>>
          <Griddle data={data} />
          </View>
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 15,
    backgroundColor: '#fff',
  },
});
