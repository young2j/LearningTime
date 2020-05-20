import { Home,Product,User,Role } from '../pages'


export const Routes = {
    HomeRoute: {
        path: "/admin/home",
        component: Home
    },
    UserRoute:{
        path: "/admin/user",
        component: User
    },
    RoleRoute:{
        path: '/admin/role',
        component: Role
    }
}



export const ProductRoute = [{
    path:'/admin/product',
    component:Product
},{
    path: '/admin/product/category',
    component: Product
},{
    path: '/admin/product/goods',
    component: Product
}]