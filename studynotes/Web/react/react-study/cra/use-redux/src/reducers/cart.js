import actionTypes from '../actions/actionTypes'

const initState = [
    {
        id:1,
        name:'Apple',
        amount:10,
        price:10000,
        buy:0
    },
    {
        id:2,
        name:'OnePlus',
        amount:10,
        price:5000,
        buy:0
    },
    {
        id:3,
        name:'HuaWei',
        amount:10,
        price:8000,
        buy:0
    },
]


export default (state = initState, action) => {
    
    switch (action.type) {
        case actionTypes.ITEM_AMOUNT_ADD:
            return state.map(item =>{
                if (item.id===action.payload.id){
                    item.amount-=1
                    item.buy+=1
                }
                return item
            })
        case actionTypes.ITEM_AMOUNT_SUB:
            return state.map(item=>{
                if (item.id===action.payload.id){
                    item.amount+=1
                    item.buy-=1
                }
                return item
            })
        default:
            return state
    }
}