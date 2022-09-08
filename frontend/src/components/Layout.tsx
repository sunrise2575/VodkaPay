import Header from "components/Header";
import Footer from "components/Footer";
import React from 'react';

function App(props: React.PropsWithChildren) {
  return (
    <div>
      <Header />
      <main>{props.children}</main>
      <Footer />
    </div>
  );
}

export default App;
