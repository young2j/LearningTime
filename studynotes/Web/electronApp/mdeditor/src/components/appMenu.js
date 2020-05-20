const {app,shell,remote,ipcMain} = require('electron')

const menuTemplate = [
  {
    label:'文件',
    submenu:[
      {
        label:'新建',
        accelerator:'CmdOrCtrl+N',
        click:(item,browerWindow,event)=>{
          browerWindow.webContents.send('create-file')
        }
      },
      {
        label:'保存',
        accelerator:'CmdOrCtrl+S',
        click:(item,browerWindow,event)=>{
          browerWindow.webContents.send('save-file')
        }
      },
      {
        label:'导入',
        accelerator:'CmdOrCtrl+I',
        click:(item,browerWindow,event)=>{
          browerWindow.webContents.send('import-file')
        }
      },
      {
        label:'搜索',
        accelerator:'CmdOrCtrl+F',
        click:(item,browerWindow,event)=>{
          browerWindow.webContents.send('search-file')
        }
      },
    ]
  },
  {
    label: '编辑',
    submenu: [
      {
        label: '撤销',
        accelerator: 'CmdOrCtrl+Z',
        role: 'undo'
      },
      {
        label: '恢复',
        accelerator: 'Shift+CmdOrCtrl+Z',
        role: 'redo'
      },
      {
        type: 'separator'
      },
      {
        label: '剪切',
        accelerator: 'CmdOrCtrl+X',
        role: 'cut'
      },
      {
        label: '复制',
        accelerator: 'CmdOrCtrl+C',
        role: 'copy'
      },
      {
        label: '粘贴',
        accelerator: 'CmdOrCtrl+V',
        role: 'paste'
      },
      {
        label: '全选',
        accelerator: 'CmdOrCtrl+A',
        role: 'selectall'
      },
    ]
  },
  {
    label: '视图',
    submenu: [
      {
        label: '刷新',
        accelerator: 'CmdOrCtrl+R',
        click: (item, focusedWindow)=>{
          if (focusedWindow)
            focusedWindow.reload();
        }
      },
      {
        label: '全屏',
        accelerator: (() =>{
          if (process.platform === 'darwin')
            return 'Ctrl+Command+F';
          else
            return 'F11';
        })(),
        click: (item, focusedWindow)=> {
          if (focusedWindow)
            focusedWindow.setFullScreen(!focusedWindow.isFullScreen());
        }
      },
      {
        label: '开发者工具',
        accelerator: (()=>{
          if (process.platform === 'darwin')
            return 'Alt+Command+I';
          else
            return 'Ctrl+Shift+I';
        })(),
        click: (item, focusedWindow)=>{
          if (focusedWindow)
            focusedWindow.toggleDevTools();
        }
      },
    ]
  },
  {
    label: '窗口',
    role: 'window',
    submenu: [
      {
        label: '最小化',
        accelerator: 'CmdOrCtrl+M',
        role: 'minimize'
      },
      {
        label: '关闭',
        accelerator: 'CmdOrCtrl+W',
        role: 'close'
      },
    ]
  },
  {
    label: '帮助',
    role: 'help',
    submenu: [
      {
        label:'设置',
        click:()=>{
          ipcMain.emit('open-settings-window')
        }
      },
      {
        label: '了解更多',
        click: ()=>{ shell.openExternal('http://electron.atom.io') }
      },
    ]
  },
];

if (process.platform === 'darwin') {
  var name = remote.app.getName();
  menuTemplate.unshift({
    label: name,
    submenu: [
      {
        label: '关于 ' + name,
        role: 'about'
      },
      {
        type: 'separator'
      },
      {
        label: '服务',
        role: 'services',
        submenu: []
      },
      {
        type: 'separator'
      },
      {
        label: '隐藏 ' + name,
        accelerator: 'Command+H',
        role: 'hide'
      },
      {
        label: '隐藏其他',
        accelerator: 'Command+Alt+H',
        role: 'hideothers'
      },
      {
        label: '显示所有',
        role: 'unhide'
      },
      {
        type: 'separator'
      },
      {
        label: '退出',
        accelerator: 'Command+Q',
        click: ()=>{ app.quit(); }
      },
    ]
  });
  // Window menu.
  menuTemplate[3].submenu.push(
    {
      type: 'separator'
    },
    {
      label: 'Bring All to Front',
      role: 'front'
    }
  );
}

module.exports = menuTemplate


