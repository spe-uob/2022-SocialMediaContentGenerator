import {boot} from 'quasar/wrappers'
import config from './debug_type.json'
// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async ({app}) => {
  app.config.globalProperties.$DEBUG = config.DEBUG;
  app.config.globalProperties.$BASEURL = config.DEBUG ? "http://127.0.0.1:8888" : "";
})
