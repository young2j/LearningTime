new Vue({
    el:'#app1',
    data:{
        message:'页面加载于' + new Date().toLocaleDateString(),
        objects:{
            name: "vue",
            url: "http://www.runoob.com",
            slogan:'quant the world!'
        }
    }
});

// 使用 computed 性能会更好，但是如果你不希望缓存，你可以使用 methods 属性。

new Vue({
    el:"#app2",
    data:{
        rawStr:"猪是念来过倒",
    },
    computed:{
        computedStr:function () {
            return this.rawStr.split('').reverse().join('') + "---计算字段"
      }
    },
    methods:{
        reverseStr: function () {
            return this.rawStr.split('').reverse().join('')
        }
    }
});

var vw = new Vue({
            el:"#app3",
            data:{
                counter:1
            }
    });
vw.$watch("counter",function(nval,oval){
    alert('计数器值的变化 :' + oval + ' 变为 ' + nval + '!');
});

var vm = new Vue({
    el:"#app4",
    data:{
        kilometers:0,
        meters:0
    },
    computed:{},
    methods:{},
    watch:{
        kilometers:function(inputVal){
            this.kilometers = inputVal
            this.meters = this.kilometers*1000
        },
        meters:function(inputVal){
            this.meters = inputVal
            this.kilometers = this.meters/1000
        }
    }
});
vm.$watch('kilometers',function(newVal,oldVal){
    document.getElementById('tips').innerHTML = '修改千米：'+ oldVal + " ==> " + newVal
});

new Vue({
    el:'#app5',
    data:{
        apply1:true,
        apply2:false
    },
    methods:{
        switcher:function (event) {
            if (this.apply2) {
                this.apply2 = false
            }else{
                this.apply2 = true
            }
        }
    }
});
//同上
new Vue({
    el:'#app5_1',
    data:{
        clsobj:{
            style1:true, //主class
            'style2':false //次class
        }
    },
    methods:{
        switcher:function (event) {
            if (this.clsobj.style2){
                this.clsobj.style2 = false
            }else{
                this.clsobj.style2 = true
            }
        }
    }
});

new Vue({
    el:'#app5_2',
    data: {
        style1: 'style1',
        style2: 'style2'
    },
    methods:{
        switcher:function (envent) {
            if (this.style2){
                this.style2 = null
            } else {
                this.style2='style2'
            }
        }
    }
});

new Vue({
    el:'#app5_3',
    data: {
        style1:'style1',
        style2:'style2',
        addStyle:true,
    },
    methods:{
        switcher:function (event) {
            if (this.addStyle){
                this.addStyle = false
            } else{
                this.addStyle = true
            }
        }
    }
});

new Vue({
    el:"#app6",
    data:{
        somecolor:'green',
        fonsize:'50',
    }
})
new Vue({
    el:'#app6_1',
    data:{
        stlobj:{
            color:'red',
            fontSize:'50px',
        }
    }
});

new Vue({
    el:'#app6_2',
    data:{
        basestl: {
            color: 'blue',
            fontSize: '50px',
        },
        overridestl:{
            color:'purple',
            'font-weight':'bold',
        }
    }
})

new Vue({
    el:"#app7",
    data:{
        checked:false,
        which:[]
    }
})

new Vue({
    el:'#app7_1',
    data:{
        selected:'dog'
    }
})

new Vue({
    el:'#app8',
    data:{
        selected:''
    }
})

Vue.component('globalcomponent',{
    props:['symbol'], //传递组件参数
    template:'<h1>自定义全局组件{{ symbol }}</h1>'
})
new Vue({
    el:'#app9',
    data:{
        message:'!!!!'
    }
})

new Vue({
    el:'#app9_1',
    components:{
        'localcomponent':{
            template:'<h1>自定义局部组件</h1>'
        }
    }
})

Vue.component('foritem',{
    props:['element'],
    template:'<li>{{ element.text }}</li>'
})
new Vue({
    el:'#app9_2',
    data:{
        items:[
            {text:'value1'},
            {text:'value2'},
            {text:'value3'},
        ]
    }
})

/*
props验证:

Vue.component('my-component', {
  props: {
    // 基础的类型检查 (`null` 和 `undefined` 会通过任何类型验证)
    propA: Number,
    // 多个可能的类型
    propB: [String, Number],
    // 必填的字符串
    propC: {
      type: String,
      required: true
    },
    // 带有默认值的数字
    propD: {
      type: Number,
      default: 100
    },
    // 带有默认值的对象
    propE: {
      type: Object,
      // 对象或数组默认值必须从一个工厂函数获取
      default: function () {
        return { message: 'hello' }
      }
    },
    // 自定义验证函数
    propF: {
      validator: function (value) {
        // 这个值必须匹配下列字符串中的一个
        return ['success', 'warning', 'danger'].indexOf(value) !== -1
      }
    }
  }
})
 */
Vue.component('button-counter',{
    template:"<button v-on:click='increamentHandler'>{{ counter }}</button>",
    data:function(){
        return {
            counter:0
        }
    },
    methods:{
        increamentHandler:function () {
            this.counter+=1
            this.$emit('increament')
        }
    }
});
new Vue({
    el:'#app10',
    data:{
        total:0
    },
    methods:{
        increamentTotal:function () {
            this.total+=1
        }
    }
})

Vue.directive('focus',{
    inserted:function (el) {
        el.focus()
    }
});
new Vue({
    el:'#app11',
})

new Vue({
    el:"#app11_1",
    directives:{
        inserted:function (el) {
            el.focus()
        }
    }
})

Vue.directive('runoob', {
    bind: function (el, binding, vnode) {
        var s = JSON.stringify
        el.innerHTML =
            'name: '       + s(binding.name) + '<br>' +
            'value: '      + s(binding.value) + '<br>' +
            'expression: ' + s(binding.expression) + '<br>' +
            'argument: '   + s(binding.arg) + '<br>' +
            'modifiers: '  + s(binding.modifiers) + '<br>' +
            'vnode keys: ' + Object.keys(vnode).join(', ')
    }
})
new Vue({
    el: '#app12',
    data: {
        message: '菜鸟教程!'
    }
})

Vue.directive('sytax',function (el,binding) {
    el.innerHTML = binding.value.text
    el.style.backgroundColor = binding.value.color
})
new Vue({
    el:'#app13'
});



new Vue({
    el: '#app14',
    data: {
        show:true,
        styleobj :{
            fontSize:'30px',
            color:'red'
        }
    },
    methods : {
    }
});

new Vue({
    el: '#app14',
    data: {
        show: true
    }
})

new Vue({
    el: '#app15',
    data: {
        show: true
    }
})

new Vue({
  el: '#app16',
  data: {
    show: false
  },
  methods: {
    beforeEnter: function (el) {
      el.style.opacity = 0
      el.style.transformOrigin = 'left'
    },
    enter: function (el, done) {
      Velocity(el, { opacity: 1, fontSize: '1.4em' }, { duration: 300 })
      Velocity(el, { fontSize: '1em' }, { complete: done })
    },
    leave: function (el, done) {
      Velocity(el, { translateX: '15px', rotateZ: '50deg' }, { duration: 600 })
      Velocity(el, { rotateZ: '100deg' }, { loop: 2 })
      Velocity(el, {
        rotateZ: '45deg',
        translateY: '30px',
        translateX: '30px',
        opacity: 0
      }, { complete: done })
    }
  }
})


window.onload = function(){
var vm = new Vue({
    el:'#app17',
    data:{
        msg:'Hello World!',
    },
    methods:{
        get:function(){
            //发送get请求
            this.$http.get('/try/ajax/ajax_info.txt').then(function(res){
                document.write(res.body);    
            },function(){
                console.log('请求失败处理');
            });
        }
    }
});
}

window.onload = function(){
	var vm = new Vue({
	    el:'#app18',
	    data:{
	        msg:'Hello World!',
	    },
	    methods:{
	        post:function(){
	            //发送 post 请求
	            this.$http.post('/try/ajax/demo_test_post.php',{name:"菜鸟教程",url:"http://www.runoob.com"},{emulateJSON:true}).then(function(res){
                    document.write(res.body);    
                },function(res){
                    console.log(res.status);
                });
	        }
	    }
	});
}




























// 1. 定义（路由）组件。
// 可以从其他文件 import 进来
const Foo = { template: '<div>foo</div>' }
const Bar = { template: '<div>bar</div>' }

// 2. 定义路由
// 每个路由应该映射一个组件。 其中"component" 可以是
// 通过 Vue.extend() 创建的组件构造器，
// 或者，只是一个组件配置对象。
// 我们晚点再讨论嵌套路由。
const routes = [
  { path: '/foo', component: Foo },
  { path: '/bar', component: Bar }
]

// 3. 创建 router 实例，然后传 `routes` 配置
// 你还可以传别的配置参数, 不过先这么简单着吧。
const router = new VueRouter({
  routes // （缩写）相当于 routes: routes
})

// 4. 创建和挂载根实例。
// 记得要通过 router 配置参数注入路由，
// 从而让整个应用都有路由功能
const app = new Vue({
  router
}).$mount('#app_unk')















