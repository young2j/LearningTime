import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'
import { faPlus,faFileImport,faSave } from '@fortawesome/free-solid-svg-icons'
import SimpleMDE from "react-simplemde-editor";
import "easymde/dist/easymde.min.css";
import uuid4 from 'uuid/v4'

import './App.css'
import FileSearch from './components/FileSearch'
import FileList from './components/FileList'
import FileBtn from './components/FileBtn'
import TabList from './components/TabList'

import {flattenFilesArr, fileHelper} from './utils'
import useIpcRenderer from './hooks/useIpcRenderer';


const path = window.require('path')
const {remote} = window.require('electron')
const Store = window.require('electron-store')
const fileStore = new Store({name:'Files Store'})
const settingsStore = new Store({name:'settings'})

// fileStore.delete('files')

const saveFilesToStore = files=>{
  const newFiles = Object.values(files).reduce((result,file)=>{
    const {id,path,title,createAt,isNew} = file
    result[id] = {
      id,
      path,
      title,
      createAt,
      isNew
    }
    return result
  },{})
  fileStore.set('files',newFiles)
}

const App = ()=> {
  const [files,setFiles] = useState(fileStore.get('files') ||{})
  const [activeFileID,setActiveFileID] = useState(null)
  const [openedFileIDs,setOpenedFileIDs ] = useState([])
  const [unsavedFileIDs,setUnsavedFileIDs] = useState([])
  const [searchedFiles,setSearchedFiles] = useState({})
  const [isSearching,setIsSearching] = useState(false)

  const openedFiles = openedFileIDs.map(openID=>{
    return files[openID]
  })

  const activeFile = files[activeFileID]

  const savedLocation = settingsStore.get('savedLocation') || remote.app.getPath('documents')
  

  const fileClick = (id)=>{
    setActiveFileID(id)
    if(!files[id].isNew){
      fileHelper.readFile(
        files[id].path
        ).then(body=>{
          setFiles(
            {
              ...files,
              [id]:{...files[id],body}
            }
            )
          }
        )
    }
    if(!openedFileIDs.includes(id)){
      setOpenedFileIDs([...openedFileIDs,id])
    }
  }

  const tabClose = (id)=>{
    if(files[id].isNew){
      const saveConfirm = window.confirm('是否保存？')
      if(saveConfirm){
        remote.dialog.showSaveDialog({
          title:'保存至',
          defaultPath:files[id].path
        }).then(res=>{          
          fileHelper.writeFile(res.filePath,files[id].body)
          .then(
            ()=>{
              const {name} = path.parse(res.filePath)
              setFiles({
                ...files,
                [id]:{...files[id],title:name,isNew:false}
              })
            }
          ).finally(()=>{
            const openedIDs = openedFileIDs.filter(openID=>openID!==id)
            setOpenedFileIDs(openedIDs)
            if (openedIDs.length>0){
              setActiveFileID(openedIDs[0])
            }else{
              setActiveFileID(null)
            }
          }
          )
        })
      }else{
        const openedIDs = openedFileIDs.filter(openID=>openID!==id)
        setOpenedFileIDs(openedIDs)
        if (openedIDs.length>0){
          setActiveFileID(openedIDs[0])
        }else{
          setActiveFileID(null)
        }
      }      
    }else{
      const openedIDs = openedFileIDs.filter(openID=>openID!==id)
      setOpenedFileIDs(openedIDs)
      if (openedIDs.length>0){
        setActiveFileID(openedIDs[0])
      }else{
        setActiveFileID(null)
      }
    }
  }

  const contentChange = (activeID,value)=>{
    const newFile = {...files[activeID],body:value}
    setFiles({
      ...files,
      [activeID]:newFile
    })

    if(!unsavedFileIDs.includes(activeID)){
      setUnsavedFileIDs([...unsavedFileIDs,activeID])
    }
  }

  const fileDelete = id=>{
    if(!files[id].isNew){
      fileHelper.deleteFile(
        files[id].path
        )
    }
    const {[id]:file,...afterDeleteFiles} = files
    setFiles(afterDeleteFiles)
    saveFilesToStore(afterDeleteFiles)
    const {[id]:_file,...afterDeleteSearchedFiles} = searchedFiles
    setSearchedFiles(afterDeleteSearchedFiles)
    tabClose(id)
  }

  const changeFileName = (id,title)=>{
    const oldFilePath = files[id].path
    const newFilePath = path.join(savedLocation,`${title}.md`)
    const newFile = {
      ...files[id],
      title,
      path:newFilePath,
    }

    const newFiles = {
      ...files,
      [id]:newFile
    }
    saveFilesToStore(newFiles)
    setFiles(newFiles)
    if(!newFile.isNew){
      fileHelper.renameFile(
        oldFilePath,
        newFilePath
        )
    }
  }

  const saveFileContent = ()=>{
    if(!activeFileID){
      return
    }
    if(files[activeFileID].isNew){
        remote.dialog.showSaveDialog({
          title:'保存至',
          defaultPath:files[activeFileID].path
        }).then(res=>{
          fileHelper.writeFile(
            res.filePath,
            files[activeFileID].body
            ).then(
              ()=>{
                const {name} = path.parse(res.filePath)
                const newFiles = {
                  ...files,
                  [activeFileID]:{...files[activeFileID],title:name,path:res.filePath,isNew:false}
                }
                setFiles(newFiles)
                setUnsavedFileIDs(unsavedFileIDs.filter(id=>id!==activeFileID))
                saveFilesToStore(newFiles)
              }
            ) 
        })
      }else{
        fileHelper.writeFile(
          files[activeFileID].path,
          files[activeFileID].body
          ).then(
            ()=>{
              setFiles(files)
              saveFilesToStore(files)
            }
          )
      }
    setUnsavedFileIDs(unsavedFileIDs.filter(unsavedID=>unsavedID!==activeFileID))
  }

  const fileSearch = (value)=>{
    if(value){
      setIsSearching(true)
      const searchFiles = flattenFilesArr(Object.values(files).filter(file=>file.title.indexOf(value)!==-1))
      setSearchedFiles(searchFiles)
    }else{
      setIsSearching(false)
    }
  }

  const fileAdd = ()=>{
    const newID = uuid4()
    
    const newFilePath = path.join(savedLocation,'untitled.md')

    const newFile = {
      id:newID,
      title: 'untitled',
      body:'',
      path:newFilePath,
      isNew:true
    }
    const newFiles = {
      ...files,
      [newID]:newFile
    }

    setActiveFileID(newID)
    setOpenedFileIDs([...openedFileIDs,newID])
    setFiles(newFiles)
    saveFilesToStore(newFiles)
  }

  const fileImport = ()=>{
    remote.dialog.showOpenDialog({
      title:'选择Markdown文档',
      defaultPath:savedLocation,
      filters:[{
        name:'markdown',extensions:['md']
      }],
      properties:['openFile','multiSelections']
    }).then(res=>{
        const filePaths = res.filePaths.filter(fp=>{
          const existFiles = Object.values(files).find(f=>f.path===fp)
          return !existFiles
        })
        const importFiles = filePaths.map(fp=>{
          return {
              id:uuid4(),
              title: path.basename(fp,path.extname(fp)),
              path:fp,
              isNew:false
            }
          })
        setFiles({
          ...files,
          ...flattenFilesArr(importFiles)
        })
        saveFilesToStore({
          ...files,
          ...flattenFilesArr(importFiles)
        })  
      })
    }

  useIpcRenderer({
    'create-file':fileAdd,
    'import-file':fileImport,
    'save-file':saveFileContent,
  })

  return (
    <div className='App container-fluid px-0'>
      <div className="row no-gutters ">
        <div className="col-3 bg-light left-panel">
          <FileSearch title='我的云文档' onFileSearch={value=>fileSearch(value)} />
          <FileList files={isSearching? searchedFiles:files} 
            onFileClick={id=>fileClick(id)}
            onFileDelete={id=>fileDelete(id)}
            onSaveEdit={(id,title)=>changeFileName(id,title)}
          />
          <div className='row d-flex no-gutters file-btn'> 
           <div className='col'>
            <FileBtn text='新建' icon={faPlus} colorClass="btn-primary" onClick={()=>fileAdd()}/>
           </div>
           <div className='col'>  
            <FileBtn text='导入' icon={faFileImport} colorClass='btn-success' onClick={()=>fileImport()}/>
           </div>
           {/* <div className='col'>  
            <FileBtn text='保存' icon={faSave} colorClass='btn-success' onClick={()=>saveFileContent()}/>
           </div> */}
          </div>
        </div>
        <div className="col-9 right-panel">
          {
            activeFile? (
            <>
            <TabList files={openedFiles} 
              onTabClick={(id)=>setActiveFileID(id)}
              activeId={activeFileID}
              onCloseTab={id=>tabClose(id)}
              unsavedIds={unsavedFileIDs}
              />
            <SimpleMDE
              key={activeFile && activeFile.id}
              value={activeFile && activeFile.body}
              onChange={(value)=>contentChange(activeFileID,value)}
              options={{
                minHeight:'70vh',
              }}
            />
            </>):(
              <div className='start-page'>
                打开或者新建文档
              </div>
            )
        }
        </div>
      </div>
    </div>
  )
}

export default App;
