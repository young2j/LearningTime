const { app, BrowserWindow, Menu, ipcMain,dialog } = require('electron')
const isDev = require('electron-is-dev')
const path = require('path')

const {autoUpdater} = require('electron-updater')

const menuTemplate = require('./src/components/appMenu')
const AppWindow = require('./src/components/appWindow')

app.on('ready', () => {
    require('devtron').install()

    autoUpdater.autoDownload = false
    autoUpdater.checkForUpdatesAndNotify()

    autoUpdater.on('error',err=>{
        dialog.showErrorBox('Error:',err===null? "unknows":err)
    })

    autoUpdater.on("update-available",()=>{
        dialog.showMessageBox({
            type:"info",
            title:"有新的版本",
            message:"发现新的版本，立即更新？",
            buttons:['是','否']
        },btnIndex=>{
            if(btnIndex===0){
                autoUpdater.downloadUpdate()
            }
        })
    })

    autoUpdater.on('update-not-available',()=>{
        dialog.showMessageBox({
            title:'没有新版本',
            message:"当前已经是最新版本"
        })
    })
    const mainWindowConfig = {
        width: 1080,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    }
    const mainURL = isDev ? 'http://localhost:3000' : path.join(__dirname,'./build/index.html')
    let mainWindow = new AppWindow(mainWindowConfig, mainURL)
    //
    mainWindow.webContents.openDevTools()
    //
    mainWindow.on('close', () => {
        mainWindow = null
    })
    //
    ipcMain.on('open-settings-window', () => {
        const settingsWindowConfig = {
            width: 500,
            height: 400,
            parent: mainWindow, //没效果？？
            // title:'设置',
        }
        const settingsURL = `file://${path.join(__dirname, './src/windowPages/settings.html')}`
        let settingsWindow = new AppWindow(settingsWindowConfig, settingsURL)
        settingsWindow.on('close', () => {
            settingsWindow = null
        })
        settingsWindow.setMenu(null)
    })
    //设置菜单
    const appMenu = Menu.buildFromTemplate(menuTemplate)
    // Menu.setApplicationMenu(appMenu) //会为所有窗口设置菜单
    mainWindow.setMenu(appMenu)
})

/*
ipcMain.emit('event') <=> ipcMain.on('event',callback)
BrowserWindow.webContents/ipcRenderer.send('event')<=>ipcRenderer.on('event',callback)
*/

// Quit when all windows are closed.
app.on('window-all-closed', function () {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') app.quit()
  })
  
app.on('activate', function () {
// On macOS it's common to re-create a window in the app when the
// dock icon is clicked and there are no other windows open.
if (BrowserWindow.getAllWindows().length === 0) createWindow()
})
  
// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.