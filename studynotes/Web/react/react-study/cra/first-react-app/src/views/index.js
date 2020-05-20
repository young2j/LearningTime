// import ArticleList from './Article'
// import ArticleEdit from './Article/Edit'
// import DashBoard from './DashBoard'
// import Login from './Login'
// import NotFound from './NotFound'
// import Settings from './Settings'



import Loadable from 'react-loadable'
import { Loading } from '../components'

const ArticleList=Loadable({
    loader:()=>import('./Article'),
    loading:Loading
})

const ArticleEdit=Loadable({
    loader:()=>import('./Article/Edit'),
    loading:Loading
})

const DashBoard=Loadable({
    loader:()=>import('./DashBoard'),
    loading:Loading
})

const Login=Loadable({
    loader:()=>import('./Login'),
    loading:Loading
})

const NotFound=Loadable({
    loader:()=>import('./NotFound'),
    loading:Loading
})

const Settings=Loadable({
    loader:()=>import('./Settings'),
    loading:Loading
})

const Notifications=Loadable({
    loader:()=>import('./Notifications'),
    loading:Loading
})
const NoAccess=Loadable({
    loader:()=>import('./NoAccess'),
    loading:Loading
})

export {
        ArticleList,
        ArticleEdit,
        DashBoard,
        Login,
        NotFound,
        Settings,
        Notifications,
        NoAccess
    }