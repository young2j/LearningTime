import React from 'react';
import { setInterval } from 'timers';

//-------------组件--------
function Welcome(props) {
    return <h1 className='header'>Hello, {props.name}</h1>;
}


// function Clock(props) {
//     return (
//         <div className='timeNow'>
//             <h1>Time Tips:</h1>
//             <h2>It is already {props.date.toLocaleTimeString()}</h2>
//         </div>
//     );
// }
// function tick() {
//     ReactDOM.render(
//         <Clock date={new Date()}/>,
//         document.getElementById('time')
//     );
// }
// setInterval(tick, 1000);

//-------------------状态和生命周期--------------------
class Clock extends React.Component {
    constructor(props) {
        super(props);
        this.state = { date: new Date() }; //构造函数是唯一可以给this.state赋值的地方
    };

    componentDidMount() { //生命周期方法，当组件挂载或卸载时就会去执行这些方法
        this.timerID = setInterval(
            () => {
                this.tick()
            }, 1000);
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    tick() {
        this.setState({ //不要直接修改state，构造函数是唯一可以给this.state赋值的地方，应始终通过setState方法修改
            date: new Date()
        });
    }

    render() {
        return (
            <div className="timeNow">
                <hr />
                <h2>Time Tips:</h2>
                <p>It is already {this.state.date.toLocaleTimeString()}.</p>
            </div>
        )
    }
}

//-------------------事件处理--------------------
class Toggle extends React.Component {
    constructor(props) {
        super(props);
        this.state = { isToggleOn: true };
        // this.handleClick = this.handleClick.bind(this);
    }

    // handleClick(){
    //     this.setState({
    //         isToggleOn:!this.state.isToggleOn
    //     })
    // }
    handleClick = () => {
        this.setState({
            isToggleOn: !this.state.isToggleOn
        })
    }

    render() {
        return (
            <button onClick={this.handleClick}>
                {this.state.isToggleOn ? 'ON' : 'OFF'}
            </button>
        )
    }
}

//--------------------条件渲染-----------------------
function LoginButton(props) {
    return (
        <button onClick={props.onClick}>Login</button>
    )
}

function LogoutButton(props) {
    return (
        <button onClick={props.onClick}>Logout</button>
    )
}

class LoginControl extends React.Component {
    constructor(props) {
        super(props);
        this.state = { isLogin: true };
    }

    loginClick = () => {
        this.setState({ isLogin: false })
    }
    logoutClick = () => {
        this.setState({ isLogin: true })
    }

    render() {
        const login = this.state.isLogin;
        // 条件渲染1
        // let button;
        // if (login){
        //     button = <LoginButton onClick={this.loginClick}/>
        // } else {
        //     button = <LogoutButton onClick={this.logoutClick} />
        // }
        // return (
        //     <div>
        //         {button}
        //     </div>
        // )

        // 条件渲染2
        // return (
        //     <div>
        //         {login? (<LoginButton onClick={this.loginClick}/>):(<LogoutButton onClick={this.logoutClick}/>)}
        //     </div>
        // )
        //条件渲染3
        return (
            <div>
                {login && <LoginButton onClick={this.loginClick} />}
                {login || <LogoutButton onClick={this.logoutClick} />}
            </div>
        )
    }
}

//------------------列表和KEY--------------------------
function ListItems(props) {
    const list = props.list
    const listItems = list.map(
        //一个好的经验法则是：在 map() 方法中的元素需要设置 key 属性。
        //key 在其兄弟节点之间应该是独一无二的。
        // (item,index) =>
        //     <li key={index}>
        //         {item}
        //     </li>
        (item) =>
            <li key={item.id}>
                {item.value}
            </li>
    )
    return (
        <ul>{listItems}</ul>
    )
}


//-----------------------表单-------------------------
class NameForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '666',
            text: 'You like ',
            selection: ""
        };
    }

    handleNameChange = (e) => {
        this.setState({
            name: e.target.value.toUpperCase(),
        })
    }

    handleTextChange = (e) => {
        this.setState({
            text: e.target.value,
        })
    }

    handleSelecChange = (e) => {
        this.setState({
            selection: e.target.value
        })
    }

    handleSubmit = (e) => {
        alert(this.state.text + this.state.selection + '\nyour name is: ' + this.state.name);
        e.preventDefault(); //阻止默认行为，等同于原生js事件函数返回false
    }
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label htmlFor="selection">SELECTION
                     <select multiple={true} value={[this.state.selection]} onChange={this.handleSelecChange}>
                        <option value="发">发快递发</option>
                        <option value="三三">三国时代</option>
                        <option value="十分">十公分的身高</option>
                        <option value="如果">十多个如果</option>
                    </select>
                </label>
                <textarea value={this.state.text} onChange={this.handleTextChange} cols="50" rows="6"></textarea>
                <label htmlFor="name">
                    大名:
                    <input type="text" value={this.state.value} onChange={this.handleNameChange} />
                </label>
                <input type="submit" value='提交' />
            </form>
        )
    }
}

//------------------------------状态提升----------------------------
const scaleNames = {
    c: 'Celsius',
    f: 'Fahrenheit'
};

function toCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5 / 9;
}
function toFahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}

function tryConvert(temperature, convert) {
    const input = parseFloat(temperature);
    if (Number.isNaN(input)) {
        return '';
    }
    const output = convert(input);
    const rounded = Math.round(output * 1000) / 1000;
    return rounded.toString();
}

function BoilingVerdict(props) {
    if (props.celsius >= 100) {
        return <p>the water would boil</p>
    }
    return <p>the water would not boil</p>
}

class TemperatureInput extends React.Component {
    constructor(props) {
        super();
        // this.state = {temperature:''};
    }

    handleChange = (e) => {
        // this.setState({temperature:e.target.value});
        this.props.onTemperatureChange(e.target.value);

    }

    render() {
        // const temperature = this.state.temperature;
        const temperature = this.props.temperature;
        const scale = this.props.scale;

        return (
            <fieldset>
                <legend>Enter temperature in {scaleNames[scale]}:</legend>
                <input value={temperature} onChange={this.handleChange} />
            </fieldset>
        )
    }
}

class Calculator extends React.Component {
    constructor(props) {
        super(props);
        this.state = { temperature: '', scale: 'c' };
    }

    handleCelsiusChange = (temperature) => {
        this.setState({ scale: 'c', temperature });
    }

    handleFahrenheitChange = (temperature) => {
        this.setState({ scale: 'f', temperature });
    }

    render() {
        const scale = this.state.scale;
        const temperature = this.state.temperature;
        const celsius = scale === 'f' ? tryConvert(temperature, toCelsius) : temperature;
        const fahrenheit = scale === 'c' ? tryConvert(temperature, toFahrenheit) : temperature;
        
        return (
            <div>
                <TemperatureInput
                    scale='c' temperature={celsius}
                    onTemperatureChange={this.handleCelsiusChange}/>
                <TemperatureInput
                    scale='f' temperature={fahrenheit}
                    onTemperatureChange={this.handleFahrenheitChange}/>
                <BoilingVerdict celsius={parseFloat(celsius)}/>
            </div>
        )
    }
}

//-------------------------组合---------------------
function FancyBorder(props){
    return (
        <div className={'FancyBorder-' + props.color}>
            {props.children}
        </div>
    )
}

function Dialog(props){
    return (
        <FancyBorder color="blue">
            <h1 className="title">
                {props.title}
            </h1>
            <p className="message">
                {props.message}
            </p>
            {props.children}
        </FancyBorder>
    )
}

class SignUpDialog extends React.Component{
    constructor(props){
        super(props);
        this.state ={'login': ''};
    }

    handleChange =(e) => {
        this.setState({login:e.target.value});
    }

    handleSignUp = (e) => {
        alert(`Welcome aboard,${this.state.login}!`);
    }

    render() {
        return (
            <Dialog title='Hello YSJ' message='this part is about component combination.'>
                <input value={this.state.login} onChange={this.handleChange}/>
                <button onClick={this.handleSignUp}>
                    Sign Up
                </button>
                <div>
                    <input type="file"/>
                    <button type='submit'>提交</button>
                </div>
            </Dialog>
        )
    }
}


//------------------鼠标和键盘事件-----------------------
class BlurExample extends React.Component{
    constructor(props){
        super(props);
        this.state = {isOpen:false};
        this.timeOutId = null;
    }   

    onClickHandler = ()=> {
        this.setState(currentState => ({
            isOpen:!currentState.isOpen
        }));
    }

    onBlurHandler = () => {
        this.timeOutId = setTimeout(() => {
            this.setState({
                isOpen: false
            });
        });
    }

    onFocusHandler = () => {
        clearTimeout(this.timeOutId);
    }

    render() {
        return (
            <div onBlur={this.onBlurHandler} onFocus={this.onFocusHandler}>
                <button onClick = {this.onClickHandler} 
                aria-haspopup='true' aria-expanded={this.state.isOpen}>
                    select an option
                </button>
                {this.state.isOpen && (
                    <ul>
                        <li>op1</li>
                        <li>op2</li>
                        <li>op3</li>
                    </ul>
                )}
            </div>
        )
    }

}

//---------------------------------
function App() {
    const list = [{ id: 1, value: '床前明月光' }, { id: 2, value: '疑是地上霜' },
    { id: 3, value: '举头望明月' }, { id: 4, value: '低头鞋一双' }];
    return (
        <div>
            <Welcome name="ysj"></Welcome>
            <Clock />
            <Toggle />
            <LoginControl />
            <ListItems list={list} />
            <NameForm />
            <Calculator />
            <SignUpDialog/>
            <BlurExample/>
        </div>
    );
}

export default App;
