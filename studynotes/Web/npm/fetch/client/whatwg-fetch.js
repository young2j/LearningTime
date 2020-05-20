// import {fetch} from 'whatwg-fetch'
import 'whatwg-fetch'

//html/text
url = 'http://rap2api.taobao.org/app/mock/236247/example/1573449345503'
fetch(url)
    .then(res=>res.text())
    .then(body=>console.log(body))

//json
fetch(url)
    .then(res=>res.json())
    .then(json=>console.log('json:',json))
    .catch(err=>console.error(err))

//metadata
fetch(url).then(res=> {
    console.log(res.headers.get('Content-Type'))
    console.log(res.headers.get('Date'))
    console.log(res.status)
    console.log(res.statusText)
})



// Post form
var form = document.querySelector('form')

fetch('/users', {
    method: 'POST',
    body: new FormData(form)
})


// Post JSON
fetch('/users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Hubot',
        login: 'hubot',
    })
})


// File upload
var input = document.querySelector('input[type="file"]')

var data = new FormData()
data.append('file', input.files[0])
data.append('user', 'hubot')

fetch('/avatars', {
    method: 'POST',
    body: data
})



//abort request
import 'abortcontroller-polyfill/dist/abortcontroller-polyfill-only'
import { fetch } from 'whatwg-fetch'

// use native browser implementation if it supports aborting
const abortableFetch = ('signal' in new Request('')) ? window.fetch : fetch

const controller = new AbortController()

abortableFetch('/avatars', {
    signal: controller.signal
}).catch(function (err) {
    if (err.name === 'AbortError') {
        console.log('request aborted')
    }
})

// some time later...
controller.abort()