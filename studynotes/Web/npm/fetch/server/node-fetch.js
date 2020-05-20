const fetch = require('node-fetch')
const Bluebird = require('bluebird');
fetch.Promise = Bluebird
const fs = require('fs')

/*
fetch(url,options)
    .then(res=>())
    .catch(err=>())
    .finally(()=>())

options = {
    // These properties are part of the Fetch Standard
    method: 'GET',
    headers: {},        // request headers. format is the identical to that accepted by the Headers constructor (see below)
    body: null,         // request body. can be null, a string, a Buffer, a Blob, or a Node.js Readable stream
    redirect: 'follow', // set to `manual` to extract redirect headers, `error` to reject redirect
    signal: null,       // pass an instance of AbortSignal to optionally abort requests
 
    // The following properties are node-fetch extensions
    follow: 20,         // maximum redirect count. 0 to not follow redirect
    timeout: 0,         // req/res timeout in ms, it resets on redirect. 0 to disable (OS limit applies). Signal is recommended instead.
    compress: true,     // support gzip/deflate content encoding. false to disable
    size: 0,            // maximum response body size in bytes. 0 to disable
    agent: null         // http(s).Agent instance or function that returns an instance (see below)
}
*/


//plain text or html
fetch('https://www.baidu.com/') //response
    .then(res => res.text()) //response.html
    .then(body => console.log(body)) //html.body
    .catch(error => console.error(error))

// Accessing Headers and other Meta data
fetch('https://www.baidu.com/')
    .then(res => {
        console.log(res.ok);
        console.log(res.status);
        console.log(res.statusText);
        console.log(res.headers.raw());
        console.log(res.headers.get('content-type'));
    });




// stream:下载pdf
const url = "http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/enquiry/c/8137628602822628.pdf"
fetch(url)
    .then(res => {
        const pdf = fs.createWriteStream('./inquiry.pdf')
        res.body.pipe(pdf)
    })
    .catch(err=>console.error(err))

//stream:上传
const { createReadStream } = require('fs');

const stream = createReadStream('input.txt');

fetch('https://httpbin.org/post', { method: 'POST', body: stream })
    .then(res => res.json())
    .then(json => console.log(json));




//json
fetch('https://api.github.com/users/github')
    .then(res => res.json())
    .then(json => console.log(json))




// Simple Post
fetch('https://httpbin.org/post', { method: 'POST', body: 'a=1' })
    .then(res => res.json()) // expecting a json response
    .then(json => console.log(json));




//Post with JSON
const body = { a: 1 };
fetch('https://httpbin.org/post', {
    method: 'post',
    body: JSON.stringify(body),
    headers: { 'Content-Type': 'application/json' },
})
    .then(res => res.json())
    .then(json => console.log(json));




// Post with form parameters
// 1
const { URLSearchParams } = require('url');

const params = new URLSearchParams();
params.append('a', 1);

fetch('https://httpbin.org/post', { method: 'POST', body: params })
    .then(res => res.json())
    .then(json => console.log(json));

// 2
const FormData = require('form-data');
const form = new FormData();
form.append('a', 1);

const options = {
    method: 'POST',
    body: form,
    headers: form.getHeaders()
}

fetch('https://httpbin.org/post', options)
    .then(res => res.json())
    .then(json => console.log(json));


    

//abort signal
import AbortController from 'abort-controller';

const controller = new AbortController();
const timeout = setTimeout(
    () => { controller.abort(); },
    150,
);

fetch(url, { signal: controller.signal })
    .then(res => res.json())
    .then(
        data => {
            useData(data)
        },
        err => {
            if (err.name === 'AbortError') {
                // request was aborted
            }
        },
    )
    .finally(() => {
        clearTimeout(timeout);
    });





//user agent
const httpAgent = new http.Agent({
    keepAlive: true
});
const httpsAgent = new https.Agent({
    keepAlive: true
});

const options = {
    agent: function (_parsedURL) {
        if (_parsedURL.protocol == 'http:') {
            return httpAgent;
        } else {
            return httpsAgent;
        }
    }
}