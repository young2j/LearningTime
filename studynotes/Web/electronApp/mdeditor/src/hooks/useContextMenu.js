import { useEffect,useRef } from 'react'
const {remote} = window.require('electron')
const {Menu,MenuItem} = remote

const useContextMenu = (menuItems,deps)=>{
  let fileRef = useRef()
  useEffect(()=>{
    const contextMemu = new Menu()
    menuItems.forEach(item=>{
      contextMemu.append(new MenuItem(item))
    })
    const handleContextmenu = e=>{
      e.preventDefault()
      const fileNode = document.querySelector('.file-list')
      if(fileNode.contains(e.target)){
        fileRef.current = e.target
        contextMemu.popup(remote.getCurrentWindow())
      }
    }
    window.addEventListener('contextmenu',handleContextmenu)
    return ()=>{
      window.removeEventListener('contextmenu',handleContextmenu)
    }
  },deps)
  return fileRef
}

export default useContextMenu

