import React, {useState,useEffect,useRef } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMarkdown } from '@fortawesome/free-brands-svg-icons'
import { 
  // faEdit,faTrash,
  faTimes,faCheck } from '@fortawesome/free-solid-svg-icons'
import PropTypes from 'prop-types'
import useKeyPress from '../hooks/useKeyPress'
import useContextMenu from '../hooks/useContextMenu'
import {getParentNode} from '../utils'



const FileList = ({files,onFileClick,onSaveEdit,onFileDelete})=>{
  const [editStatus, setEditStatus] = useState()
  const [value, setValue] = useState('untitled')
  const inputRef = useRef()

  const enterPressed = useKeyPress(13)
  const escPressed = useKeyPress(27)

  useEffect(() => {
    if(enterPressed && editStatus){
      let editFile = files[editStatus]
      onSaveEdit(editFile.id,value)
      setEditStatus(null)
    }
    if(escPressed && editStatus){
      setEditStatus(null)
    }
  },[editStatus, enterPressed, escPressed, files, onSaveEdit, value])

  useEffect(()=>{
    if(editStatus){
      inputRef.current.focus()
    }
  },[editStatus])

  const clickNode = useContextMenu([
    {
      label:"打开",
      click:()=>{
        let id = getParentNode(clickNode.current,'file-item').dataset.id
        onFileClick(id)
      }
    },
    {
      label:"重命名",
      click:()=>{
        const {id,title} = getParentNode(clickNode.current,'file-item').dataset
        setEditStatus(id);
        setValue(title);
      }
    },
    {
      label:"删除",
      click:()=>{
        let id = getParentNode(clickNode.current,'file-item').dataset.id
        onFileDelete(id)
      }
    },
  ],[files])


  return (
    <ul className="list-group list-group-flush file-list">
      {
        Object.values(files).map(file=>(
          <li
            className='list-group-item bg-light d-flex align-items-center row mx-0 file-item'
            key={file.id}
            data-id = {file.id}
            data-title={file.title}
          >
            {
              editStatus!==file.id ?
            (
            <>
              <span className='col-2'>
                <FontAwesomeIcon icon={faMarkdown} size='lg'/>
              </span>
              
              <span className='col-7 c-pointer'
              onClick={()=>onFileClick(file.id)}
              >
                {file.title}
              </span>
              
              {/* <button className='col-1 icon-btn'
              onClick={()=>{
                setEditStatus(file.id);
                setValue(file.title);
                }}
              >
                <FontAwesomeIcon icon={faEdit}/>
              </button>
              <button className='col-1 icon-btn'
              onClick={()=>onFileDelete(file.id)}
              >
                <FontAwesomeIcon icon={faTrash}/>
              </button> */}
            </>
            ):
            (
              <div className='d-flex justify-content-between align-items-center'>
              <span className='col-2'>
                <FontAwesomeIcon icon={faMarkdown} size='lg'/>
              </span>
              <input className='form-control col-6 form-control-sm '
                value={value}
                onChange={e=>setValue(e.target.value)}
                placeholder='untitled.md'
                ref = {inputRef}
              />
              <button
                type='button'
                className='icon-btn col-1'
                onClick={()=>{onSaveEdit(file.id,value);setEditStatus(null)}}
              >
                <FontAwesomeIcon icon={faCheck} />
              </button>
              <button
                type='button'
                className='icon-btn col-1'
                onClick={()=>setEditStatus(null)}
              >
                <FontAwesomeIcon icon={faTimes} />
              </button>
            </div>
            )
          }
          </li>
        ))
      }
    </ul>
  )
}

FileList.propTypes = {
  files:PropTypes.object,
  onFileClick:PropTypes.func,
  onSaveEdit:PropTypes.func,
  onFileDelete:PropTypes.func,
}

export default FileList