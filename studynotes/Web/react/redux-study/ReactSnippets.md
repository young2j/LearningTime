## Basic Methods

| Prefix  | Method                                              |
| :------ | :-------------------------------------------------- |
| `imp→`  | `import moduleName from 'module'`                   |
| `imn→`  | `import 'module'`                                   |
| `imd→`  | `import { destructuredModule } from 'module'`       |
| `ime→`  | `import * as alias from 'module'`                   |
| `ima→`  | `import { originalName as aliasName} from 'module'` |
| `exp→`  | `export default moduleName`                         |
| `exd→`  | `export { destructuredModule } from 'module'`       |
| `exa→`  | `export { originalName as aliasName} from 'module'` |
| `enf→`  | `export const functionName = (params) => { }`       |
| `edf→`  | `export default (params) => { }`                    |
| `met→`  | `methodName = (params) => { }`                      |
| `fre→`  | `arrayName.forEach(element => { }`                  |
| `fof→`  | `for(let itemName of objectName { }`                |
| `fin→`  | `for(let itemName in objectName { }`                |
| `anfn→` | `(params) => { }`                                   |
| `nfn→`  | `const functionName = (params) => { }`              |
| `dob→`  | `const {propName} = objectToDescruct`               |
| `dar→`  | `const [propName] = arrayToDescruct`                |
| `sti→`  | `setInterval(() => { }, intervalTime`               |
| `sto→`  | `setTimeout(() => { }, delayTime`                   |
| `prom→` | `return new Promise((resolve, reject) => { }`       |
| `cmmb→` | `comment block`                                     |
| `cp→`   | `const { } = this.props`                            |
| `cs→`   | `const { } = this.state`                            |

## React

| Prefix      | Method                                                       |
| :---------- | :----------------------------------------------------------- |
| `imr→`      | `import React from 'react'`                                  |
| `imrd→`     | `import ReactDOM from 'react-dom'`                           |
| `imrc→`     | `import React, { Component } from 'react'`                   |
| `imrcp→`    | `import React, { Component } from 'react' & import PropTypes from 'prop-types'` |
| `imrpc→`    | `import React, { PureComponent } from 'react'`               |
| `imrpcp→`   | `import React, { PureComponent } from 'react' & import PropTypes from 'prop-types'` |
| `imrm→`     | `import React, { memo } from 'react'`                        |
| `imrmp→`    | `import React, { memo } from 'react' & import PropTypes from 'prop-types'` |
| `impt→`     | `import PropTypes from 'prop-types'`                         |
| `imrr→`     | `import { BrowserRouter as Router, Route, Link } from 'react-router-dom'` |
| `redux→`    | `import { connect } from 'react-redux'`                      |
| `rconst→`   | `constructor(props) with this.state`                         |
| `rconc→`    | `constructor(props, context) with this.state`                |
| `est→`      | `this.state = { }`                                           |
| `cwm→`      | `componentWillMount = () => { }` DEPRECATED!!!               |
| `cdm→`      | `componentDidMount = () => { }`                              |
| `cwr→`      | `componentWillReceiveProps = (nextProps) => { }` DEPRECATED!!! |
| `scu→`      | `shouldComponentUpdate = (nextProps, nextState) => { }`      |
| `cwup→`     | `componentWillUpdate = (nextProps, nextState) => { }` DEPRECATED!!! |
| `cdup→`     | `componentDidUpdate = (prevProps, prevState) => { }`         |
| `cwun→`     | `componentWillUnmount = () => { }`                           |
| `gdsfp→`    | `static getDerivedStateFromProps(nextProps, prevState) { }`  |
| `gsbu→`     | `getSnapshotBeforeUpdate = (prevProps, prevState) => { }`    |
| `ren→`      | `render() { return( ) }`                                     |
| `sst→`      | `this.setState({ })`                                         |
| `ssf→`      | `this.setState((state, props) => return { })`                |
| `props→`    | `this.props.propName`                                        |
| `state→`    | `this.state.stateName`                                       |
| `rcontext→` | `const ${1:contextName} = React.createContext()`             |
| `cref→`     | `this.${1:refName}Ref = React.createRef()`                   |
| `fref→`     | `const ref = React.createRef()`                              |
| `bnd→`      | `this.methodName = this.methodName.bind(this)`               |