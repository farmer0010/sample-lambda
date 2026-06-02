# DynamoDB Single Table Design

## 테이블 구조

### Table

- Table Name: `${DYNAMODB_TABLE}`
- Partition Key (PK): String
- Sort Key (SK): String

### Item Schema

| 필드 | 타입 | 예시 |
|--------|--------|--------|
| PK | String | `MEMO#01JBY7...` |
| SK | String | `METADATA` |
| user_id | String | `user123` |
| category | String | `basic`, `python` |
| content | String | `메모 내용` |
| created_at | String | `2026-06-02T09:00:00` |
| GSI1PK | String | `USER#user123` |
| GSI1SK | String | `2026-06-02T09:00:00` |
| GSI2PK | String | `USER#user123#CATEGORY#python` |
| GSI2SK | String | `2026-06-02T09:00:00` |

---

## 인덱스 설계

### GSI1

사용자별 전체 메모 조회를 위한 인덱스입니다.

| Key | Value |
|------|------|
| Partition Key | `USER#{user_id}` |
| Sort Key | `created_at` |

최신순으로 조회를 위해 `ScanIndexForward=False` 옵션을 사용하였습니다.

### GSI2

사용자별 카테고리 조회를 위한 인덱스입니다.

| Key | Value |
|------|------|
| Partition Key | `USER#{user_id}#CATEGORY#{category}` |
| Sort Key | `created_at` |

카테고리별 데이터를 Query로 조회할 수 있습니다.

---

## 액세스 패턴

### 메모 생성 / 수정 / 삭제

대상: Base Table

```text
PK = MEMO#{memo_id}
SK = METADATA
```

메모 ID를 기준으로 단건 조회 및 수정 및 삭제를 수행합니다.

### 사용자 전체 메모 조회

대상: GSI1

```text
GSI1PK = USER#{user_id}
```

사용자의 전체 메모를 최신순으로 조회합니다.

### 사용자 카테고리별 메모 조회

대상: GSI2

```text
GSI2PK = USER#{user_id}#CATEGORY#{category}
```

특정 카테고리의 메모를 최신순으로 조회합니다.

---

## 설계 의도

### 메모 단건 조회

메모 ID를 PK로 사용하여 단건 조회 및 수정, 삭제 시 Key 기반 조회가 가능하도록 설계하였습니다.

### 사용자별 조회

사용자별 메모 목록 조회를 위해 GSI1을 구성하였습니다.

사용자 단위로 파티션을 분리하여 다른 사용자의 데이터 규모에 영향을 받지 않고 조회할 수 있도록 하였습니다.

### 카테고리별 조회

카테고리별 조회를 위해 GSI2를 구성하였습니다.

별도 인덱스가 없다면 사용자의 전체 메모를 조회한 뒤 애플리케이션 레벨에서 카테고리를 필터링해야 합니다.

조회 패턴을 고려하여 카테고리 전용 인덱스를 추가하였습니다.

### 조회 제한

검색어가 없는 경우 Query에 `Limit`를 적용하여 불필요하게 많은 데이터를 읽어오는 상황을 방지하였습니다.

### 검색 처리

DynamoDB의 `contains()` 함수는 대소문자를 구분합니다.

대소문자 구분 없이 검색해야 하는 경우 Python 레벨에서 문자열을 소문자로 변환한 뒤 비교하도록 구현하였습니다.