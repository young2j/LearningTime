/**********异步 action 创建函数******
如何把同步 action 创建函数和网络请求结合起来呢？
    标准的做法是使用 Redux Thunk 中间件。
    通过使用指定的 middleware，action 创建函数除了返回 action 对象外还可以返回函数。这时，这个 action 创建函数就成为了 thunk。

当 action 创建函数返回函数时，这个函数会被 Redux Thunk middleware 执行。
这个函数并不需要保持纯净；它还可以带有副作用，包括执行异步 API 请求、dispatch action。
 */
// thunk-actionCreator

import fetch from 'cross-fetch'

export const REQUEST_POSTS = 'REQUEST_POSTS'
function requestPosts(subreddit) {
    return {
        type: REQUEST_POSTS,
        subreddit
    }
}

export const RECEIVE_POSTS = 'RECEIVE_POSTS'
function receivePosts(subreddit, json) {
    return {
        type: RECEIVE_POSTS,
        subreddit,
        posts: json.data.children.map(child => child.data),
        receivedAt: Date.now()
    }
}

export const INVALIDATE_SUBREDDIT = 'INVALIDATE_SUBREDDIT'
export function invalidateSubreddit(subreddit) {
    return {
        type: INVALIDATE_SUBREDDIT,
        subreddit
    }
}

// 来看一下我们写的第一个 thunk action 创建函数！
// 虽然内部操作不同，你可以像其它 action 创建函数 一样使用它：
// store.dispatch(fetchPosts('reactjs'))

export function fetchPosts(subreddit) {

    // Thunk middleware 知道如何处理函数。
    // 这里把 dispatch 方法通过参数的形式传给函数，
    // 以此来让它自己也能 dispatch action。

    return function (dispatch) {

        // 首次 dispatch：更新应用的 state 来通知
        // API 请求发起了。

        dispatch(requestPosts(subreddit))

        // thunk middleware 调用的函数可以有返回值，
        // 它会被当作 dispatch 方法的返回值传递。

        // 这个案例中，我们返回一个等待处理的 promise。
        // 这并不是 redux middleware 所必须的，但这对于我们而言很方便。

        return fetch(`http://www.subreddit.com/r/${subreddit}.json`)
            .then(
                response => response.json(),
                // 不要使用 catch，因为会捕获
                // 在 dispatch 和渲染中出现的任何错误，
                // 导致 'Unexpected batch number' 错误。
                // https://github.com/facebook/react/issues/6895
                error => console.log('An error occurred.', error)
            )
            .then(json =>
                // 可以多次 dispatch！
                // 这里，使用 API 请求结果来更新应用的 state。

                dispatch(receivePosts(subreddit, json))
            )
    }
}


function shouldFetchPosts(state, subreddit) {
    const posts = state.postsBySubreddit[subreddit]
    if (!posts) {
        return true
    } else if (posts.isFetching) {
        return false
    } else {
        return posts.didInvalidate
    }
}

export function fetchPostsIfNeeded(subreddit) {

    // 注意这个函数也接收了 getState() 方法
    // 它让你选择接下来 dispatch 什么。

    // 当缓存的值是可用时，
    // 减少网络请求很有用。

    return (dispatch, getState) => {
        if (shouldFetchPosts(getState(), subreddit)) {
            // 在 thunk 里 dispatch 另一个 thunk！
            return dispatch(fetchPosts(subreddit))
        } else {
            // 告诉调用代码不需要再等待。
            return Promise.resolve()
        }
    }
}