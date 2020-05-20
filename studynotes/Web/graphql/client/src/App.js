import React from 'react';
import { ApolloProvider } from 'react-apollo'

import { ProductList,AddProduct } from './components'
import gqlClient from './graphql'



function App() {
  return (
    <ApolloProvider client={gqlClient}>
      <div className="App">
        <h1>产品列表</h1>
        <ProductList/>
        <AddProduct/>
      </div>
    </ApolloProvider>
  );
}

export default App;
