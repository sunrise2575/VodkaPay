import React, { useState } from "react";
import axios from "axios";
import Layout from "components/Layout";

function UserAuth() {
  const [isLogin, set_PageState] = useState(true);

  const handle_PageState = () => {
    set_PageState(false);
  };

  const onSubmit_UserAuth = (e: React.FormEvent) => {
    e.preventDefault();
    var payload = {
      email: e.target[0].value,
      password: e.target[1].value,
    };
    axios
      .post("/api/user/login", payload, {
        headers: { "Content-Type": "application/json" },
      })
      .then((res) => console.log(res))
      .catch();
  };

  const onSubmit_UserInsert = (e: React.FormEvent) => {
    e.preventDefault();
    var payload = {
      email: e.target[0].value,
      password: e.target[1].value,
      name: e.target[2].value,
    };
    axios
      .post("/api/user/new", payload, {
        headers: { "Content-Type": "application/json" },
      })
      .then((res) => console.log(res))
      .catch();
  };

  return (
    <Layout>
      <form onSubmit={isLogin ? onSubmit_UserAuth : onSubmit_UserInsert}>
        <h2>{isLogin ? "로그인" : "회원가입"}</h2>
        <div>
          <label htmlFor="email">이메일: </label>
          <input
            type="email"
            name="email"
            autoComplete="on"
            placeholder="example@dgist.ac.kr"
          />
        </div>
        <div>
          <label htmlFor="password">비밀번호: </label>
          <input type="password" name="password" autoComplete="on" />
        </div>
        {!isLogin && (
          <div>
            <label htmlFor="name">실명: </label>
            <input type="text" name="name" placeholder="홍길동" />
          </div>
        )}
        <div>
          {isLogin && <input type="submit" value="로그인" />}
          <input
            type={isLogin ? "button" : "submit"}
            onClick={isLogin ? handle_PageState : undefined}
            value="회원가입"
          />
        </div>
      </form>
    </Layout>
  );
}

export default UserAuth;
