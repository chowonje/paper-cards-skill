---
title: "{{title}}"
authors: []
year: {{year}}
source: "TODO: verify source from the PDF first page"
tags: [paper-card]
---

# {{title}}

> Reader Card: 먼저 읽기 쉬운 요약과 핵심 구조를 쓴다. 자세한 검증 근거는 아래 `# Evidence Appendix`에 분리한다.

## 한 문단 요약

TODO: 논문 전체를 처음 읽는 사람이 이해할 수 있게 한 문단으로 요약한다. 긴 원문 인용 없이 작성하고, 상세 근거는 아래 Evidence Appendix로 보낸다.

## 핵심 아이디어

- TODO
- TODO
- TODO

## 수식으로 보는 핵심

TODO: 수식이 핵심이면 짧은 block math나 `../{{equations_dir_relpath}}/<name>.svg` 링크를 사용한다. 긴 inline LaTeX를 문장 안에 넣지 않는다.

## 왜 중요한가

- TODO

## 기억할 수치

| 항목 | 값 | 의미 |
|---|---:|---|
| TODO | TODO | TODO |

## 그림·표 한눈에 보기

- TODO: 중요한 Figure/Table만 독자용으로 1-2문장씩 설명한다. 축, 추세, 수치의 상세 감사 내용은 Evidence Appendix에 쓴다.

## 한계와 조심할 점

- TODO

---

# Evidence Appendix

## 문서 신원

- 제목 확인: TODO
- 저자 확인: TODO
- 출처/버전 확인: TODO
- 판독 범위: TODO

## 핵심 주장별 근거

### Claim 1

**저자 주장**
- TODO

**근거·데이터**
- TODO

**원문 페이지**: pdf p.N

> [!note] 해석
> TODO: 필요한 경우에만 연구자 해석을 저자 주장과 분리한다.

## 수식 근거

### Equation 1

**원문 페이지**: pdf p.N

```latex
TODO
```

- 의미: TODO
- 본문 표시 방식: TODO

## 그림·표 근거

### Figure/Table Coverage Ledger

| 원문 항목 | 원문 페이지 | 본문 포함 | Appendix 설명 상태 |
|---|---:|---|---|
| Figure TODO | pdf p.N | TODO | TODO |
| Table TODO | pdf p.N | TODO | TODO |

### Figure TODO

- 패널/축/범례: TODO
- 추세/대표 수치: TODO
- 불확실성: TODO

### Table TODO

- 비교 구조: TODO
- 핵심 행/열: TODO
- 불확실성: TODO

## QA 메모

- PDF 물리 페이지 번호 사용 여부: TODO
- Figure/Table 누락 여부: TODO
- 긴 원문 인용 제거 여부: TODO
- 수식 LaTeX 보존 여부: TODO
- Reader Card와 Evidence Appendix 균형 확인: TODO
- 제목/저자/핵심 수치 visual spot-check 여부: TODO
- 성능 주장 범위와 그림 축/단위 확인 여부: TODO
- 수동 리뷰 상태: review candidate / WARN / PASS 중 하나로 기록
