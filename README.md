# VodkaPay

간편하고 효율적인 외상 장부

## TODO

- [ ] Frontend 제작
- [ ] Backend 제작

## HTTP routing

1. Frontend (by `react-router-dom`)

| **Name**          | **Path**   | **Comment**                      |
| ----------------- | ---------- | -------------------------------- |
| **Main**          | `/`        | 메인 화면. 로그인 페이지가 뜬다. |
| **Sign-up**       | `/signup`  | 회원가입 화면.                   |
| **User info.**    | `/my`      | 유저 정보 화면                   |
| **Users Ranking** | `/ranking` | 유저들 랭킹 화면                 |
| **Event**         | `/event`   | 이벤트 관리 화면                 |

2. Backend

| **Name**       | **Path**       | **Comment**      | **C** | **R** | **U** | **D** |
| -------------- | -------------- | ---------------- | ----- | ----- | ----- | ----- |
| **User**       | `/api/user`    | 유저 관련 요청   | Y     | Y     | Y     | Y     |
| **Event**      | `/api/event`   | 이벤트 관련 요청 | Y     | Y     | Y     | Y     |
| **Ranking**    | `/api/ranking` | 랭킹 관련 요청   |       | Y     |       |       |
| **Statistics** | `/api/stat`    | 통계 관련 요청   |       | Y     |       |       |

- Note: RESTful CRUD rule
  | **HTTP method** | **Meaning in CRUD** |
  |-----------------|---------------------|
  | **POST** | Create |
  | **GET** | Read |
  | **PUT** | Update (entire) |
  | **PATCH** | Update (partial) |
  | **DELETE** | Delete |

## Design

|              | **Concept** | **Implementation** |
| ------------ | ----------- | ------------------ |
| **Frontend** | SPA         | ReactJS            |
| **Backend**  | RESTful     | NodeJS express     |
| **Database** | Relational  | Sqite3             |
