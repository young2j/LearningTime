import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTimes } from '@fortawesome/free-solid-svg-icons'

import './tablist.css'

const TabList = ({files,activeId,unsavedIds,onTabClick,onCloseTab})=>{
  return (
    <ul className="nav nav-pills tablist">
      {
        files.map(file=>{
          const withUnsavedMark = unsavedIds.includes(file.id)
          const tabClassName = classNames({
            'nav-link':true,
            'active':file.id===activeId,
            'withUnsaved':withUnsavedMark,
          })
          return(
            <li className='nav-item' key={file.id}>
            {/*eslint-disable-next-line jsx-a11y/anchor-is-valid*/}
            <a href="#" 
              className={tabClassName}
              onClick={e=>{e.preventDefault();onTabClick(file.id)}}
              >
              {file.title}
              <span className='ml-2 close-icon'
                onClick={(e)=>{e.stopPropagation();onCloseTab(file.id)}}
              >
                <FontAwesomeIcon icon={faTimes}/>
              </span>
              {
                withUnsavedMark && <span className='rounded-circle ml-2 unsaved-icon'></span>
              }
            </a>
          </li>
        )
      })
      }
    </ul>
  )
}

TabList.propTypes = {
  files:PropTypes.arrayOf(PropTypes.object),
  activeId:PropTypes.oneOfType([PropTypes.string,PropTypes.number]),
  unsavedIds:PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.string,PropTypes.number])),
  onTabClick:PropTypes.func,
  onCloseTab:PropTypes.func
}

export default  TabList