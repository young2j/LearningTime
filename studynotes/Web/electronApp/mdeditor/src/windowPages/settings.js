const {remote} = window.require('electron')
const Store = window.require('electron-store')

const settingsStore = new Store({name:'settings'})


const $ = id=>{
  return document.getElementById(id)
}

document.addEventListener('DOMContentLoaded',()=>{
  let savedLocation = settingsStore.get('savedLocation')
  if(savedLocation){
    $('savedLocation').value = savedLocation
  }
  $('selectLocation').addEventListener('click', e =>{
    e.preventDefault()
    remote.dialog.showOpenDialog({
      title:'选择保存路径',
      properties:['openDirectory']
    }).then(res=>{
        const filePaths = res.filePaths
        $('savedLocation').value = filePaths[0]
        savedLocation = filePaths[0]
      }
    )
  })

  $('settings-form').addEventListener('submit',()=>{
    settingsStore.set('savedLocation',savedLocation)
    remote.getCurrentWindow().close()
  })
})