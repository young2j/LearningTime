import actionTypes from '../actions/actionTypes'

const initState = {
    isLoading:false,
    list:[
    {
        id:1,
        title:'一二三四五',
        description:'上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎哒哒哒哒哒哒阿哒哒哒哒哒哒哒哒哒',
        hasRead:false
    }, {
            id: 2,
            title: '一二三四五',
            description: '上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎哒哒哒哒哒哒阿哒哒哒哒哒哒哒哒哒',
            hasRead: false
        }, {
            id: 3,
            title: '一二三四五',
            description: '上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎哒哒哒哒哒哒阿哒哒哒哒哒哒哒哒哒',
            hasRead: false
        }, {
            id: 4,
            title: '一二三四五',
            description: '上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎哒哒哒哒哒哒阿哒哒哒哒哒哒哒哒哒',
            hasRead: false
        }, {
            id: 5,
            title: '一二三四五',
            description: '上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎上山打老虎哒哒哒哒哒哒阿哒哒哒哒哒哒哒哒哒',
            hasRead: true
        }
    ]
}

export default (state=initState,action)=>{
    switch(action.type){
        case actionTypes.START_MARK:
            return{
                ...state,
                isLoading:true
            }
        case actionTypes.FINISH_MARK:
            return{
                ...state,
                isLoading:false
            }

        case actionTypes.MARK_NOTIFICATION:
            const newList = state.list.map(item=>{
                if (item.id===action.payload.id){
                    item.hasRead=true
                }
                return item
            })
            return {
                ...state,
                list:newList
            }
        
        case actionTypes.MARK_ALL_NOTFICATIONS:
            const newAllList = state.list.map(item=>{
                if (!item.hasRead){
                    item.hasRead=true
                }
                return item
            })
            return {
                ...state,
                list:newAllList
            }

        case actionTypes.GET_NOTIFICATIONS_LIST:
            return {
                ...state,
                list:action.payload
            }            
        default:
            return state        
    }
}