---
title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
authors: ["Patrick Lewis", "Ethan Perez", "Aleksandra Piktus", "Fabio Petroni", "Vladimir Karpukhin", "Naman Goyal", "Heinrich Küttler", "Mike Lewis", "Wen-tau Yih", "Tim Rocktäschel", "Sebastian Riedel", "Douwe Kiela"]
year: 2020
source: "NeurIPS 2020 (arXiv:2005.11401v4, 2021-04-12 갱신판)"
tags: [retrieval-augmented-generation, rag, dpr, bart, open-domain-qa, fact-verification, non-parametric-memory, seq2seq, paper-card]
---

# 논문 전체 요약

사전학습 seq2seq 모델(BART, 파라미터 기반 메모리)과 위키피디아 밀집 벡터 인덱스(DPR 리트리버로 접근하는 비파라미터 메모리)를 결합해 끝까지(end-to-end) 미세조정하는 범용 레시피인 **RAG(Retrieval-Augmented Generation)**를 제안한다. 검색된 문서를 잠재 변수로 취급해 주변화(marginalize)하는 두 가지 정식화 — 출력 시퀀스 전체가 같은 문서를 쓰는 RAG-Sequence와 토큰마다 다른 문서를 쓸 수 있는 RAG-Token — 를 비교하며, 오픈도메인 QA 4개 벤치마크(NQ, TriviaQA, WebQuestions, CuratedTrec)에서 당시 최고 성능을 경신하고, 생성 과제(MS-MARCO, Jeopardy 질문 생성)에서는 BART 단독 대비 더 사실적·구체적·다양한 텍스트를 생성함을 보였다. FEVER 사실 검증에서는 검색 감독 없이 SotA 파이프라인 대비 4.3% 이내 성능을 달성했고, 문서 인덱스 교체만으로 모델 지식을 갱신할 수 있음(인덱스 핫스왑)을 시연했다. (p.1)


### TL;DR

- 사전학습 seq2seq 모델(BART, 파라미터 기반 메모리)과 위키피디아 밀집 벡터 인덱스(DPR 리트리버로 접근하는 비파라미터 메모리)를 결합해 끝까지(end-to-end) 미세조정하는 범용 레시피인 **RAG(Retrieval-Augmented Generation)**를 제안한다.
- 아래 섹션의 수치, 그림, 표 장부를 원문 근거 단위로 확인한다.

### Why it matters

- 이 공개 예시 카드에서 논문의 방법, 결과, 한계, 그림·표 근거를 검토하기 위한 기본 요약 카드다.

### When to cite

- `Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks`의 핵심 주장, 방법, 실험 결과, 또는 한계를 근거와 함께 인용해야 할 때 사용한다.

### Do not overclaim

- 카드에 명시된 원문 근거와 `해석` 콜아웃 밖으로 주장을 확장하지 않는다.
- 정량 비교는 아래 섹션이나 `그림·표 커버리지`에 적힌 수치가 있을 때만 사용한다.

### Limitations / Failure modes / Not settled by this paper

- 이 블록은 새 한계를 추가하지 않는다. 논문이 명시한 한계와 카드의 `해석` 콜아웃, `Limitations`, `Discussion`, `한계` 섹션을 우선 근거로 사용한다.
- 명시 근거가 없는 후속 해석은 원문 확인 전까지 보류한다.

---

## 1 Introduction

**핵심 주장**
- 사전학습 LM은 파라미터 안에 사실 지식을 암묵적 지식베이스로 저장하지만, 메모리의 확장·수정이 어렵고 예측 근거(provenance) 제시가 안 되며 "환각(hallucination)"을 만든다.
- REALM·ORQA 같은 기존 하이브리드(파라미터+검색) 모델은 추출형(extractive) 오픈도메인 QA에만 국한되었다 — 본 논문은 이를 "NLP의 일꾼"인 seq2seq 생성 모델로 확장한다.
- 파라미터/비파라미터 메모리 모두 사전학습·사전적재된 상태에서 시작하므로, 추가 학습 없이도 지식 접근 능력이 갖춰져 있다는 점이 과제별로 처음부터 학습하는 기존 메모리 아키텍처(메모리 네트워크 등)와의 결정적 차이다.

**근거·데이터 요약**
- 구성: 리트리버는 DPR(Dense Passage Retriever), 생성기는 BART. top-K 근사로 잠재 문서를 주변화하되, 출력 단위(시퀀스당 같은 문서) 또는 토큰 단위(토큰마다 다른 문서)의 두 방식을 둔다. (p.1-2)
- **그림 1 (p.2)**: 접근법 개요 다이어그램. 왼쪽에서 질의 $x$ (예: QA "define middle ear", 사실검증 "Barack Obama was born in Hawaii.", Jeopardy 생성 "The Divine Comedy")가 Query Encoder $q(x)$로 인코딩되고, MIPS(최대내적탐색)로 문서 인덱스에서 top-K 문서 $z_1 \ldots z_4$를 찾은 뒤, 생성기 $p_\theta$(파라미터 메모리)가 각 문서를 조건으로 출력을 생성하고 주변화(Margin-alize)해 최종 $y$를 낸다 (예: "The middle ear includes the tympanic cavity and the three ossicles.", "supports", Jeopardy 질문 문장). 역전파는 $q$와 $p_\theta$를 관통해 end-to-end로 흐른다.
- 결과 요약(서론 선언): NQ·WQ·CuratedTrec SotA, TriviaQA에서 특화 사전학습 기법 능가, MS-MARCO·Jeopardy에서 BART보다 사실적·구체적·다양, FEVER는 SotA 파이프라인 대비 4.3% 이내, 그리고 비파라미터 메모리 교체로 지식 갱신 가능. 코드는 HuggingFace Transformers에 공개. (p.1-2)

> [!note] 해석
> 이 논문이 "RAG"라는 용어의 원전이다. 이후 업계에서 통용되는 RAG(프롬프트에 검색 결과를 붙이는 파이프라인)와 달리, 원래의 RAG는 리트리버까지 함께 미세조정되는 확률적 잠재변수 모델이라는 점이 자주 잊힌다 — 검색 분포 $p_\eta(z|x)$로 생성 확률을 주변화한다는 정식화가 핵심 기여다.

**원문 페이지**: p.1-2

---

## 2 Methods

**핵심 주장**
- 입력 $x$로 텍스트 문서 $z$를 검색하고 이를 추가 문맥으로 삼아 목표 시퀀스 $y$를 생성한다. 문서는 직접 감독 없이 잠재 변수로 취급되어 주변화된다.
- RAG-Sequence는 시퀀스 전체에 같은 문서 하나를, RAG-Token은 토큰마다 다른 문서를 허용한다 — 후자는 여러 문서의 내용을 조합한 답을 만들 수 있다.
- 학습 시 문서 인코더(와 인덱스)는 고정하고 질의 인코더 $\text{BERT}_q$와 BART 생성기만 미세조정해도 충분하다 — REALM처럼 인덱스를 주기적으로 재구축하는 비용을 피한다.

**근거·데이터 요약**
- **2.1 두 모델** (p.3): 수식 보존 —
$$p_{\text{RAG-Sequence}}(y|x) \approx \sum_{z \in \text{top-}k(p(\cdot|x))} p_\eta(z|x)\, p_\theta(y|x,z) = \sum_{z \in \text{top-}k(p(\cdot|x))} p_\eta(z|x) \prod_i^N p_\theta(y_i|x,z,y_{1:i-1})$$
$$p_{\text{RAG-Token}}(y|x) \approx \prod_i^N \;\sum_{z \in \text{top-}k(p(\cdot|x))} p_\eta(z|x)\, p_\theta(y_i|x,z,y_{1:i-1})$$
  목표가 길이 1인 분류 과제에서는 두 정식화가 동치다.
- **2.2 리트리버 DPR** (p.3): 바이인코더 구조 — $p_\eta(z|x) \propto \exp\left(\mathbf{d}(z)^{\top}\mathbf{q}(x)\right)$, $\mathbf{d}(z)=\text{BERT}_d(z)$, $\mathbf{q}(x)=\text{BERT}_q(x)$ (둘 다 BERT-BASE). top-k 계산은 MIPS 문제로 준선형 시간에 근사 해결. TriviaQA/NQ로 학습된 DPR 사전학습 바이인코더로 리트리버와 인덱스를 초기화하며, 이 문서 인덱스를 비파라미터 메모리라 부른다.
- **2.3 생성기 BART** (p.3): BART-large(400M 파라미터) 사용, 입력 $x$와 검색 문서 $z$는 단순 연결(concatenate). BART 파라미터 $\theta$가 파라미터 메모리.
- **2.4 학습** (p.3-4): 어떤 문서를 검색해야 하는지에 대한 직접 감독 없이, 목표의 음의 주변 로그우도 $\sum_j -\log p(y_j|x_j)$를 Adam SGD로 최소화.
- **2.5 디코딩** (p.4): RAG-Token은 전이 확률 $p'_\theta(y_i|x, y_{1:i-1}) = \sum_{z \in \text{top-}k(p(\cdot|x))} p_\eta(z_i|x)\, p_\theta(y_i|x, z_i, y_{1:i-1})$ 을 표준 빔 디코더에 꽂으면 된다. RAG-Sequence는 우도가 토큰별로 분해되지 않으므로 문서별로 빔 서치를 돌린 후, 후보 $y$가 등장하지 않은 문서에 대해 추가 순전파를 돌려 주변화하는 "Thorough Decoding", 또는 빔에 없으면 $p_\theta(y|x,z_i)\approx 0$으로 근사하는 "Fast Decoding"을 쓴다.

> [!note] 해석
> "문서 인코더 고정, 질의 인코더만 학습"은 공학적 타협이지만 결과적으로 RAG 실용화의 핵심 설계가 됐다 — 인덱스 재구축 없이 fine-tuning이 가능해진다. 반면 검색 분포가 DPR 초기화(NQ/TriviaQA 감독)에 크게 의존하므로, 완전한 비감독 검색 학습이라고 보기는 어렵다.

**원문 페이지**: p.2-4

---

## 3 Experiments

**핵심 주장**
- 모든 과제에 단일 비파라미터 지식원을 사용한다: 2018년 12월 위키피디아 덤프를 100단어 단위 청크로 잘라 2,100만 문서를 만들고, FAISS + HNSW 근사로 단일 MIPS 인덱스를 구축한다.
- 과제 4종으로 평가: 오픈도메인 QA(추출이 아닌 생성으로), 추상적 QA(MS-MARCO를 골드 패시지 없이), Jeopardy 질문 생성(지식 집약적 생성), FEVER 사실 검증(검색 감독 없는 분류).
- 학습 시 top-$k \in \{5, 10\}$ 문서를 검색하고, 테스트용 $k$는 dev 데이터로 결정한다.

**근거·데이터 요약**
- **3.1 오픈도메인 QA** (p.4): NQ, TriviaQA(TQA), WebQuestions(WQ), CuratedTrec(CT) 4개 데이터셋, Exact Match(EM) 평가. 답을 입출력 텍스트 쌍으로 보고 음의 로그우도를 직접 최소화. WQ/CT는 작아서 NQ로 학습한 RAG 모델로 초기화. TQA는 T5와 비교 위해 TQA-Wiki 테스트셋도 별도 평가. 비교 대상: 추출형 QA(REALM, DPR)와 "Closed-Book QA"(T5; 검색 없이 파라미터 지식만으로 생성).
- **3.2 추상적 QA** (p.4-5): MSMARCO NLG v2.1을 골드 패시지 없이 질문·답만 사용해 오픈도메인 추상적 QA로 변환. "What is the weather in Volcano, CA?"처럼 골드 패시지 없이는 답할 수 없는 질문, 위키피디아만으로 답할 수 없는 질문이 존재해 성능 상한이 깎인다 — 이런 경우 RAG는 파라미터 지식에 의존.
- **3.3 Jeopardy 질문 생성** (p.5): 답 엔티티에서 그 엔티티에 관한 정밀한 사실 문장(Jeopardy 질문)을 생성하는 까다로운 과제. SearchQA 분할(학습 100K/개발 14K/테스트 27K), 엔티티 매칭에 가중치를 둔 Q-BLEU-1 지표 + 인간 평가 2종(사실성, 구체성)을 쌍대 비교(pairwise)로 수행. 비교용 BART 모델도 학습.
- **3.4 사실 검증** (p.5): FEVER 클래스 라벨(supports/refutes/not enough info)을 단일 출력 토큰으로 매핑해 claim-class 쌍으로 학습. 대부분의 기존 접근과 달리 **검색된 증거에 대한 감독을 쓰지 않는다.** 3-way와 2-way(Thorne & Vlachos 설정) 두 변형, 라벨 정확도로 보고.

**원문 페이지**: p.4-5

---

## 4 Results

**핵심 주장**
- 오픈도메인 QA 4개 모두에서 새 SotA 달성 — 재랭커나 추출형 리더 없이도 가능하며, 답이 검색 문서에 그대로(verbatim) 없어도 생성으로 맞출 수 있다(그런 경우 NQ에서 11.8% 정확도; 추출형이라면 0%).
- 생성 과제에서 RAG는 BART보다 환각이 적고, 더 사실적·구체적·다양하다 — 인간 평가에서 사실성 우위(RAG 42.7% vs BART 7.1%).
- 학습된 검색은 모든 과제에 도움이 되며(고정 리트리버·BM25 대비), 인덱스 교체만으로 세계 지식을 갱신할 수 있다.

**근거·데이터 요약**
- **표 1 (p.6)** — 오픈도메인 QA 테스트 EM (TQA 좌측=표준 테스트, 우측=TQA-Wiki 테스트):
  | 모델 | NQ | TQA | WQ | CT |
  |---|---|---|---|---|
  | T5-11B (closed-book) | 34.5 | - /50.1 | 37.4 | - |
  | T5-11B+SSM (closed-book) | 36.6 | - /60.5 | 44.7 | - |
  | REALM | 40.4 | - / - | 40.7 | 46.8 |
  | DPR | 41.5 | 57.9/ - | 41.1 | 50.6 |
  | RAG-Token | 44.1 | 55.2/66.1 | 45.5 | 50.0 |
  | **RAG-Sequence** | **44.5** | 56.8/**68.0** | 45.2 | **52.2** |
  REALM·T5+SSM처럼 비싼 "salient span masking" 사전학습 없이 이 성능을 달성. (p.5-6)
- **표 2 (p.6)** — 생성·분류 테스트 점수 (Jeopardy: B-1/QB-1, MSMARCO: R-L/B-1, FEVER: 라벨 정확도):
  | 모델 | Jeopardy B-1/QB-1 | MSMARCO R-L/B-1 | FVR3 | FVR2 |
  |---|---|---|---|---|
  | SotA | - | 49.8*/49.9* | 76.8 | 92.2* |
  | BART | 15.1/19.7 | 38.2/41.6 | 64.0 | 81.1 |
  | RAG-Token | **17.3/22.2** | 40.1/41.5 | 72.5 | 89.5 |
  | RAG-Sequence | 14.7/21.4 | **40.8/44.2** | 72.5 | 89.5 |
  (*는 골드 문맥/증거 사용.) RAG-Sequence는 MSMARCO에서 BART 대비 Bleu +2.6, Rouge-L +2.6. FEVER 3-way는 SotA 대비 4.3% 이내, 2-way는 골드 증거를 받는 RoBERTa 대비 2.7% 이내 — RAG는 claim만 받고 증거를 스스로 검색. 검색-증거 일치 분석: top-1 검색 문서가 골드 문서인 비율 71%, top-10 안에 골드 문서가 있는 비율 90%. (p.6-7)
- **그림 2 (p.7)**: 입력 "Hemingway"에 대한 Jeopardy 생성 시 RAG-Token의 문서 사후확률 $p(z_i|x, y_i, y_{-i})$ 히트맵. x축은 생성 토큰 열("This novel by ... "The Sun Also Rises" ... "A Farewell to Arms""), y축은 검색 문서 5개. "A Farewell to Arms"를 언급한 문서 1의 사후확률이 해당 책 제목 생성 시 높고, "The Sun Also Rises"를 언급한 문서 2는 그 제목 생성 시 높다. 흥미롭게도 각 제목의 첫 토큰 이후 사후분포가 평평해진다 — 제목의 나머지는 BART의 파라미터 지식만으로 완성 가능하다는 뜻이며, 실제로 BART 단독에 부분 디코딩 "The Sun을 주면 "The Sun Also Rises"를 완성한다. 비파라미터 메모리가 생성을 유도해 파라미터 메모리 속 특정 지식을 끌어내는 협업의 예시. (p.6-7)
- **표 3 (p.7)**: 생성 예시. MSMARCO "define middle ear"에서 BART는 "The middle ear is the part of the ear between the middle ear and the nose"(사실 오류 ?)인 반면 RAG-S는 "The middle ear includes the tympanic cavity and the three ossicles."(정확). Jeopardy "Washington"에서 BART는 "This state has the largest number of counties in the U.S."(오류) vs RAG-T "It's the only U.S. state named for a U.S. president"(정확·구체적). "The Divine Comedy"에서 BART는 "the Inferno, the Purgatorio & the Purgatorio"(부분 오류 *) vs RAG-S ""Inferno", "Purgatorio" & "Paradiso""(정확).
- **표 4 (p.8)** — Jeopardy 인간 평가 (452 생성 쌍): 사실성 — BART 우위 7.1% / RAG 우위 42.7% / 둘 다 좋음 11.7% / 둘 다 나쁨 17.7% / 다수결 없음 20.8%. 구체성 — BART 우위 16.8% / RAG 우위 37.4% / 둘 다 좋음 11.8% / 둘 다 나쁨 6.9% / 다수결 없음 20.1%.
- **표 5 (p.8)** — 고유 trigram/전체 trigram 비율(다양성): MSMARCO에서 Gold 89.6% > RAG-Seq 83.5% > RAG-Token 77.8% > BART 70.7%; Jeopardy에서 Gold 90.0% > RAG-Seq 53.8% > RAG-Token 46.8% > BART 32.4%. 다양성 촉진 디코딩 없이도 RAG가 훨씬 다양.
- **표 6 (p.8)** — dev셋 절제 실험 (FEVER는 분류라 두 RAG가 동치):
  | 모델 | NQ | TQA | WQ | CT | Jeopardy B-1/QB-1 | MSMarco R-L/B-1 | FVR3/FVR2 |
  |---|---|---|---|---|---|---|---|
  | RAG-Token-BM25 | 29.7 | 41.5 | 32.1 | 33.1 | 17.5/22.3 | 55.5/48.4 | 75.1/91.6 |
  | RAG-Seq-BM25 | 31.8 | 44.1 | 36.6 | 33.8 | 11.1/19.5 | 56.5/46.9 | 75.1/91.6 |
  | RAG-Token-Frozen | 37.8 | 50.1 | 37.1 | 51.1 | 16.7/21.7 | 55.9/49.4 | 72.9/89.4 |
  | RAG-Seq-Frozen | 41.2 | 52.1 | 41.8 | 52.6 | 11.8/19.6 | 56.7/47.3 | 72.9/89.4 |
  | RAG-Token | 43.5 | 54.8 | **46.5** | 51.9 | **17.9/22.6** | 56.2/49.4 | 74.5/90.6 |
  | RAG-Sequence | **44.0** | **55.8** | 44.9 | **53.4** | 15.3/21.5 | **57.2**/47.5 | 74.5/90.6 |
  학습된 검색(미고정)이 전 과제에서 고정 리트리버를 이긴다. BM25는 FEVER에서만 최고(75.1/91.6) — claim이 엔티티 중심이라 단어 중첩 검색에 유리; 오픈도메인 QA에서는 밀집 미분가능 검색이 결정적(NQ 44.0 vs BM25 31.8).
- **인덱스 핫스왑 (p.7-8)**: 2016년 12월 DrQA 위키 덤프 인덱스 vs 본 실험의 2018년 12월 인덱스. 시기 사이에 바뀐 세계 지도자 82명에 대해 "Who is {position}?" 템플릿 질의: 2016 인덱스 + 2016 지도자 70% 정답, 2018 인덱스 + 2018 지도자 68% 정답; 불일치 조합은 급락(2018 인덱스 + 2016 지도자 12%, 2016 인덱스 + 2018 지도자 4%). 재학습 없이 비파라미터 메모리 교체만으로 세계 지식이 갱신됨을 입증.
- **그림 3 (p.8)** — 3개 패널, x축은 모두 테스트 시 검색 문서 수 K(10~50). **좌**: NQ Exact Match(y축 39~44). RAG-Sequence(점선)는 K 증가에 따라 단조 상승해 K=50 부근에서 약 44에 도달, RAG-Token(실선)은 K=10 부근 약 43으로 정점 후 완만히 하락. **중**: NQ Answer Recall@K(y축 40~80). RAG-Token/RAG-Seq와 Fixed DPR이 비슷하게 70~80대로 상승, BM25는 일관되게 그 아래(약 50→60대). **우**: MSMARCO Bleu-1/Rouge-L(y축 48~56). RAG-Token은 K 증가 시 Rouge-L 상승·Bleu-1 하락의 트레이드오프, RAG-Sequence는 변화가 완만. 학습은 K∈{5,10}으로 했고 둘 사이 유의한 차이는 없었음.

> [!note] 해석
> 절제 결과(표 6)에서 "검색이 얼마나 중요한가"는 과제에 따라 크게 갈린다 — NQ는 BM25로 12점 이상 추락하지만 FEVER는 오히려 BM25가 낫다. 즉 RAG의 이득은 "검색 난이도가 의미 매칭을 요구하는 과제"에 집중되며, 이 비대칭은 이후 하이브리드(BM25+dense) 검색 연구의 동기가 된다. 또한 표 2에서 Jeopardy는 RAG-Token이, MSMARCO는 RAG-Sequence가 우세한 패턴은 "여러 문서의 사실 조합이 필요한가"로 깔끔히 설명되는데, 이는 그림 2의 사후확률 분석과 정합적이다.

**원문 페이지**: p.5-8

---

## 5 Related Work

**핵심 주장**
- 검색이 개별 과제(오픈도메인 QA, 사실 검증, 장문 QA, 위키 문서 생성, 대화, 번역, 언어모델링)의 성능을 올린다는 선행 연구는 많지만, 본 연구는 단일 검색 기반 아키텍처가 여러 과제에서 동시에 강함을 보인 점이 다르다.
- GPT-2, BART, T5 등 범용 사전학습 아키텍처의 흐름에 "학습되는 검색 모듈"을 더해 단일 통합 아키텍처의 과제 범위를 확장한다.
- 메모리가 분산 표현이 아닌 **원시 텍스트**라는 점이 핵심 — (i) 사람이 읽을 수 있어 해석 가능성을 주고, (ii) 사람이 쓸 수 있어 인덱스 편집으로 메모리를 동적 갱신할 수 있다.

**근거·데이터 요약**
- 학습된 검색 선행 연구: 탐색(search), 강화학습, 잠재변수 접근(ORQA, REALM — 본 연구와 같은 계열)으로 특정 다운스트림 과제용 검색을 최적화. 본 연구는 단일 아키텍처의 다과제 미세조정을 시연. (p.9)
- retrieve-and-edit 계열(기계번역, 의미 파싱)과의 차이: 검색된 항목을 가볍게 편집하는 게 아니라 여러 검색 콘텐츠의 내용을 집계하고, 잠재 검색을 학습하며, 유사 학습쌍이 아닌 증거 문서를 검색한다. (p.9)

**원문 페이지**: p.8-9

---

## 6 Discussion

**핵심 주장**
- 파라미터·비파라미터 메모리에 모두 접근하는 하이브리드 생성 모델로 오픈도메인 QA SotA를 달성했고, 인간은 순수 파라미터 BART보다 RAG의 생성을 더 사실적·구체적이라 평가했다.
- 학습된 검색 컴포넌트의 효과를 검증했고, 재학습 없이 검색 인덱스를 핫스왑해 모델을 갱신할 수 있음을 보였다.
- 향후 과제: 두 컴포넌트를 처음부터(from scratch) 공동 사전학습하는 것(BART식 디노이징 또는 다른 목적함수), 그리고 두 메모리의 상호작용과 결합 방법 연구.

**근거·데이터 요약**
- 본문 4장의 결과 종합 외 신규 실험 없음. (p.9)

**원문 페이지**: p.9

---

## Broader Impact

**핵심 주장**
- 실제 사실 지식(위키피디아)에 더 강하게 접지(grounding)되어 환각이 적고 더 사실적이며, 제어·해석 가능성이 높다는 사회적 이점이 있다 — 예: 의료 인덱스를 달아 오픈도메인 의료 질의에 활용.
- 단, 위키피디아 등 어떤 외부 지식원도 완전히 사실적이고 편향 없을 수는 없으며, 언어모델로 쓰일 수 있으므로 GPT-2와 유사한 악용 우려(허위/오도 콘텐츠 생성, 사칭, 스팸/피싱 자동화)가 — 정도는 덜할지라도 — 유효하다.

**근거·데이터 요약**
- 완화책으로 오도 콘텐츠·자동 스팸과 싸우는 AI 시스템 활용을 제안. 향후 수십 년 내 직업 자동화 가능성도 언급. (p.10)

**원문 페이지**: p.10

---

## 부록 A–I (Appendices)

**핵심 주장**
- 테스트 시 검색 문서 수·디코딩 방식은 과제별로 다르게 최적화했다: 오픈도메인 QA는 RAG-Token 15문서 / RAG-Sequence 50문서 + Thorough Decoding + 탐욕 디코딩, 생성 과제는 둘 다 10문서 + 빔 4 + Fast Decoding.
- RAG의 학습 가능 파라미터는 총 626M(DPR BERT-base 인코더 110M×2 + BART-large 406M)으로, NQ에서 비슷한 크기의 T5-large(770M, EM 28.9)를 크게 상회(44.5)한다 — 하이브리드 모델은 훨씬 적은 파라미터로 강한 QA 성능을 낸다.
- 일부 과제(스토리 생성)에서는 검색이 "붕괴(retrieval collapse)"해 입력과 무관하게 같은 문서만 검색하고 생성기가 문서를 무시하게 된다 — 사실 지식 요구가 약하거나 목표 시퀀스가 길어 리트리버 그래디언트가 빈약한 경우.

**근거·데이터 요약**
- **A 구현 (p.17)**: 위 디코딩 설정. QA는 빔 서치가 도움이 안 돼 탐욕 디코딩 사용.
- **B 인간 평가 / 그림 4 (p.17)**: 사실성 평가용 주석 UI 스크린샷 — 답("Washington")과 문장 A/B를 제시하고 "A가 더 사실적 / B가 더 사실적 / 둘 다 / 둘 다 아님" 4지선다. 화면 위치 편향 방지를 위해 모델-문장 배정을 무작위화, 골드 문장을 섞어 주석자 정확도를 검사해 부진한 주석자 2명의 데이터를 제거.
- **C 학습 설정 (p.17)**: Fairseq, 혼합 정밀도, 32GB V100 8장(단일 GPU로도 가능). FAISS MIPS는 CPU에서 충분히 빨라 인덱스를 CPU 메모리에 저장 — 전체 위키피디아에 약 100GB, FAISS 압축 후 36GB. 이후 HuggingFace Transformers로 포팅(동등 성능).
- **D 오픈도메인 QA 상세 (p.18)**: NQ/WQ는 복수 답 주석을 (q,a)쌍별 학습으로 활용(소폭 향상). TriviaQA는 top-1000 문서에 안 나오는 답 후보(이모지, 철자 변형) 필터링. CuratedTrec은 정규식 답을 top-1000 문서 최빈 매칭 문자열로 전처리. TQA-Wiki 공식 테스트셋 점수가 표준 분할보다 훨씬 높은 이유는 질문이 위키피디아로 답하기 쉬운 쪽이기 때문으로 추정.
- **E FEVER 상세 (p.18)**: BART 분류 관행대로 claim을 재생성 후 최종 은닉 상태 표현으로 분류, 문서에 걸쳐 주변화. FEVER의 증거 문장 추출 서브태스크는 위키 덤프 버전이 달라 직접 다루지 않음.
- **F 널 문서 (p.18)**: REALM식 "널 문서" 로짓(임베딩/정적 바이어스/신경망 예측 3종)을 실험했으나 성능 향상이 없어 제외. MSMARCO에서 모델이 검색 이득이 적은 질문에 대해 특정 문서 집합을 일관 검색하도록 스스로 학습함을 관찰 — 널 문서 메커니즘이 불필요할 수 있다는 시사.
- **G 파라미터 (p.18-19)**: 학습 가능 626M + 비파라미터 인덱스 21M개 × 728차원 벡터(153억 값, 8-bit 부동소수점 저장 가능).
- **H 검색 붕괴 (p.19)**: 위 핵심 주장 3 참조; Perez et al.도 다운스트림 성능 최적화 시 허위(spurious) 검색을 보고.
- **표 7 (p.19)** — 데이터셋 인스턴스 수 (학습/개발/테스트): NQ 79,169/8,758/3,611; TriviaQA 78,786/8,838/11,314; WebQuestions 3,418/362/2,033; CuratedTrec 635/134/635; Jeopardy QGen 97,392/13,714/26,849; MS-MARCO 153,726/12,468/101,093*(*숨겨진 부분집합으로 평가); FEVER-3 145,450/10,000/10,000; FEVER-2 96,966/6,666/6,666.

> [!note] 해석
> 부록 H의 "검색 붕괴"는 본문에 없는 가장 중요한 한계 고지다 — RAG식 잠재 검색 학습이 모든 생성 과제에 통하는 게 아니라, 사실 지식 의존성이 강하고 출력이 짧은 과제에서만 안정적으로 학습된다는 경계 조건을 시사한다. 또한 부록 G의 "626M으로 T5-11B를 이긴다"는 비교는 이후 'retrieval은 파라미터의 대체재'라는 retro/Atlas 계열 스케일링 논증의 출발점이 됐다.

**원문 페이지**: p.17-19

---

> [!note] 카드 메모
> 페이지 번호는 arXiv v4 PDF(전체 19쪽) 기준이다. p.10-16은 참고문헌이라 별도 카드를 만들지 않았다. NeurIPS 2020 본 회의록 판과 페이지 구성이 다를 수 있다.

---

## 그림·표 커버리지

- 원문(텍스트 휴리스틱 추출): Figure 1-4 / Table 1-7
- 카드에서 언급 확인: Figure 1-4 / Table 1-7
- 미확인 항목 없음
- (기계 백필 장부 — 휴리스틱 기반이므로 심층 감사 시 갱신)
