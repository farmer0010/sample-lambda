# DynamoDB Single Table Design

## Use Case

### 메모 생성

* 사용자 메모 저장
* memo_id는 ULID 사용

### 메모 단건 조회

조회 패턴

* GSI1PK = MEMO#{memo_id}

### 메모 수정 / 삭제

조회 패턴

* GSI1PK = MEMO#{memo_id}
* 조회된 원본 PK, SK를 이용하여 수정 및 삭제 진행

### 전체 메모 조회

조회 패턴

* PK = USER#{user_id}
* ScanIndexForward = False

### 카테고리별 메모 조회

조회 패턴

* GSI2PK = USER#{user_id}#CATEGORY#{category}
* ScanIndexForward = False

---

## Base Table

| Key | Value          |
| --- | -------------- |
| PK  | USER#{user_id} |
| SK  | MEMO#{memo_id} |

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
