import React, { useState } from "react";
import axios from "axios";
import Layout from "components/Layout";

function Ranking() {
  const [userRanking, set_userRanking] = useState(true);

  const onSubmit_Ranking = (e: React.FormEvent) => {
    e.preventDefault();
    axios
      .get("/api/ranking")  
      .then(res => set_userRanking(res))
      .catch();
  };

  function 

  return (
    <Layout>
      <div onSubmit={isLogin ? onSubmit_Ranking : onSubmit_UserInsert}>
        <h2>랭킹</h2>
        <div>
          <label htmlFor="email">이메일: </label>
          <input
            type="email"
            name="email"
            autoComplete="on"
            placeholder="example@dgist.ac.kr"
          />
        </div>
      </div>
    </Layout>
  );
}

export default Ranking;
