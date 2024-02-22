import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import LoginPage from './src/pages/login';
import RegisterPage from './src/pages/register';
import RolePage from './src/pages/role';
import ProviderPage from './src/pages/provider';
import RequesterPage from './src/pages/requester';
import DatasetPage from './src/pages/dataset';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Login" component={LoginPage} />
        <Stack.Screen name="Request dataset" component={RequesterPage} />
        <Stack.Screen name="Provide dataset" component={ProviderPage} />
        <Stack.Screen name="Dataset" component={DatasetPage} />
        <Stack.Screen name="Register" component={RegisterPage} />
        <Stack.Screen name="What do you want to do?" component={RolePage} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
