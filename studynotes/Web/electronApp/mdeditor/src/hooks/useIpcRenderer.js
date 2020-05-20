import { useEffect } from "react"

const {ipcRenderer} = window.require('electron')

const useIpcRenderer = (ipcMap) =>{
  useEffect(()=>{
    Object.keys(ipcMap).forEach(key=>{
      ipcRenderer.on(key,ipcMap[key])
    })
    return ()=>{
      Object.keys(ipcMap).forEach(key=>{
        ipcRenderer.removeListener(key,ipcMap[key])
      })
    }
  })
}

export default useIpcRenderer