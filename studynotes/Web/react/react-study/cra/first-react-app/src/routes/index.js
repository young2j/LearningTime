import {
    ArticleList,
    ArticleEdit,
    DashBoard,
    Login,
    NotFound,
    Settings,
    Notifications,
    NoAccess
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
    component:DashBoard,
    title:'仪表盘',
    isNav:true,
    iconType:'dot-chart',
    roles: ['001', '003']
},{
    pathname:'/admin/article',
    component:ArticleList,
    exact:true,
    title:'文章管理',
    isNav:true,
    iconType:"unordered-list",
    roles:['001','002','003']
},{
    pathname:'/admin/article/edit/:id',
    component:ArticleEdit,
    title:'文章编辑',
    isNav:false,
    roles:['001','002']
},{
    pathname:'/admin/settings',
    component:Settings,
    title:'设置',
    isNav:true,
    iconType:'setting',
    roles:['001']
},{
    pathname:'/admin/notifications',
    component:Notifications,
    title:'通知中心',
    isNav:false,
    iconType:'notification',
    roles:['002','003']
}, {
    pathname: '/admin/noaccess',
    component: NoAccess,
    title: '无权限',
    isNav: false,
    iconType: '',
    roles: ['001', '002', '003','004']
},
]
