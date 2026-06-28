---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
authors: ["Shunyu Yao", "Jeffrey Zhao", "Dian Yu", "Nan Du", "Izhak Shafran", "Karthik Narasimhan", "Yuan Cao"]
year: 2023
source: "ICLR 2023 (arXiv:2210.03629v3, Princeton University & Google Research Brain team)"
tags: [llm, agent, reasoning, acting, chain-of-thought, prompting, tool-use, hotpotqa, fever, alfworld, webshop, paper-card]
---

# 논문 전체 요약

LLM의 추론(chain-of-thought)과 행동(action plan 생성)은 그동안 별개 주제로 연구되어 왔는데, 이 논문은 **추론 흔적(reasoning trace)과 과업별 행동을 교차(interleave) 생성**시키는 프롬프팅 패러다임 ReAct를 제안한다. 추론은 행동 계획의 수립·추적·수정과 예외 처리를 돕고("reason to act"), 행동은 위키피디아 API나 환경 같은 외부 소스에서 추가 정보를 끌어와 추론을 접지(grounding)시킨다("act to reason"). PaLM-540B 기반 few-shot 프롬프팅만으로 HotpotQA·FEVER에서 CoT의 고질적 환각·오류 전파를 완화하고(최고 조합 ReAct+CoT-SC), ALFWorld·WebShop에서는 1~2개의 in-context 예시만으로 $10^3{\sim}10^5$ 개 과업 인스턴스로 학습한 모방학습/강화학습 베이스라인을 각각 절대 성공률 +34%p, +10%p 차이로 능가했다. 인간이 모델의 내부 지식과 외부 정보를 구분해 검사할 수 있어 해석가능성·신뢰성도 개선된다고 주장한다. (p.1)


### TL;DR

- LLM의 추론(chain-of-thought)과 행동(action plan 생성)은 그동안 별개 주제로 연구되어 왔는데, 이 논문은 **추론 흔적(reasoning trace)과 과업별 행동을 교차(interleave) 생성**시키는 프롬프팅 패러다임 ReAct를 제안한다.
- 아래 섹션의 수치, 그림, 표 장부를 원문 근거 단위로 확인한다.

### Why it matters

- 이 공개 예시 카드에서 논문의 방법, 결과, 한계, 그림·표 근거를 검토하기 위한 기본 요약 카드다.

### When to cite

- `ReAct: Synergizing Reasoning and Acting in Language Models`의 핵심 주장, 방법, 실험 결과, 또는 한계를 근거와 함께 인용해야 할 때 사용한다.

### Do not overclaim

- 카드에 명시된 원문 근거와 `해석` 콜아웃 밖으로 주장을 확장하지 않는다.
- 정량 비교는 아래 섹션이나 `그림·표 커버리지`에 적힌 수치가 있을 때만 사용한다.

### Limitations / Failure modes / Not settled by this paper

- 이 블록은 새 한계를 추가하지 않는다. 논문이 명시한 한계와 카드의 `해석` 콜아웃, `Limitations`, `Discussion`, `한계` 섹션을 우선 근거로 사용한다.
- 명시 근거가 없는 후속 해석은 원문 확인 전까지 보류한다.

---

## 1 Introduction

**핵심 주장**
- 인간 지능의 고유 특징은 과업 지향 행동과 언어적 추론(inner speech)의 매끄러운 결합이며, 이것이 자기조절·전략 수립·작업 기억 유지를 가능하게 한다 (요리 중 "물을 끓여야겠다", "소금이 없으니 간장으로" 같은 사고의 예).
- 기존 CoT 추론은 외부 세계에 접지되지 않은 **정적 블랙박스**라 사실 환각(fact hallucination)과 오류 전파에 취약하고, 반대로 기존 행동 생성 연구(SayCan, WebGPT 등)는 고수준 목표에 대한 추상적 추론이나 작업 기억 유지를 하지 않는다.
- ReAct는 추론과 행동을 교차 생성해 양쪽의 시너지를 얻는 일반 패러다임이며, 4개 벤치마크(HotpotQA, FEVER, ALFWorld, WebShop)에서 추론 전용/행동 전용 베이스라인을 일관되게 능가한다.

**근거·데이터 요약**
- **그림 1 (p.2)**: 2단 비교 패널. (1) HotpotQA 질문 "Apple Remote가 원래 상호작용하도록 설계된 프로그램을 제어할 수 있는 다른 기기는?"에 대해 — (1a) Standard는 "iPod"(오답), (1b) CoT는 "Apple TV → iPhone, iPad, iPod Touch"로 그럴듯하지만 환각된 추론, (1c) Act-only는 검색은 하지만 최종 종합에 실패, (1d) ReAct만 "Front Row 미디어 센터 → 키보드 기능 키"라는 정답에 도달. (2) ALFWorld "후추통을 서랍에 넣기" 과업에서 — (2a) Act-only는 sinkbasin에 후추통이 없는데도 "take peppershaker from sinkbasin"을 반복 환각하며 실패, (2b) ReAct는 "후추통은 cabinet이나 countertop에 있을 가능성이 높다"는 상식 추론 Think 액션으로 countertop 1에서 발견·성공.
- 기여 4가지: (1) ReAct 패러다임 제안, (2) 다양한 벤치마크에서 few-shot 우위 입증, (3) 추론 과업에서 행동의 중요성·결정 과업에서 추론의 중요성에 대한 체계적 절제 분석, (4) 프롬프팅 한계 분석과 초기 파인튜닝 실험. (p.2-3)

**원문 페이지**: p.1-3

---

## 2 ReAct: Synergizing Reasoning + Acting

**핵심 주장**
- 에이전트가 시점 $t$에 관측 $o_t \in \mathcal{O}$ 를 받고 정책 $\pi(a_t|c_t)$ ($c_t = (o_1, a_1, \cdots, o_{t-1}, a_{t-1}, o_t)$)로 행동 $a_t \in \mathcal{A}$ 를 내는 일반 설정에서, ReAct는 행동 공간을 언어 공간 $\mathcal{L}$ 을 더한 $\hat{\mathcal{A}} = \mathcal{A} \cup \mathcal{L}$ 로 확장한다.
- 언어 공간의 행동 $\hat{a}_t \in \mathcal{L}$ (= thought, 추론 흔적)은 환경에 영향을 주지 않고 관측 피드백도 없으며, 현재 문맥 $c_t$ 에 대한 추론으로 유용한 정보를 구성해 문맥을 $c_{t+1} = (c_t, \hat{a}_t)$ 로 갱신함으로써 이후 추론·행동을 지원한다.
- 언어 공간은 무한하므로 강한 언어 사전(prior)이 필요 — 본 논문은 frozen PaLM-540B를 few-shot in-context 예시(사람이 작성한 행동·생각·관측 궤적)로 프롬프팅한다. 추론 중심 과업은 생각-행동-관측을 빽빽하게 교대(dense thought), 행동이 많은 결정 과업은 생각을 궤적의 관련 위치에만 드물게(sparse thought) 배치하고 출현 시점은 모델이 스스로 정하게 한다.

**근거·데이터 요약**
- 유용한 생각의 유형 예: 목표 분해와 행동 계획 수립, 과업 관련 상식 주입, 관측에서 중요 부분 추출, 진행 상황 추적과 계획 전환, 예외 처리와 계획 수정 (그림 1의 각 위치로 예시). (p.3)
- ReAct의 4가지 특성: (A) 직관적 설계 — 주석자가 행동 위에 생각을 적기만 하면 되고 ad-hoc 포맷 설계 불필요, (B) 일반성·유연성 — QA/사실검증/텍스트 게임/웹 탐색 등 상이한 행동 공간에 적용, (C) 성능·강건성 — 1~6개 예시만으로 새 인스턴스에 일반화, 프롬프트 선택에 강건, (D) 인간 정렬·제어 가능 — 추론 흔적 검사 및 **생각 편집(thought editing)**으로 에이전트 행동을 즉석 교정 가능. (p.4)

**원문 페이지**: p.3-4

---

## 3 Knowledge-Intensive Reasoning Tasks

**핵심 주장**
- 멀티홉 QA(HotpotQA)와 사실 검증(FEVER)에서 ReAct는 Act-only를 일관되게 능가하며(추론이 행동을 유도하는 가치), CoT 대비로는 FEVER에서 우세(60.9 vs 56.3)·HotpotQA에서 소폭 열세(27.4 vs 29.4)다.
- ReAct는 사실적·접지된 반면 CoT는 추론 구조 수립에는 정확하나 환각에 취약 — 그래서 **내부 지식과 외부 지식을 결합한 ReAct + CoT-SC 전환 전략이 프롬프팅 최고 성능**이다.
- 파인튜닝 시 ReAct가 4개 방법 중 최강: 3,000개 부트스트랩 궤적만으로 PaLM-8B 파인튜닝 ReAct가 PaLM-62B 프롬프팅 전부를, 62B 파인튜닝이 540B 프롬프팅 전부를 능가한다.

**근거·데이터 요약**
- **설정 (3.1, p.4)**: 질문/주장만 입력받는 question-only 설정. 행동 공간은 단순 위키피디아 API 3종 — `search[entity]`(해당 페이지 첫 5문장 또는 유사 엔티티 top-5 제안), `lookup[string]`(문자열 포함 다음 문장, Ctrl+F 모사), `finish[answer]`. 의도적으로 SOTA 검색기보다 약하게 설계해 명시적 추론으로 검색하게 강제.
- **방법 (3.2, p.4-5)**: HotpotQA 6개·FEVER 3개 수작업 궤적을 few-shot 예시로 사용(더 늘려도 성능 향상 없음). 베이스라인은 ReAct 궤적에서 체계적 절제로 구성 — Standard(생각·행동·관측 모두 제거), CoT(행동·관측 제거; +온도 0.7로 21개 샘플링한 다수결 CoT-SC), Act(생각 제거). 결합 전략: ReAct→CoT-SC(HotpotQA 7스텝/FEVER 5스텝 내 미해결 시 CoT-SC로 후퇴), CoT-SC→ReAct(다수결 답이 $n/2$ 미만이면 ReAct로 후퇴). 파인튜닝은 STaR류 부트스트랩 — ReAct가 정답 낸 3,000개 궤적으로 PaLM-8/62B를 학습.
- **표 1 (p.5)** — PaLM-540B 프롬프팅 결과 (HotpotQA EM / FEVER Acc):
  | 방법 | HotpotQA (EM) | FEVER (Acc) |
  |---|---|---|
  | Standard | 28.7 | 57.1 |
  | CoT | 29.4 | 56.3 |
  | CoT-SC | 33.4 | 60.4 |
  | Act | 25.7 | 58.9 |
  | ReAct | 27.4 | 60.9 |
  | CoT-SC → ReAct | 34.2 | **64.6** |
  | ReAct → CoT-SC | **35.1** | 62.0 |
  | 지도학습 SoTA | 67.5 | 89.5 |
- **그림 2 (p.5)**: CoT-SC 샘플 수(x축 0~21)에 따른 성능. 좌측 HotpotQA EM(y축 약 26~35), 우측 FEVER Acc(y축 47.5~65.0). ReAct·CoT는 샘플 수와 무관한 수평선, CoT-SC는 샘플 수에 따라 상승하나, 두 결합 방법(CoT-SC→ReAct, ReAct→CoT-SC)이 전 구간에서 CoT-SC를 일관되게 상회하며 **3~5개 샘플만으로 21샘플 CoT-SC 성능에 도달**.
- **표 2 (p.6)** — 성공·실패 유형 인간 분석(ReAct·CoT 각각 정답/오답 궤적 50개씩, 총 200개 수동 라벨링):
  | 구분 | 유형 | ReAct | CoT |
  |---|---|---|---|
  | 성공 | 참 양성(올바른 추론+사실) | 94% | 86% |
  | 성공 | 거짓 양성(환각인데 정답) | 6% | 14% |
  | 실패 | 추론 오류(반복 루프 포함) | 47% | 16% |
  | 실패 | 검색 결과 오류 | 23% | – |
  | 실패 | 환각 | **0%** | **56%** |
  | 실패 | 라벨 모호성 | 29% | 28% |
  핵심 관찰: (A) CoT의 최대 실패 모드는 환각(56%), ReAct는 환각 0%로 접지·신뢰성 우위. (B) 단, 교차 구조 제약이 추론 유연성을 깎아 ReAct의 추론 오류율이 더 높고, 직전 생각·행동을 반복 생성하는 루프 패턴이 빈발(저자들은 greedy 디코딩 탓으로 추정). (C) 비정보적 검색(오류의 23%)이 추론을 탈선시킴 — 이것이 두 방법 결합의 동기.
- **그림 3 (p.7)**: HotpotQA 스케일링. 두 패널(learning=prompt / finetune), x축 모델 크기(8b/62b/540b), y축 HotpotQA EM(0~30+), 4개 방법(Standard, CoT, Act, ReAct) 막대. 프롬프팅 패널에서는 8B/62B에서 ReAct가 4개 중 최하(in-context로 추론+행동 동시 학습이 어려움), 모든 방법이 크기에 따라 상승. 파인튜닝 패널에서는 ReAct가 최강으로 역전 — 8B 파인튜닝 ReAct > 62B 모든 프롬프팅, 62B 파인튜닝 ReAct > 540B 모든 프롬프팅. Standard/CoT 파인튜닝은 (잠재적 환각) 지식 암기를 가르치는 반면 ReAct/Act 파인튜닝은 위키피디아 접근이라는 일반화 가능한 기술을 가르치므로 격차가 큼.

> [!note] 해석
> 표 1에서 ReAct 단독은 CoT-SC조차 못 이기며(34.2 vs 27.4), 지도학습 SoTA(67.5)와의 격차는 두 배 가까이 된다. 이 논문의 실질 기여는 "ReAct가 QA 성능을 올렸다"가 아니라 (1) 환각 0%라는 접지 특성, (2) 내부/외부 지식 전환 휴리스틱, (3) 파인튜닝 시 역전이라는 세 가지 구조적 발견으로 읽는 것이 정확하다. 또한 표 2는 무작위 50개씩의 수동 분석이라 표본이 작다.

**원문 페이지**: p.4-7

---

## 4 Decision Making Tasks

**핵심 주장**
- ALFWorld(텍스트 가정환경 게임)와 WebShop(실제 상품 기반 쇼핑 환경)에서 1~2-shot ReAct가 $10^3{\sim}10^5$ 개 인스턴스로 학습한 모방/강화학습을 능가 — 최고 ReAct 시도는 ALFWorld 성공률 71%로 최고 Act(45%)·BUTLER(37%)를 압도하고, 최악 ReAct 시도(48%)조차 두 방법의 최고 시도를 이긴다.
- 희소(sparse) 추론만으로도 행동 전용 대비 일관 우위: ALFWorld 6개 통제 시도 전부에서 ReAct > Act (상대 이득 33~90%, 평균 62%).
- Inner Monologue(IM)식 "환경 피드백 재진술"은 진짜 내부 추론이 아니다 — IM식 절제(ReAct-IM)는 ReAct에 크게 뒤져(전체 53 vs 71), 고수준 목표 분해·상식적 위치 추론의 가치를 입증한다.

**근거·데이터 요약**
- **ALFWorld 설정 (p.7)**: 6개 과업 유형(Pick, Clean, Heat, Cool, Look, Pick 2), 134개 미공개 평가 게임. 인스턴스당 50개 이상 장소·전문가 정책 기준 50스텝 이상 — 계획·하위목표 추적·체계적 탐색 요구. 과업 유형별 3개 궤적에 (1) 목표 분해, (2) 하위목표 완료 추적, (3) 다음 하위목표 결정, (4) 물건 위치 상식 추론의 희소 생각을 주석. 3개 중 2개씩 뽑은 순열로 6개 프롬프트를 만들어 강건성 평가. 베이스라인 BUTLER는 과업당 $10^5$ 전문가 궤적으로 학습한 모방학습.
- **표 3 (p.8)** — ALFWorld 과업별 성공률(%):
  | 방법 | Pick | Clean | Heat | Cool | Look | Pick 2 | 전체 |
  |---|---|---|---|---|---|---|---|
  | Act (best of 6) | 88 | 42 | 74 | 67 | 72 | 41 | 45 |
  | ReAct (avg) | 65 | 39 | 83 | 76 | 55 | 24 | 57 |
  | ReAct (best of 6) | **92** | 58 | **96** | 86 | **78** | **41** | **71** |
  | ReAct-IM (avg) | 55 | 59 | 60 | 55 | 23 | 24 | 48 |
  | ReAct-IM (best of 6) | 62 | **68** | 87 | 57 | 39 | 33 | 53 |
  | BUTLERg (best of 8) | 33 | 26 | 70 | 76 | 17 | 12 | 22 |
  | BUTLER (best of 8) | 46 | 39 | 74 | **100** | 22 | 24 | 37 |
  (BUTLER만 beam search, 나머지는 greedy. ReAct는 6과업 중 5개에서 ReAct-IM에 우세.) Act는 생각이 없어 목표의 하위목표 분해와 환경 상태 추적에 실패.
- **WebShop 설정 (p.7-8)**: 118만 개 실제 상품·1.2만 개 인간 지시문. 노이즈 많은 비/반구조 텍스트(아마존 크롤링 제목·설명·옵션)에서 지시문에 맞는 상품을 검색·옵션 선택·구매. 평가는 500개 테스트 지시문에 대한 평균 점수(선택 상품이 원하는 속성을 덮는 비율)와 성공률(모든 요건 충족 비율). 1-shot Act 대비 ReAct는 "무엇을 탐색할지·언제 살지·어떤 옵션이 관련 있는지" 추론을 추가.
- **표 4 (p.8)** — WebShop 점수/성공률(SR):
  | 방법 | Score | SR |
  |---|---|---|
  | Act | 62.3 | 30.1 |
  | ReAct | **66.6** | **40.0** |
  | IL (인간 궤적 1,012개) | 59.9 | 29.1 |
  | IL+RL (+지시문 10,587개) | 62.4 | 28.7 |
  | 인간 전문가 | 82.1 | 59.6 |
  1-shot Act가 이미 IL/IL+RL과 대등하고, ReAct는 종전 최고 성공률 대비 절대 +10%p. 단 인간 전문가(59.6)와는 큰 격차 — 인간이 하는 다양한 상품 탐색·질의 재구성이 프롬프팅에는 여전히 어렵다.
- **내부 추론 vs 외부 피드백 (p.8)**: ReAct는 LLM의 추론+행동 결합을 폐루프(closed-loop) 상호작용 환경에 적용한 최초 사례라고 주장. 가장 가까운 선행 연구 Inner Monologue는 "내적 독백"이 환경 상태 관측과 목표 충족 요건의 재진술에 한정. 같은 전문가 궤적에 IM식 빽빽한 외부 피드백 생각만 재주석한 ReAct-IM 절제 결과(표 3), 하위목표 완료 시점 판단·다음 하위목표 결정·상식적 물건 위치 추론 실패가 빈발.

> [!note] 해석
> 표 3에서 ReAct-IM의 평균(48)이 Act 최고(45)와 비슷한 수준이라는 점이 흥미롭다 — 생각의 "존재"가 아니라 생각의 "종류"(목표 분해·상식 추론 같은 내부 추론)가 성능을 만든다는 것이 이 절의 실질적 절제 결론이다. 또한 ALFWorld 평가는 134개 게임·6개 프롬프트라 분산이 크고(avg와 best-of-6 격차 14%p), WebShop은 단일 프롬프트 결과로 보인다.

**원문 페이지**: p.6-8

---

## 5 Related Work

**핵심 주장**
- 추론 계열: CoT, least-to-most, zero-shot CoT, self-consistency, Selection-Inference, STaR, Faithful reasoning, Scratchpad 등은 모두 **고립된·고정된 추론**이며, ReAct는 행동과 관측을 추론 입력 스트림에 통합해 추론을 넘어선 과업(상호작용 결정)까지 다룬다는 점에서 다르다.
- 결정 계열: WebGPT는 브라우저와 상호작용하지만 사고·추론 절차를 명시적으로 모델링하지 않고 비싼 인간 피드백 RL에 의존; BlenderBot·Sparrow·SimpleTOD도 API 호출 결정을 학습하지만 추론 절차가 없고 대규모 데이터셋·인간 피드백이 필요. ReAct는 추론 절차의 언어 기술만 요구하므로 훨씬 저렴한 정책 학습이다.
- SayCan(어포던스 모델로 행동 재순위화)·Inner Monologue(환경 피드백 주입)가 가장 근접하나, IM의 독백은 진짜 내부 사고가 아니라는 것이 4절 절제의 논점.

**근거·데이터 요약**
- CoT 효과의 요인 분석(Madaan & Yazdanbakhsh 2022 — 기호·패턴·텍스트의 존재가 핵심), 언어를 의미 풍부한 입력으로 쓰는 상호작용 연구들(Abramson 2020, Karamcheti 2021, Huang 2022a, Li 2022), 제너럴리스트 에이전트(Gato/Reed 2022) 인용으로 위치 설정. (p.9)

**원문 페이지**: p.9

---

## 6 Conclusion

**핵심 주장**
- ReAct는 단순하지만 효과적인 추론+행동 시너지 방법으로, 멀티홉 QA·사실 검증·상호작용 결정 과업에서 해석 가능한 결정 흔적과 함께 우수한 성능을 보인다.
- 한계: 행동 공간이 큰 복잡한 과업은 더 많은 시연이 필요한데 in-context 학습의 입력 길이 제한을 쉽게 초과한다 — HotpotQA 파인튜닝의 초기 유망 결과를 제시했으며, 고품질 인간 주석 데이터 학습이 향후 과제.
- 멀티태스크 학습으로 확장하고 강화학습 같은 보완 패러다임과 결합하면 더 강한 에이전트로 발전 가능하다고 전망.

**근거·데이터 요약**
- 재현성: 주 실험은 비공개 모델 PaLM 기반이므로, 전체 프롬프트(부록 C)·GPT-3 추가 실험(부록 A.1)·GPT-3 ReAct 코드 공개로 보완. 윤리 진술: LLM을 외부 환경에 연결하는 것의 위험(부적절한 정보 조회, 유해 행동)을 인지하고 실험을 위키피디아·WebShop 벤치마크로 한정(실제 구매·편집 불가). (p.10)

**원문 페이지**: p.9-10

---

## Appendix 하이라이트

**핵심 주장**
- (A.1) ReAct 프롬프팅은 모델 일반적: GPT-3(text-davinci-002)가 PaLM-540B를 두 과업 모두에서 능가 — 지시문 파인튜닝의 효과 추정.
- (A.2–A.3) 행동에 의한 접지의 부수 효과 두 가지: 최신 지식 획득(오래된 데이터셋 라벨을 넘어서는 답), 그리고 생각 편집만으로 가능한 인간 개입(human-in-the-loop) 행동 교정.
- (E.1) 본문 표 2의 성공·실패 유형별 실제 사례 제공 — CoT 환각의 전형과 ReAct 검색 실패·라벨 모호성의 전형.

**근거·데이터 요약**
- **표 5 (p.14)** — PaLM-540B vs GPT-3(greedy): HotpotQA EM 29.4 vs **30.8**(500개 검증 질문 표본), ALFWorld 성공률 70.9% vs **78.4%**(134개 전체, PaLM 기준 최적 프롬프트 사용).
- **그림 4 (p.14)**: 라벨이 낡은 HotpotQA 사례 — "Cirque du Soleil 쇼 Mystère가 열리는 호텔의 객실 수는?"에서 데이터셋 라벨은 2,664(구식). Standard는 3,000, CoT는 "Treasure Island에 2,885실" 환각, Act-only는 답 없이 종료. ReAct만 검색 체인(Mystère → Treasure Island Hotel and Casino)으로 "2,884 rooms and 220 suites" 관측을 얻어 합산 **Finish[3,104]**라는 최신 정보 기반 답을 냄.
- **그림 5 (p.15)**: ALFWorld "키체인 2개를 금고에 넣기" 과업의 인간 개입 사례. (a) 원 궤적은 Act 17의 환각된 생각("두 번째 키체인을 drawer 2에서 찾을 수 있다") 탓에 실패. (b) 인간이 생각 2개(Act 17의 환각 문장 제거, Act 23에 "dresser 등을 볼 것" 힌트 추가)만 편집하자 dresser에서 두 번째 키체인을 찾아 성공. 수십 개 행동을 타이핑하는 대신 생각 몇 줄 편집으로 정책을 즉석 수정 — 모델 파라미터를 못 바꾸는 Act/RL 방식에선 어려운 새로운 인간-기계 협업 형태라고 주장.
- **B.1 파인튜닝 세부 (p.15)**: 배치 64; PaLM-8B는 ReAct/Act 4,000스텝·Standard/CoT 2,000스텝, PaLM-62B는 ReAct/Act 4,000스텝·Standard/CoT 1,000스텝 — ReAct/Act는 데이터·스텝이 늘수록 개선, Standard/CoT는 곧 열화.
- **B.2 + 표 9 (p.15, 25)**: ReAct-IM은 같은 전문가 궤적에 "현재 목표 분해"와 "현재 하위목표"만 재진술하는 빽빽한 IM식 생각을 주석한 것 — 하위목표 완료 판단, 다음 하위목표 결정, 사전학습 상식 활용(물건 위치)이 결여됨.
- **C 프롬프트 전문 (p.16-25)**: HotpotQA 6개 예시(원 질문·CoT·Act·ReAct 형태 병기), FEVER 3개, WebShop(표 6: Act는 `search[...]`/`click[...]`, ReAct는 `think[...]` 추가), ALFWorld(표 7 Act / 표 8 ReAct / 표 9 ReAct-IM — 동일한 clean 과업으로 세 형식 대비).
- **D 궤적 사례 (p.25-31)**: FEVER에서 ReAct가 검색 관측("2007년 미국 영화")으로 라벨 REFUTES를 맞히는 반면 CoT는 내부 지식으로 SUPPORTS 오답(예제 3208). ALFWorld 동일 게임에서 ReAct는 칼을 찾아 씻어 배치 성공, Act는 동일 행동 반복 환각, ReAct-IM은 "I need to find a clean knife"라는 생각에 속아 씻지 않고 배치 시도 후 루프에 갇힘. **표 10 (p.31)**: WebShop 동일 지시문("사과 시나몬 동결건조 바나나칩 16팩, $50 미만")에서 Act는 속성 무시 클릭으로 점수 0.125, ReAct는 `think`로 옵션('apple cinnamon', '0.53 ounce (pack of 16)')을 대조 확인해 점수 1.0.
- **E.1 사례 (p.32-33)**: 성공-거짓양성(ReAct가 근거 없이 "San Marco가 먼저"라 답하고 정답 처리), 실패-검색 오류(goddess frigg 검색 실패 후 표류), 실패-환각(CoT가 "1916"을 지어냄, 라벨 1909), 실패-라벨 모호성(ReAct가 "Israeli" 답변, 라벨은 "Israel-American").

> [!note] 해석
> 부록 A.2·A.3은 이후 에이전트 연구에서 표준이 된 두 주제 — 도구 사용에 의한 지식 최신성 확보, 사고 사슬 개입에 의한 조종성(steerability) — 의 초기 시연이다. 다만 둘 다 단일 사례 기반의 정성적 시연이며 정량 평가는 없다. GPT-3 우위(표 5)는 이후 "지시문 튜닝이 에이전트 능력의 전제"라는 통념의 근거로 자주 인용된다.

**원문 페이지**: p.14-33

---

## 그림·표 커버리지

- 원문(텍스트 휴리스틱 추출): Figure 1-5 / Table 1-10
- 카드에서 언급 확인: Figure 1-5 / Table 1-10
- 미확인 항목 없음
- (기계 백필 장부 — 휴리스틱 기반이므로 심층 감사 시 갱신)
