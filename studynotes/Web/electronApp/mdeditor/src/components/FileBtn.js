import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import PropTypes from 'prop-types'

const FileBtn = ({text,icon,colorClass,onClick})=>{
  return (
    <button type='button' 
      className={`btn btn-block no-border ${colorClass}`}
      onClick = {onClick}  
    >
      <FontAwesomeIcon icon={icon} />
      {text}
    </button>      
  )
}


FileBtn.propTypes = {
  text:PropTypes.string,
  icon:PropTypes.object,
  colorClass:PropTypes.string,
  onClick:PropTypes.func

}
export default FileBtn