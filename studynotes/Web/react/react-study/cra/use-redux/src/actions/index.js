import actionTypes from './actionTypes'

export const add = (id) => {
    
    return {
        type:actionTypes.ITEM_AMOUNT_ADD,
        payload:{
            id
        }
    }
}

export const sub = (id) => {
    return {
        type:actionTypes.ITEM_AMOUNT_SUB,
        payload:{
            id
        }
    }
}