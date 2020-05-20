import React, { useState,useEffect,useRef } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch,faTimes } from '@fortawesome/free-solid-svg-icons'
import PropTypes from 'prop-types'

import useKeyPress from '../hooks/useKeyPress'
import useIpcRenderer from '../hooks/useIpcRenderer'


const FileSearch = ({title,onFileSearch})=>{
  const [inputActive, setInputActive] = useState(false)
  const [value, setValue] = useState('')
  const inputRef = useRef()

  const enterPressed = useKeyPress(13)
  const escPressed = useKeyPress(27)


  const closeSearch = e=>{
    // e.preventDefault()
    setInputActive(false)
    setValue('')
    onFileSearch(null)
  }

  useEffect(() => {
    if(enterPressed && inputActive){
      onFileSearch(value)
    }
    if(escPressed && inputActive){
      closeSearch()
    }

    // const handleInputEvent = e =>{
    //   const {keyCode} = e
    //   if(keyCode===13 && inputActive){
    //     onFileSearch(value)
    //   }
    //   else if (keyCode===27 && inputActive){
    //     closeSearch(e)
    //   }
    // }
    // document.addEventListener('keyup',handleInputEvent)
    // return ()=>{
    //   document.removeEventListener('keyup',handleInputEvent)
    // }

  })

  useEffect(()=>{
    if(inputActive){
      inputRef.current.focus()
    }
  },[inputActive])

  useIpcRenderer({
    'search-file':()=>setInputActive(true)
  })
  
  return (
    <div className='alert alert-primary no-gutters mb-0'>
      { !inputActive && 
        <div className='d-flex justify-content-between align-items-center'>
          <span>{title}</span>
          <button
            type='button'
            className='icon-btn'
            onClick={()=>{setInputActive(true)}}
          >
          <FontAwesomeIcon icon={faSearch} size='lg'/>
          </button>
        </div>
      }
      {
        inputActive && 
        <div className='d-flex justify-content-between align-items-center'>
          <input className='form-control form-control-sm'
            value={value}
            onChange={e=>setValue(e.target.value)}
            ref = {inputRef}
          />
          <button
            type='button'
            className='icon-btn'
            onClick={e=>closeSearch(e)}
          >
            <FontAwesomeIcon icon={faTimes} size='lg'/>
          </button>
        </div>
      }
    </div>
  )
}

FileSearch.propTypes = {
  title:PropTypes.string,
  onFileSearch:PropTypes.func.isRequired
}

FileSearch.defaultProps = {
  title:'我的云文档'
}


export default FileSearch