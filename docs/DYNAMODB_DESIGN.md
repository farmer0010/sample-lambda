# DynamoDB Single Table Design

## Use Case

### 메모 생성

* 사용자 메모 저장
* `memo_id`는 ULID 사용

### 메모 단건 조회

조회 패턴

* `MemoLookupIndex`의 Partition Key = `MEMO#{memo_id}`

### 메모 수정 / 삭제

조회 패턴

* `MemoLookupIndex`의 Partition Key = `MEMO#{memo_id}`
* 조회된 Base Table의 PK와 SK를 이용하여 수정 및 삭제

### 특정 유저의 전체 메모 조회

조회 패턴

* `PK = USER#{user_id}`
* `ScanIndexForward = False`

### 특정 유저의 카테고리별 메모 조회

조회 패턴

* `PK = USER#{user_id}`
* `LSI1SK begins_with C#{category}#`
* `ScanIndexForward = False`

---

## Base Table

| Key           | Field  | Value                      |
| ------------- | ------ | -------------------------- |
| Partition Key | PK     | `USER#{user_id}`           |
| Sort Key      | SK     | `MEMO#{memo_id}`           |
| LSI1 Sort Key | LSI1SK | `C#{category}#M#{memo_id}` |

---

## LSI1 (CategoryIndex)

| Key           | Field  | Value                      |
| ------------- | ------ | -------------------------- |
| Partition Key | PK     | Base Table PK              |
| Sort Key      | LSI1SK | `C#{category}#M#{memo_id}` |

---

## GSI1 (MemoLookupIndex)

| Key           | Field | Value                      |
| ------------- | ----- | -------------------------- |
| Partition Key | SK    | `MEMO#{memo_id}`  |
| Sort Key      | PK    | `USER#{user_id}` |
