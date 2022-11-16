import Vue from 'vue';
import Router from 'vue-router';
import Addresss from '../components/Address.vue';
import Ping from '../components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Address',
      component: Addresss,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
