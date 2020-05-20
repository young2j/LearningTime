const {BrowserWindow} = require('electron')

class AppWindow extends BrowserWindow{
  constructor(customConfig,url){
    const basicConfig = {
      width:800,
      height:600,
      webPreferences:{
        nodeIntegration:true
      },
      show:false,
      backgroundColor:"#efefef"
    }
    const config = {...basicConfig,...customConfig}
    super(config)
    this.loadURL(url)
    this.once('ready-to-show',()=>{
      this.show()
    })
  }
}

module.exports = AppWindow