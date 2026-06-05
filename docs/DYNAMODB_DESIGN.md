# DynamoDB Single Table Design

## Use Case

### 메모 생성

* 사용자 메모 저장

### 메모 단건 조회

조회 패턴

* GSI1PK = MEMO#{memo_id}

### 메모 수정

조회 패턴

* GSI1PK = MEMO#{memo_id}

### 메모 삭제

조회 패턴

* GSI1PK = MEMO#{memo_id}

### 전체 메모 조회

조회 패턴

* PK = USER#{user_id}
* ScanIndexForward = False

### 카테고리별 메모 조회

조회 패턴

* GSI2PK = USER#{user_id}#CATEGORY#{category}
* ScanIndexForward = False

### 검색어 조회

조회 패턴

* PK = USER#{user_id}
* 애플리케이션 레벨 문자열 필터링

---

## Base Table

| Key | Value               |
| --- | ------------------- |
| PK  | USER#{user_id}      |
| SK  | MEMO#{memo_id_ulid} |

---

## GSI1

| Key    | Value         |
| ------ | ------------- |
| GSI1PK | Base Table SK |
| GSI1SK | Base Table PK |

---

## GSI2

| Key    | Value                              |
| ------ | ---------------------------------- |
| GSI2PK | USER#{user_id}#CATEGORY#{category} |
| GSI2SK | Base Table SK                      |
