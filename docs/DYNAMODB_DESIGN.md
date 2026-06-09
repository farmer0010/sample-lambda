# DynamoDB Single Table Design

## Use Case

### 메모 생성

* 사용자 메모 저장
* `memo_id`는 ULID 사용

### 메모 단건 조회

조회 패턴

* `GSI1PK = MEMO#{memo_id}`

### 메모 수정 / 삭제

조회 패턴

* `GSI1PK = MEMO#{memo_id}`
* 조회된 원본 PK(`GSI1SK`)와 SK(`GSI1PK`)를 이용하여 수정 및 삭제

### 전체 메모 조회

조회 패턴

* `PK = USER#{user_id}`
* `ScanIndexForward = False`

### 카테고리별 메모 조회

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

| Key           | Field  | Value         |
| ------------- | ------ | ------------- |
| Partition Key | GSI1PK | Base Table SK |
| Sort Key      | GSI1SK | Base Table PK |
