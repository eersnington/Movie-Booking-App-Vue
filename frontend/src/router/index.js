import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import ShowsView from "../views/ShowsView.vue";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import AdminLoginView from "../views/AdminLoginView.vue";
import AdminDashboardView from "../views/AdminDashboardView.vue";
import SeatBookingView from "../views/SeatBookingView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/shows",
    name: "shows",
    component: ShowsView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/signup",
    name: "signup",
    component: SignupView,
  },
  {
    path: "/adminlogin",
    name: "adminlogin",
    component: AdminLoginView,
  },
  {
    path: "/admindashboard",
    name: "admindashboard",
    component: AdminDashboardView,
    meta: {requiresAuth: true,  requiresAdmin: true },
  },
  { 
    path: '/booking/:showId', 
    name: 'booking', 
    component: SeatBookingView,
    meta: { requiresAuth: true}, 
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});


router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token');
  const isAdmin = localStorage.getItem('isAdmin');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'login' }); 
    } else if (to.matched.some(record => record.meta.requiresAdmin) && isAdmin == null) {
      next({ name: 'home' }); 
    } else {
      next(); 
    }
  } else {
    next(); 
  }
});

export default router;
