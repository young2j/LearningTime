const fs = window.require('fs').promises

export const defaultFiles = [
  {
    id: 1,
    title: 'document01.md',
    body: '# balabala1',
    // createAt: new Date().getTime() - 10000
  },
  {
    id: 2,
    title: 'document02.md',
    body: '# balabala2',
    // createAt: new Date().getTime() - 1000
  },
  {
    id: 3,
    title: 'document03.md',
    body: '# balabala3',
    // createAt: new Date().getTime() - 100
  },
]

export const flattenFilesArr = (files) => {
  return files.reduce((map, item) => {
    map[item.id] = item
    return map
  }, {})
}

export const filesToObjArr = obj =>{
  return Object.keys(obj).map(key=>obj[key])
}

export const fileHelper = {
  readFile:(path)=>{
    return fs.readFile(path,{encoding:'utf8'})
  },
  writeFile:(path,content)=>{
      return fs.writeFile(path,content,{encoding:'utf8'})
  },
  renameFile:(oldName,newName)=>{
    return fs.rename(oldName,newName)
  },
  deleteFile:(path)=>{
    return fs.unlink(path)
  }
}

// const currentPath = path.join(__dirname,'index.js')
// const writePath = path.join(__dirname,'index.md')
// fileHelper.readFile(currentPath).then(data=>console.log(data))
// fileHelper.writeFile(writePath,'# mdeditor').then(()=>console.log('写入成功'))
// fileHelper.renameFile(writePath,path.join(__dirname,'rename.md')).then(()=>console.log('重命名成功'))
// fileHelper.deleteFile(path.join(__dirname,'rename.md')).then(()=>console.log('删除成功'))

export const getParentNode = (node,parentClassName) =>{
  let current = node
  while(current!==null){
    if(current.classList.contains(parentClassName)){
      return current
    }
    current = current.parentNode
  }
  return false
}