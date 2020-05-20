import {
    ArticleList,
    ArticleEdit,
    DashBoard,
    Login,
    NotFound,
    Settings
} from '../views'

export const mainRouter = [{
    pathname:'/login',
    component:Login
    },{
    pathname:'/404',
    component:NotFound
}]

export const adminRouter=[{
    pathname:'/admin/dashboard',
    component:DashBoard
},{
    pathname:'/admin/article',
    component:ArticleList,
    exact:true
},{
    pathname:'/admin/article/edit/:id',
    component:ArticleEdit
},{
    pathname:'/admin/settings',
    component:Settings
}
]
