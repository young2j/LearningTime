hello = require('./hello')
hello.a('ysj')
hello.b()

process.nextTick(function () {
    console.log('nextTick callback')
})
console.log('nextTick was set')

process.on('exit',function () {
    console.log('typeof window:',typeof(global))
})