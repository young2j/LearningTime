export default {
  saveUser(user){
      return window.localStorage.setItem('user', JSON.stringify(user))
  },

  getUser(){
      return JSON.parse(window.localStorage.getItem('user'))
  },

  removeUser(){
      return window.localStorage.removeItem('user')
  }
}