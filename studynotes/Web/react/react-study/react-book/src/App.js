import React from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'
// import style from './tabs.scss'
import qrimg from './qr.jpg'
import { format } from 'path'


// 深入react技术栈
//-----------------???没有渲染效果----------------------
// class Tabs extends React.Component {
//     static propTypes = {
//         className: PropTypes.string,
//         classPrefix: PropTypes.string,
//         children: PropTypes.oneOfType([
//             PropTypes.arrayOf(PropTypes.node),
//             PropTypes.node,
//         ]),
//         defaultActiveIndex: PropTypes.number,
//         activeIndex: PropTypes.number,
//         onChange: PropTypes.func,
//     }
    
//     static defaultProps ={
//         classPrefix: 'tabs',
//         onChange: ()=>{},
//     }

//     constructor(props){
//         super(props)
//         this.handleTabClick = this.handleTabClick.bind(this)
//         const currProps = this.props
        
//         let activeIndex
//         if ('activeIndex' in currProps) {
//             activeIndex = currProps.activeIndex
//         } else if ('defaultActiveIndex' in currProps) {
//             activeIndex = currProps.defaultActiveIndex
//         }
        
//         this.state = {
//             activeIndex,
//             prevIndex: activeIndex,
//         }
//     }

//     componentWillReceiveProps(nextProps) { //props发生变化时执行，初始化render时不执行
//         if ('activeIndex' in nextProps) {
//             this.setState({
//                 activeIndex:nextProps.activeIndex
//             })
//         }
//     }

//     handleTabClick(activeIndex) {
//         const prevIndex = this.state.activeIndex
//         if (this.state.activeIndex !== activeIndex && 
//             'defaultActiveIndex' in this.props) {
//                 this.setState({
//                     activeIndex,
//                     prevIndex
//                 })
//                 this.props.onChange({activeIndex,prevIndex})
//             }
//     }

//     renderTabNav(){
//         const {classPrefix,children} = this.props

//         return (
//             <TabNav 
//                 key='tabBar'
//                 classPrefix = {classPrefix}
//                 onTabClick = {this.handleTabClick}    
//                 panels = {children}
//                 activeIndex  = {this.state.activeIndex}
//             />
//         )
//     }

//     renderTabContent() {
//         const {classPrefix,children} = this.props

//         return (
//             <TabContent
//                 key='tabcontent'
//                 classPrefix={classPrefix}
//                 panels={children}
//                 activeIndex={this.state.activeIndex}
//             />
//         )
//     }

//     render(){
//         const {className} = this.props
//         const classes = classnames(className,'ui-tabs')

//         return (
//             <div className={classes}>
//                 {this.renderTabNav()}
//                 {this.renderTabContent()}
//             </div>
//         )
//     }
// }

// class TabNav extends React.Component {
//     static propTypes = {
//         classPrefix:PropTypes.string,
//         panels:PropTypes.node,
//         activeIndex:PropTypes.number,
//     }

//     getTabs = ()=>{
//         const  {panels,classPrefix,activeIndex} = this.props

//         return React.Children.map(panels,(child)=>{
//             if (!child) {return}
//             const order = parseInt(child.props.order,10)
//             let classes = classnames ({
//                 [`${classPrefix}-tab`]:true,
//                 [`${classPrefix}-active`] : activeIndex===order,
//                 [`${classPrefix}-disabled`]: child.props.disabled,
//             })

//             let events = {}
//             if (!child.props.disabled){
//                 events = {
//                     onClick:this.props.onTabClick.bind(this,order)
//                 }
//             }
//             const ref = {}
//             if (activeIndex === order) {
//                 ref.ref = 'activeTab'
//              }
//             return (
//                 <li role='tab' 
//                 aria-disabled = {child.props.disabled? 'true':'false'}
//                 aria-selected={activeIndex===order? 'true':'false'}
//                 {...events}
//                 className={classes}
//                 key = {order}
//                 {...ref}
//                 >
//                     {child.props.tab}
//                 </li>
//             )
//         })
//     }

//     render() {
//         const {classPrefix} =this.props
//         const rootClasses = classnames({
//             [`${classPrefix}-nav`]:true,
//         })

//         const classes = classnames({
//             [`${classPrefix}-nav`]:true,
//         })

//         return (
//             <div className={rootClasses} role='tablist'>
//                 <ul className={classes}>
//                     {this.getTabs()}
//                 </ul>
//             </div>
//         )
//     }
// }

// class TabContent extends React.Component {
//     static propTypes = {
//         classPrefix: PropTypes.string,
//         panels:PropTypes.node,
//         activeIndex:PropTypes.number,
//     }
//     // constructor(props){
//     //     super(props)
//     //     this.getTabPanes = this.getTabPanes().bind(this)
//     // }

//     getTabPanes() {
//         const {classPrefix,activeIndex,panels} = this.props

//         return React.children.map(panels,(child) => {
//             if (!child){return}
//             const order = parseInt(child.props.order,10)
//             const isActive = activeIndex === order

//             return React.cloneElement(child,{
//                 classPrefix,
//                 isActive,
//                 children:child.props.children,
//                 key:`tabpane-${order}`
//             })
//         })
//     }

//     render() {
//         const {classPrefix} = this.props
//         const classes = classnames ({
//             [`${classPrefix}-content`]:true,
//         })

//         return (
//             <div className={classes}>
//                 {this.getTabPanes}
//             </div>
//         )
//     }
// }

// class TabPane extends React.Component {
//     static propTypes = { 
//         tab:PropTypes.oneOfType([
//             PropTypes.string,
//             PropTypes.node,
//         ]).isRequired,
//         order:PropTypes.string.isRequired,
//         disabled:PropTypes.bool,
//         isActive:PropTypes.bool,
//     }
//     render() {
//         const {classPrefix,className,isActive,children}=this.props
//         const classes = classnames({
//             [className]:className,
//             [`${classPrefix}-panel`]:true,
//             [`${classPrefix}-active`]:isActive
//         })
//         return (
//             <div role='tabpanel'
//             className = {classes}
//             aria-hidden={!isActive}>
//                 {children}
//             </div>
//         )
//     }
// }

//-----------------------------------
//在react中使用原生事件
class NativeEventDemo extends React.Component{
    componentDidMount(){
        this.refs.button.addEventListener('click',e=>{
            this.handleClick(e)
        })
    }

    handleClick(e){
        console.log(e)
    }

    componentWillUnmount(){
        this.refs.button.removeEventListener('click')
    }
    render(){
        return (
            <button ref="button">Test</button>
        )
    }
}

//合成事件与原生事件混用---要尽量避免混用

class QrCode extends React.Component {
    constructor(props){
        super(props)
        this.handleClick = this.handleClick.bind(this)
        this.handleClickQr = this.handleClickQr.bind(this)

        this.state = {
            active:false
        }
    }

    componentDidMount() { //初始化render时执行
        document.body.addEventListener('click',e => {
            if (e.target && e.target.matches('div.code')) {
                return
            }
            this.setState({
                active:false
            })
        })
    }

    componentWillUnmount () {
        document.body.removeEventListener('click')
    }

    handleClick() {
        this.setState({
            active:!this.state.active
        })
    }

    handleClickQr(e) {
        e.stopPropagation()
    }

    render(){
        return(
            <div className="qr-wrapper">
                <button className='qr' onClick={this.handleClick}>二维码</button>
                <div className='code' style={{display:this.state.active ? 'block' : 'none'}} onClick = {this.handleClickQr}>
                    <img src={qrimg} alt='qr'/>
                </div>
            </div>
        )
    }
}

//--------------表单组件------------------------
//文本框+单选框+复选框+下拉列表【受控组件】
/*
React 受控组件更新 state 的流程：
(1) 可以通过在初始 state 中设置表单的默认值。
(2) 每当表单的值发生变化时，调用 onChange 事件处理器。
(3) 事件处理器通过合成事件对象 e 拿到改变后的状态，并更新应用的 state。
(4) setState 触发视图的重新渲染，完成表单组件值的更新。
*/
class TextFrame extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            inputVlaue: '',
            textareaValue:'',
            radioValue:'',
            checkboxValue:[],
            selectValue:'',
            selectValues:[]
        }
    }

    handleInputChange = (e) => {
        this.setState({
            inputVlaue: e.target.value,
        })
    }
    handleTextareaChange = (e) =>{
        this.setState({
            textareaValue:e.target.value.substring(0,10)
        })
    }
    handleRadioChange = (e) => {
        this.setState({
            radioValue: e.target.value
        })
    }
    handleCheckBoxChange = (e) => {
        const {checked,value} = e.target
        let checkboxValue = this.state.checkboxValue
        if (checked && checkboxValue.indexOf(value)===-1){
            checkboxValue.push(value)
        } else {
            checkboxValue = checkboxValue.filter(v => v!==value)
        }
        this.setState({
            checkboxValue:checkboxValue
        })
    }
    handleSelectValueChange = (e) => {
        this.setState({
            selectValue: e.target.value
        })
    }

    handleSelectValuesChange = (e) => {
        let options = e.target
        // console.log(Object.keys(options))
        const selectedValues = Object.keys(options)
            .filter(i => options[i].selected===true)
            .map(i=>options[i].value)
            
        this.setState({
            selectValues:selectedValues
        })
    }
    render() {
        const {inputValue,textareaValue,
               radioValue,checkboxValue,
               selectValue,selectValues} = this.state
        return (
            <div>
                <p>单行输入框:
                    <input type="text" value={inputValue} onChange={this.handleInputChange}/>
                </p>
                <p>多行输入框:
                    <textarea type="text" value={textareaValue} onChange={this.handleTextareaChange}/>
                </p>


                <p>单选框：gender:</p>
                <label htmlFor="male">male
                    <input type="radio" value='male' checked={radioValue==='male'} onChange={this.handleRadioChange}/>
                </label>
                <label htmlFor="female">female
                    <input type="radio" value='female' checked={radioValue==='female'} onChange={this.handleRadioChange}/>
                </label>


                <p>多选框：请做选择：</p>
                <label htmlFor="">
                    <input type="checkbox" value='AAA' checked={checkboxValue.indexOf('AAA')!==-1} onChange = {this.handleCheckBoxChange} />
                    'AAA'
                </label>
                <label htmlFor="">
                    <input type="checkbox" value='AAB' checked={checkboxValue.indexOf('AAB')!==-1} onChange = {this.handleCheckBoxChange} />
                    'AAB'
                </label>

                <p>下拉单选项：</p>
                <select value={selectValue} onChange = {this.handleSelectValueChange}>
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                </select>

                <p>下拉多选项：</p>
                <select multiple={true} value={selectValues} onChange = {this.handleSelectValuesChange}>
                    <option value="钱">钱</option>
                    <option value="RMB">RMB</option>
                    <option value="很多">很多</option>
                </select>
            </div>
        )
    }

}

//---------------------------------
//【非受控组件】
//非受控组件是一种反模式，它的值不受组件自身的 state 或 props 控制。
//通常，需要通过为其添加 ref prop 来访问渲染后的底层 DOM 元素。

class UncontroledComponent extends React.Component {
    constructor(props) {
        super(props)
        this.handleSubmit = this.handleSubmit.bind(this)
    }
    handleSubmit(e) {
        e.preventDefault()
        const {value} = this.refs.name
        console.log(value)
    }
    render(){
        return(
            <form onSubmit={this.handleSubmit}>
                <input type="text" ref='name' defaultValue='Chengdu'/>
                <button type='submit' defaultChecked={true}>Submit</button>
            </form>
        )
    }
}

//通过 defaultValue 或者 defaultChecked 来设置表单的默认值，它仅会被渲染一次，在后续的渲染时并不起作用。
//受控组件和非受控组件的最大区别是：非受控组件的状态并不会受应用状态的控制，应用中也而受控组件的值来自于组件的 state。
class CompareControled extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            value:'defaultValue render only once'
        }
    }
    render() {
        return (
            <>
            <input type="text" value={this.state.value}
                onChange={e => {
                    this.setState({
                        value: e.target.value.toUpperCase()
                    })
                }} />
            <input type="text" defaultValue={this.state.value}
                onChange={e => {
                    this.setState({
                        value: e.target.value.toUpperCase()
                    })
                }}/>
            </>
        )
    }
}

//---------------表单事件绑定------------------
class FormApp extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            name:'',
            age:18
        }
    }

    handleChange(name,e){
        const {value} = e.target
        this.setState({
            [name]:value
        })
    }
    render(){
        const {name,age} = this.state

        return (
            <div>
                <input type="text" value={name} onChange={this.handleChange.bind(this,'name')}/>
                <input type="text" value={age} onChange={this.handleChange.bind(this,'age')}/>
            </div>
        )
    }
}

//-------------样式---------------------
//  自定义组件建议支持 className prop，以让用户使用时添加自定义样式；
//  设置行内样式时要使用对象。

//---------------------------------
function App() {
    return (
        <>
            <p>深入react技术栈</p>
            {/* <Tabs/> */}
            <NativeEventDemo/>
            <QrCode/>
            <TextFrame/>
            <UncontroledComponent/>
            <CompareControled/>
            <FormApp/>
        </>
    );
}

export default App;