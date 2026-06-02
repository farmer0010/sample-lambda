# DynamoDB Single Table Design

## Use Case

### 메모 생성

* 사용자 메모 저장

### 메모 단건 조회

조회 패턴

* PK = USER#{user_id}
* SK = MEMO#{memo_id}

### 메모 수정

조회 패턴

* PK = USER#{user_id}
* SK = MEMO#{memo_id}

### 메모 삭제

조회 패턴

* PK = USER#{user_id}
* SK = MEMO#{memo_id}

### 전체 메모 조회

조회 패턴

* GSI1PK = USER#{user_id}
* created_at 내림차순 정렬

### 카테고리별 메모 조회

조회 패턴

* GSI1PK = USER#{user_id}
* category FilterExpression
* created_at 내림차순 정렬

### 검색어 조회

조회 패턴

* GSI1PK = USER#{user_id}
* search_content FilterExpression
* created_at 내림차순 정렬

---

## Base Table

| Key | Value          |
| --- | -------------- |
| PK  | USER#{user_id} |
| SK  | MEMO#{memo_id} |

---

## GSI1

| Key    | Value          |
| ------ | -------------- |
| GSI1PK | USER#{user_id} |
| GSI1SK | created_at     |