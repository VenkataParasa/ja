import './polyfills';
import { AppRegistry } from 'react-native';
import App from './App';

const appName = 'JA BizTown Web';

AppRegistry.registerComponent(appName, () => App);

// For web, we need to render to the DOM
if (typeof document !== 'undefined') {
    const { AppRegistry } = require('react-native-web');
    AppRegistry.runApplication(appName, {
        rootTag: document.getElementById('root'),
    });
}
